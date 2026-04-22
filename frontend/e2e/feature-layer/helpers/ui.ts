import type { Page } from '@playwright/test';

export function installDialogResponder(page: Page, replies: string[]) {
  page.on('dialog', async (dialog) => {
    if (dialog.type() === 'confirm') {
      await dialog.accept();
      return;
    }
    if (dialog.type() === 'prompt') {
      await dialog.accept(replies.shift() ?? '');
      return;
    }
    await dialog.dismiss();
  });
}

export function captureConsoleErrors(page: Page): string[] {
  const errors: string[] = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') {
      errors.push(msg.text());
    }
  });
  return errors;
}
