import { afterEach, beforeEach, describe, expect, it, jest } from '@jest/globals';
import '@testing-library/jest-dom';
import { userbaseApi } from './userbase';
import apiClient from './client';

describe('userbaseApi', () => {
  let getSpy: jest.SpiedFunction<typeof apiClient.get>;

  beforeEach(() => {
    getSpy = jest.spyOn(apiClient, 'get');
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('hospitals.list calls correct endpoint', async () => {
    getSpy.mockResolvedValue({ data: [] } as never);
    await userbaseApi.hospitals.list();
    expect(apiClient.get).toHaveBeenCalledWith('/api/hospitals/');
  });

  it('users.list calls correct endpoint with params', async () => {
    getSpy.mockResolvedValue({ data: [] } as never);
    await userbaseApi.users.list({ role: 'RESIDENT' });
    expect(apiClient.get).toHaveBeenCalledWith('/api/users/', { params: { role: 'RESIDENT' } });
  });
});

describe('directory response and mutation contracts', () => {
  afterEach(() => jest.restoreAllMocks());

  const lists = [
    ['hospitals', '/api/hospitals/', () => userbaseApi.hospitals.list()],
    ['departments', '/api/departments/', () => userbaseApi.departments.list()],
    ['matrix', '/api/hospital-departments/', () => userbaseApi.matrix.list()],
    ['users', '/api/users/', () => userbaseApi.users.list()],
    ['staff', '/api/staff/', () => userbaseApi.staff.list()],
  ] as const;
  it.each(lists)('%s accepts array, paginated and empty responses', async (_name, endpoint, read) => {
    const get = jest.spyOn(apiClient, 'get');
    for (const [data, expected] of [[[{id:1}], [{id:1}]], [{results:[{id:1}], count:50}, [{id:1}]], [{count:0}, []]]) {
      get.mockResolvedValueOnce({data} as never);
      expect(await read()).toEqual(expected);
      expect(get.mock.calls.at(-1)?.[0]).toBe(endpoint);
    }
  });

  it.each([[{count: 105, results:[{id:1}]},105], [[{id:1},{id:2}],2], [{},0], [{count:0},0]])('uses the server total for dashboard counts %#', async (data, total) => {
    const get = jest.spyOn(apiClient, 'get').mockResolvedValue({ data } as never);
    expect(await userbaseApi.users.count({role:'RESIDENT',active:true})).toBe(total);
    expect(get).toHaveBeenCalledWith('/api/users/', {params:{role:'RESIDENT',active:true,page_size:1}});
  });

  const reads = [
    ['/api/hospitals/7/departments/', () => userbaseApi.hospitals.listDepartments(7)],
    ['/api/departments/7/roster/', () => userbaseApi.departments.roster(7)],
    ['/api/users/7/', () => userbaseApi.users.get(7)],
    ['/api/residents/7/', () => userbaseApi.residents.get(7)],
    ['/api/supervisors/7/', () => userbaseApi.supervisors.get(7)],
    ['/api/admin/data-quality/summary', () => userbaseApi.dataQuality.summary()],
    ['/api/admin/data-quality/audit', () => userbaseApi.dataQuality.audit()],
  ] as const;
  it.each(reads)('returns the detail response from %s', async (endpoint, read) => {
    const get = jest.spyOn(apiClient, 'get').mockResolvedValue({data:{id:7}} as never);
    expect(await read()).toEqual({id:7}); expect(get).toHaveBeenCalledWith(endpoint);
  });

  it.each([undefined, 'missing_dates'])('passes optional data quality filter %s', async filter => {
    const get = jest.spyOn(apiClient, 'get').mockResolvedValue({data:[]} as never);
    expect(await userbaseApi.dataQuality.users(filter)).toEqual([]);
    expect(get).toHaveBeenCalledWith('/api/admin/data-quality/users', {params:filter ? {filter} : undefined});
  });

  const mutations = [
    ['post','/api/hospitals/', {name:'New'}, () => userbaseApi.hospitals.create({name:'New'})],
    ['patch','/api/hospitals/7/', {active:false}, () => userbaseApi.hospitals.update(7,{active:false})],
    ['post','/api/departments/', {name:'New'}, () => userbaseApi.departments.create({name:'New'})],
    ['patch','/api/departments/7/', {active:false}, () => userbaseApi.departments.update(7,{active:false})],
    ['post','/api/hospital-departments/', {hospital_id:1,department_id:2}, () => userbaseApi.matrix.create({hospital_id:1,department_id:2})],
    ['patch','/api/hospital-departments/7/', {active:false}, () => userbaseApi.matrix.update(7,{active:false})],
    ['post','/api/users/', {full_name:'Person',role:'ADMIN'}, () => userbaseApi.users.create({full_name:'Person',role:'ADMIN'})],
    ['patch','/api/users/7/', {is_active:false}, () => userbaseApi.users.update(7,{is_active:false})],
    ['patch','/api/residents/7/', {training_level:'2'}, () => userbaseApi.residents.update(7,{training_level:'2'})],
    ['patch','/api/staff/7/', {designation:'Office'}, () => userbaseApi.staff.update(7,{designation:'Office'})],
    ['post','/api/department-memberships/', {department:1}, () => userbaseApi.memberships.create({department:1})],
    ['patch','/api/department-memberships/7/', {active:false}, () => userbaseApi.memberships.update(7,{active:false})],
    ['post','/api/hospital-assignments/', {hospital:1}, () => userbaseApi.hospitalAssignments.create({hospital:1})],
    ['patch','/api/hospital-assignments/7/', {active:false}, () => userbaseApi.hospitalAssignments.update(7,{active:false})],
  ] as const;
  it.each(mutations)('%s %s preserves payload and returns the saved row', async (method, endpoint, payload, mutate) => {
    const spy = jest.spyOn(apiClient,method).mockResolvedValue({data:{id:7}} as never);
    expect(await mutate()).toEqual({id:7}); expect(spy).toHaveBeenCalledWith(endpoint,payload);
  });

  it.each([
    ['/api/hospitals/7/', () => userbaseApi.hospitals.delete(7)],
    ['/api/departments/7/', () => userbaseApi.departments.delete(7)],
    ['/api/department-memberships/7/', () => userbaseApi.memberships.remove(7)],
    ['/api/hospital-assignments/7/', () => userbaseApi.hospitalAssignments.remove(7)],
  ] as const)('deletes %s without requiring a response body', async (endpoint, remove) => {
    const spy=jest.spyOn(apiClient,'delete').mockResolvedValue({status:204} as never);
    expect(await remove()).toBeUndefined(); expect(spy).toHaveBeenCalledWith(endpoint);
  });

  it('recomputes data quality on the explicit mutation endpoint', async () => {
    const spy=jest.spyOn(apiClient,'post').mockResolvedValue({data:{total_users:3}} as never);
    expect(await userbaseApi.dataQuality.recompute()).toEqual({total_users:3});
    expect(spy).toHaveBeenCalledWith('/api/admin/data-quality/recompute');
  });

  it('propagates permission and network failures to the caller', async () => {
    const error = new Error('permission denied');
    jest.spyOn(apiClient,'patch').mockRejectedValue(error);
    await expect(userbaseApi.users.update(7,{is_active:false})).rejects.toBe(error);
    jest.spyOn(apiClient,'get').mockRejectedValue(error);
    await expect(userbaseApi.users.list()).rejects.toBe(error);
  });
});
