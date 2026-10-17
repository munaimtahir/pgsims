/** @jest-environment node */
import { describe, expect, it } from '@jest/globals';
import { NextRequest } from 'next/server';
import { middleware } from './middleware';

const token = (payload: unknown) => `header.${Buffer.from(JSON.stringify(payload)).toString('base64url')}.signature`;
const future = () => Math.floor(Date.now()/1000)+600;
function request(path: string, cookies: Record<string,string> = {}) {
  const req = new NextRequest(`http://localhost${path}`);
  for (const [key,value] of Object.entries(cookies)) req.cookies.set(key,value);
  return req;
}
const auth = (role: string) => ({pgsims_access_token:token({role,exp:future()})});

describe('dashboard routing hints', () => {
  it('leaves non-dashboard URLs to their application/backend guards', () => {
    expect(middleware(request('/complete-profile')).headers.get('x-middleware-next')).toBe('1');
  });
  it('redirects missing authentication to login', () => {
    expect(middleware(request('/dashboard/resident')).headers.get('location')).toBe('http://localhost/login');
  });
  const paths=['/dashboard/pg','/dashboard/resident','/dashboard/supervisor','/dashboard/admin','/dashboard/utrmc','/dashboard/account'];
  const matrix = [
    ['ADMIN','/dashboard/utrmc',[true,true,true,true,true,true]],
    ['RESIDENT','/dashboard/resident',[true,true,false,false,false,true]],
    ['SUPERVISOR','/dashboard/supervisor',[false,false,true,false,false,true]],
    ['SUPPORT_STAFF','/dashboard/utrmc',[false,false,false,false,true,true]],
  ] as const;
  it.each(matrix)('routes %s to allowed dashboards and redirects others', (role,home,allowed) => {
    paths.forEach((path,index) => {
      const result=middleware(request(path,auth(role)));
      if (allowed[index]) expect(result.headers.get('x-middleware-next')).toBe('1');
      else expect(result.headers.get('location')).toBe(`http://localhost${home}`);
    });
  });
  it.each([
    token({role:'ADMIN',exp:0}),token({role:'ADMIN',exp:1}),token({role:'INVALID',exp:future()}),
    token({role:12,exp:future()}),'broken','a.%%%bad.b', token(null),token({role:'ADMIN'}),
  ])('clears invalid or expired routing cookies %#', value => {
    const result=middleware(request('/dashboard/admin',{pgsims_access_token:value}));
    expect(result.headers.get('location')).toBe('http://localhost/login');
    for (const name of ['pgsims_access_token','pgsims_user_role','pgsims_access_exp']) {
      expect(result.cookies.get(name)?.value).toBe('');
      expect(result.cookies.get(name)?.expires).toEqual(new Date(0));
    }
  });
  it('accepts the legacy claim name and numeric expiry-cookie fallback', () => {
    const result=middleware(request('/dashboard/supervisor',{pgsims_access_token:token({user_role:'SUPERVISOR'}),pgsims_access_exp:String(future())}));
    expect(result.headers.get('x-middleware-next')).toBe('1');
  });
  it('uses role-cookie fallback only when the JWT claim is not a string', () => {
    const result=middleware(request('/dashboard/resident',{pgsims_access_token:token({role:42,exp:future()}),pgsims_user_role:'RESIDENT'}));
    expect(result.headers.get('x-middleware-next')).toBe('1');
  });
  it.each(['invalid','12.5','-1','0'])('rejects invalid or expired fallback expiry %s', expiry => {
    const result=middleware(request('/dashboard/admin',{pgsims_access_token:token({role:'ADMIN',exp:'not-numeric'}),pgsims_access_exp:expiry}));
    expect(result.headers.get('location')).toBe('http://localhost/login');
  });
  it('does not allow a cookie to override an expired JWT', () => {
    const result=middleware(request('/dashboard/admin',{pgsims_access_token:token({role:'ADMIN',exp:1}),pgsims_access_exp:String(future())}));
    expect(result.headers.get('location')).toBe('http://localhost/login');
  });
});
