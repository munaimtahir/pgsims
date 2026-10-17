import { afterEach, describe, expect, it, jest } from '@jest/globals';
import apiClient from './client';
import { academicsApi as api } from './academics';

afterEach(() => jest.restoreAllMocks());
const prefix='/api/academics/';

describe('academic collection contracts', () => {
  const collections = [
    ['periods/',api.listPeriods],['rotation-templates/',api.listRotationTemplates],
    ['evaluation-templates/',api.listEvaluationTemplates],['logbook-categories/',api.listLogbookCategories],
    ['review-queue/',api.listReviewQueue],['monitoring/departments/',api.getDepartmentMonitoringSummary],
    ['monitoring/programs/',api.getProgramMonitoringSummary],['monitoring/sessions/',api.getSessionMonitoringSummary],
    ['reports/resident-progress/',api.getResidentProgressReportList],['reports/supervisor-workload/',api.getSupervisorWorkloadReportList],
  ] as const;
  it.each(collections)('%s unwraps all supported collection shapes', async (path,read) => {
    const get=jest.spyOn(apiClient,'get');
    for (const data of [[{id:1}],{count:1,results:[{id:1}]},{}]) {
      get.mockResolvedValueOnce({data} as never);
      expect(await read()).toEqual('results' in data || Array.isArray(data) ? [{id:1}] : []);
      expect(get).toHaveBeenLastCalledWith(prefix+path);
    }
  });
  it.each([
    ['training-records/',api.listTrainingRecords],['evaluation-submissions/',api.listEvaluationSubmissions],
    ['logbook-entries/',api.listLogbookEntries],['reports/evaluations/',api.getEvaluationReport],['reports/logbook/',api.getLogbookReport],
  ] as const)('%s preserves filters and handles no matches', async (path,read) => {
    const get=jest.spyOn(apiClient,'get').mockResolvedValue({data:{count:0,results:[]}} as never);
    expect(await read({resident:7,status:'DRAFT',active:true})).toEqual([]);
    expect(get).toHaveBeenCalledWith(prefix+path,{params:{resident:7,status:'DRAFT',active:true}});
    get.mockResolvedValue({data:[{id:7}]} as never);
    expect(await read()).toEqual([{id:7}]);
    expect(get).toHaveBeenLastCalledWith(prefix+path,{params:undefined});
  });
});

describe('academic detail and summary contracts', () => {
  it.each([
    ['overview/',api.getOverview],['data-quality/',api.getDataQuality],['options/',api.getOptions],
    ['residents/me/summary/',api.getMyResidentSummary],['supervisors/me/summary/',api.getMySupervisorSummary],
    ['my-progress/',api.getMyAcademicProgress],['supervisor-workload/',api.getSupervisorAcademicWorkload],
    ['admin-workflow-overview/',api.getAdminAcademicWorkflowOverview],['workflow-data-quality/',api.getAcademicWorkflowDataQuality],
    ['monitoring/admin-dashboard/',api.getAdminDashboardMonitoring],['monitoring/supervisor-dashboard/',api.getSupervisorDashboardMonitoring],
    ['monitoring/my-progress/',api.getMyProgressMonitoring],['reports/data-quality/',api.getDataQualityReport],
  ] as const)('reads %s', async (path,read) => {
    const get=jest.spyOn(apiClient,'get').mockResolvedValue({data:{id:7}} as never);
    expect(await read()).toEqual({id:7}); expect(get).toHaveBeenCalledWith(prefix+path);
  });
  it.each([
    ['training-records/7/',api.getTrainingRecord],['residents/7/summary/',api.getResidentSummary],
    ['supervisors/7/summary/',api.getSupervisorSummary],['evaluation-submissions/7/',api.getEvaluationSubmission],
    ['logbook-entries/7/',api.getLogbookEntry],['residents/7/progress/',api.getResidentAcademicProgress],
    ['reports/resident-progress/7/',api.getResidentProgressReportDetail],['reports/supervisor-workload/7/',api.getSupervisorWorkloadReportDetail],
  ] as const)('reads scoped detail %s', async (path,read) => {
    const get=jest.spyOn(apiClient,'get').mockResolvedValue({data:{id:7}} as never);
    expect(await read(7)).toEqual({id:7}); expect(get).toHaveBeenCalledWith(prefix+path);
  });
});

describe('academic mutations', () => {
  const payload={notes:'Reviewed',resident:7};
  it.each([
    ['training-records/',api.createTrainingRecord],['periods/',api.createPeriod],
    ['rotation-templates/',api.createRotationTemplate],['evaluation-templates/',api.createEvaluationTemplate],
    ['logbook-categories/',api.createLogbookCategory],['review-queue/',api.createReviewQueueItem],
    ['evaluation-submissions/',api.createEvaluationSubmission],['logbook-entries/',api.createLogbookEntry],
  ] as const)('creates through %s', async (path,create) => {
    const post=jest.spyOn(apiClient,'post').mockResolvedValue({data:{id:7,...payload}} as never);
    expect(await create(payload)).toEqual({id:7,...payload}); expect(post).toHaveBeenCalledWith(prefix+path,payload);
  });
  it.each([
    ['training-records/7/',api.updateTrainingRecord],['periods/7/',api.updatePeriod],
    ['rotation-templates/7/',api.updateRotationTemplate],['evaluation-templates/7/',api.updateEvaluationTemplate],
    ['logbook-categories/7/',api.updateLogbookCategory],['review-queue/7/',api.updateReviewQueueItem],
    ['evaluation-submissions/7/',api.updateEvaluationSubmission],['logbook-entries/7/',api.updateLogbookEntry],
  ] as const)('patches %s without replacing unrelated fields', async (path,update) => {
    const patch=jest.spyOn(apiClient,'patch').mockResolvedValue({data:{id:7,...payload}} as never);
    expect(await update(7,payload)).toEqual({id:7,...payload}); expect(patch).toHaveBeenCalledWith(prefix+path,payload);
  });
  it.each([
    ['training-records/7/close/',api.closeTrainingRecord],['evaluation-submissions/7/approve/',api.approveEvaluation],
    ['evaluation-submissions/7/return_revision/',api.returnEvaluation],['evaluation-submissions/7/reject/',api.rejectEvaluation],
    ['logbook-entries/7/verify/',api.verifyLogbookEntry],['logbook-entries/7/return_revision/',api.returnLogbookEntry],
    ['logbook-entries/7/reject/',api.rejectLogbookEntry],
  ] as const)('sends review data to %s', async (path,action) => {
    const post=jest.spyOn(apiClient,'post').mockResolvedValue({data:{id:7}} as never);
    expect(await action(7,payload)).toEqual({id:7}); expect(post).toHaveBeenCalledWith(prefix+path,payload);
  });
  it.each([
    ['evaluation-submissions/7/submit/',api.submitEvaluation],['evaluation-submissions/7/start_review/',api.startEvaluationReview],
    ['evaluation-submissions/7/cancel/',api.cancelEvaluation],['logbook-entries/7/submit/',api.submitLogbookEntry],
    ['logbook-entries/7/cancel/',api.cancelLogbookEntry],
  ] as const)('uses the explicit transition %s', async (path,action) => {
    const post=jest.spyOn(apiClient,'post').mockResolvedValue({data:{id:7}} as never);
    expect(await action(7)).toEqual({id:7}); expect(post).toHaveBeenCalledWith(prefix+path);
  });
  it.each([['seed/',api.seedPilotAcademics],['seed-workflows/',api.seedWorkflows]] as const)('keeps %s as an explicit POST contract without executing a real seed', async (path,action) => {
    const post=jest.spyOn(apiClient,'post').mockResolvedValue({data:{created:2}} as never);
    expect(await action()).toEqual({created:2}); expect(post).toHaveBeenCalledWith(prefix+path);
  });
  it('propagates rejected workflow transitions and unavailable summaries', async () => {
    const failure={response:{status:409,data:{detail:'Invalid transition'}}};
    jest.spyOn(apiClient,'post').mockRejectedValue(failure);
    await expect(api.approveEvaluation(7,payload)).rejects.toBe(failure);
    jest.spyOn(apiClient,'get').mockRejectedValue(new Error('offline'));
    await expect(api.getMyResidentSummary()).rejects.toThrow('offline');
  });
});
