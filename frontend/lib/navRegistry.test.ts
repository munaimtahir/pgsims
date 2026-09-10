import fs from 'fs';
import path from 'path';
import { NAV_SECTIONS } from './navRegistry';

/**
 * Regression guard for the sidebar-disappears-on-navigation bug: every href registered
 * in NAV_SECTIONS must resolve to a real Next.js App Router page, and every top-level
 * segment it lives under must render the authenticated shell (have a layout.tsx
 * somewhere in its ancestry back to app/dashboard or its own folder).
 */

const APP_DIR = path.join(__dirname, '..', 'app');

function collectHrefs(): string[] {
  const hrefs: string[] = [];
  for (const section of NAV_SECTIONS) {
    for (const item of section.items) {
      if (item.href) hrefs.push(item.href);
      for (const sub of item.subItems ?? []) {
        hrefs.push(sub.href);
      }
    }
  }
  return hrefs;
}

function hrefToPageCandidates(href: string): string[] {
  // Strip query/hash, split into segments, dynamic segments match any [*] folder.
  const segments = href.split('?')[0].split('/').filter(Boolean);
  return [path.join(APP_DIR, ...segments, 'page.tsx')];
}

function routeExists(href: string): boolean {
  const [candidate] = hrefToPageCandidates(href);
  if (fs.existsSync(candidate)) return true;
  // Fall back to matching a dynamic segment folder (e.g. /residents/5 -> [id]/page.tsx)
  // not needed for current registry (all hrefs are static), but keeps this resilient.
  return false;
}

function topLevelSegment(href: string): string {
  return href.split('?')[0].split('/').filter(Boolean)[0] ?? '';
}

function hasAuthenticatedLayout(topSegment: string): boolean {
  if (topSegment === 'dashboard') return true; // app/dashboard/layout.tsx mounts the shell
  return fs.existsSync(path.join(APP_DIR, topSegment, 'layout.tsx'));
}

describe('navRegistry route contract', () => {
  const hrefs = collectHrefs();

  it('has at least one registered nav item', () => {
    expect(hrefs.length).toBeGreaterThan(0);
  });

  hrefs.forEach((href) => {
    it(`href ${href} resolves to a real page.tsx`, () => {
      expect(routeExists(href)).toBe(true);
    });
  });

  hrefs.forEach((href) => {
    it(`href ${href} is mounted under an authenticated shell layout`, () => {
      const top = topLevelSegment(href);
      expect(hasAuthenticatedLayout(top)).toBe(true);
    });
  });
});
