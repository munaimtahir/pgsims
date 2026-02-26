# Integration Truth Map (Backend <-> Frontend) — PGSIMS / UTRMC

Generated from repo inspection (static scan + Django URL resolver extraction). This document is canonical and contract-adjacent documentation only; no route changes or UI redesign were made in this run.

## Scope / Method
- Backend endpoint inventory extracted via Django URL resolver (DRF routers + urlpatterns), then filtered to project-exposed API routes (`sims.*`) plus the exposed SimpleJWT refresh endpoint.
- Frontend inventory extracted from `frontend/lib/api/*.ts` (`apiClient` / `axios` calls), then enriched with page/component call sites by static grep.
- Cross-linking performed on normalized `(HTTP method, path)` pairs with parameter placeholder normalization (`<int:pk>`, regex groups, template literals).
- Dynamic URL helper case (`certificatesApi.downloadCertificate`) was manually normalized to the backend certificate download endpoint.

Summary counts:
- Backend API endpoints (exposed): **114**
- Frontend outbound API calls: **80**
- Frontend calls matched: **80**
- Frontend calls unmatched (real drift): **0**
- Backend endpoints with frontend consumers: **59**
- Backend endpoints without current Next.js consumers (classified): **55**

## A) Backend Inventory
Notes:
- `Permission(s)` is extracted from DRF class attributes when available; function-based views may appear with decorator-resolved permissions only.
- `Scope Rule` is a repo-derived heuristic label and references view logic for core flows.
- DRF router format-suffix duplicates are intentionally listed and classified as internal duplicates.

| Method(s) | Path | View/Class | Action | Serializer | Permission(s) | Scope Rule | Frontend Consumer(s) / Classification |
|---|---|---|---|---|---|---|---|
| GET,POST | `/academics/api/batches/` | `BatchViewSet` | `create,list` | `BatchSerializer` | `IsAuthenticated` | ALL / view-specific | `academicsApi.list` (lib/api/academics.ts:73); `academicsApi.create` (lib/api/academics.ts:81) |
| DELETE,GET,PATCH,PUT | `/academics/api/batches/(?P<pk>[/.]+)/` | `BatchViewSet` | `destroy,partial_update,retrieve,update` | `BatchSerializer` | `IsAuthenticated` | ALL / view-specific | `academicsApi.delete` (lib/api/academics.ts:89); `academicsApi.get` (lib/api/academics.ts:77); `academicsApi.update` (lib/api/academics.ts:85) |
| GET | `/academics/api/batches/(?P<pk>[/.]+)/students/` | `BatchViewSet` | `students` | `BatchSerializer` | `IsAuthenticated` | ALL / view-specific | `academicsApi.getStudents` (lib/api/academics.ts:92) |
| GET | `/academics/api/batches/(?P<pk>[/.]+)/students\.(?P<format>[a-z0-9]+)/?` | `BatchViewSet` | `students` | `BatchSerializer` | `IsAuthenticated` | ALL / view-specific | [internal] DRF format-suffix duplicate route |
| DELETE,GET,PATCH,PUT | `/academics/api/batches/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?` | `BatchViewSet` | `destroy,partial_update,retrieve,update` | `BatchSerializer` | `IsAuthenticated` | ALL / view-specific | [internal] DRF format-suffix duplicate route |
| GET,POST | `/academics/api/batches\.(?P<format>[a-z0-9]+)/?` | `BatchViewSet` | `create,list` | `BatchSerializer` | `IsAuthenticated` | ALL / view-specific | [internal] DRF format-suffix duplicate route |
| GET,POST | `/academics/api/departments/` | `DepartmentViewSet` | `create,list` | `DepartmentSerializer` | `ReadAnyWriteAdminOrUTRMCAdmin` | ALL read; admin/utrmc_admin write | `academicsApi.list` (lib/api/academics.ts:48); `academicsApi.create` (lib/api/academics.ts:56) |
| DELETE,GET,PATCH,PUT | `/academics/api/departments/(?P<pk>[/.]+)/` | `DepartmentViewSet` | `destroy,partial_update,retrieve,update` | `DepartmentSerializer` | `ReadAnyWriteAdminOrUTRMCAdmin` | ALL read; admin/utrmc_admin write | `academicsApi.delete` (lib/api/academics.ts:64); `academicsApi.get` (lib/api/academics.ts:52); `academicsApi.update` (lib/api/academics.ts:60) |
| DELETE,GET,PATCH,PUT | `/academics/api/departments/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?` | `DepartmentViewSet` | `destroy,partial_update,retrieve,update` | `DepartmentSerializer` | `ReadAnyWriteAdminOrUTRMCAdmin` | ALL read; admin/utrmc_admin write | [internal] DRF format-suffix duplicate route |
| GET,POST | `/academics/api/departments\.(?P<format>[a-z0-9]+)/?` | `DepartmentViewSet` | `create,list` | `DepartmentSerializer` | `ReadAnyWriteAdminOrUTRMCAdmin` | ALL / view-specific | [internal] DRF format-suffix duplicate route |
| GET,POST | `/academics/api/students/` | `StudentProfileViewSet` | `create,list` | `StudentProfileSerializer` | `IsAuthenticated` | OWN \| SUPERVISEES \| ALL | `academicsApi.list` (lib/api/academics.ts:102); `academicsApi.create` (lib/api/academics.ts:110) |
| DELETE,GET,PATCH,PUT | `/academics/api/students/(?P<pk>[/.]+)/` | `StudentProfileViewSet` | `destroy,partial_update,retrieve,update` | `StudentProfileSerializer` | `IsAuthenticated` | OWN \| SUPERVISEES \| ALL | `academicsApi.delete` (lib/api/academics.ts:118); `academicsApi.get` (lib/api/academics.ts:106); `academicsApi.update` (lib/api/academics.ts:114) |
| POST | `/academics/api/students/(?P<pk>[/.]+)/update_status/` | `StudentProfileViewSet` | `update_status` | `StudentProfileSerializer` | `IsAuthenticated` | OWN \| SUPERVISEES \| ALL | `academicsApi.updateStatus` (lib/api/academics.ts:121) |
| POST | `/academics/api/students/(?P<pk>[/.]+)/update_status\.(?P<format>[a-z0-9]+)/?` | `StudentProfileViewSet` | `update_status` | `StudentProfileSerializer` | `IsAuthenticated` | OWN \| SUPERVISEES \| ALL | [internal] DRF format-suffix duplicate route |
| DELETE,GET,PATCH,PUT | `/academics/api/students/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?` | `StudentProfileViewSet` | `destroy,partial_update,retrieve,update` | `StudentProfileSerializer` | `IsAuthenticated` | OWN \| SUPERVISEES \| ALL | [internal] DRF format-suffix duplicate route |
| GET,POST | `/academics/api/students\.(?P<format>[a-z0-9]+)/?` | `StudentProfileViewSet` | `create,list` | `StudentProfileSerializer` | `IsAuthenticated` | ALL / view-specific | [internal] DRF format-suffix duplicate route |
| GET | `/api/analytics/comparative/` | `ComparativeAnalyticsView` | `list/custom` | `n/a` | `IsAuthenticated` | ALL / view-specific | [backend-only] no current Next.js consumer found by static scan |
| GET | `/api/analytics/dashboard/compliance/` | `DashboardComplianceView` | `list/custom` | `n/a` | `IsAuthenticated` | ALL / view-specific | `analyticsApi.getCompliance` (lib/api/analytics.ts:58) |
| GET | `/api/analytics/dashboard/overview/` | `DashboardOverviewView` | `list/custom` | `n/a` | `IsAuthenticated` | ALL / view-specific | `analyticsApi.getDashboardOverview` (lib/api/analytics.ts:42) |
| GET | `/api/analytics/dashboard/trends/` | `DashboardTrendsView` | `list/custom` | `n/a` | `IsAuthenticated` | ALL / view-specific | `analyticsApi.getTrends` (lib/api/analytics.ts:50) |
| GET | `/api/analytics/performance/` | `PerformanceMetricsView` | `list/custom` | `n/a` | `IsAuthenticated` | ALL / view-specific | `analyticsApi.getPerformance` (lib/api/analytics.ts:66) |
| GET | `/api/analytics/trends/` | `TrendAnalyticsView` | `list/custom` | `n/a` | `IsAuthenticated` | ALL / view-specific | [backend-only] no current Next.js consumer found by static scan |
| GET | `/api/attendance/summary/` | `AttendanceSummaryView` | `list/custom` | `n/a` | `IsAuthenticated` | ALL / view-specific | `attendanceApi.getSummary` (lib/api/attendance.ts:38) |
| POST | `/api/attendance/upload/` | `BulkAttendanceUploadView` | `custom` | `n/a` | `IsAuthenticated` | ALL / view-specific | `attendanceApi.bulkUpload` (lib/api/attendance.ts:49) |
| GET | `/api/audit/activity/` | `ActivityLogViewSet` | `list` | `ActivityLogSerializer` | `IsAdminUser` | ALL / view-specific | `auditApi.getActivityLogs` (lib/api/audit.ts:31) |
| GET | `/api/audit/activity/(?P<pk>[/.]+)/` | `ActivityLogViewSet` | `retrieve` | `ActivityLogSerializer` | `IsAdminUser` | ALL / view-specific | [admin-only/system-only] exposed for admin operations; current pages may use subset only |
| GET | `/api/audit/activity/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?` | `ActivityLogViewSet` | `retrieve` | `ActivityLogSerializer` | `IsAdminUser` | ALL / view-specific | [internal] DRF format-suffix duplicate route |
| GET | `/api/audit/activity/export/` | `ActivityLogViewSet` | `export_csv` | `ActivityLogSerializer` | `IsAdminUser` | ALL / view-specific | [admin-only/system-only] exposed for admin operations; current pages may use subset only |
| GET | `/api/audit/activity/export\.(?P<format>[a-z0-9]+)/?` | `ActivityLogViewSet` | `export_csv` | `ActivityLogSerializer` | `IsAdminUser` | ALL / view-specific | [internal] DRF format-suffix duplicate route |
| GET | `/api/audit/activity\.(?P<format>[a-z0-9]+)/?` | `ActivityLogViewSet` | `list` | `ActivityLogSerializer` | `IsAdminUser` | ALL / view-specific | [internal] DRF format-suffix duplicate route |
| GET,POST | `/api/audit/reports/` | `AuditReportViewSet` | `create,list` | `AuditReportSerializer` | `IsAdminUser` | ALL / view-specific | `auditApi.getReports` (lib/api/audit.ts:39); `auditApi.createReport` (lib/api/audit.ts:47) |
| GET | `/api/audit/reports/latest/` | `AuditReportViewSet` | `latest` | `AuditReportSerializer` | `IsAdminUser` | ALL / view-specific | [admin-only/system-only] exposed for admin operations; current pages may use subset only |
| GET | `/api/audit/reports/latest\.(?P<format>[a-z0-9]+)/?` | `AuditReportViewSet` | `latest` | `AuditReportSerializer` | `IsAdminUser` | ALL / view-specific | [internal] DRF format-suffix duplicate route |
| GET,POST | `/api/audit/reports\.(?P<format>[a-z0-9]+)/?` | `AuditReportViewSet` | `create,list` | `AuditReportSerializer` | `IsAdminUser` | ALL / view-specific | [internal] DRF format-suffix duplicate route |
| POST | `/api/auth/change-password/` | `change_password_view` | `custom` | `n/a` | `IsAuthenticated` | ALL / view-specific | `authApi.changePassword` (lib/api/auth.ts:153) |
| POST | `/api/auth/login/` | `CustomTokenObtainPairView` | `custom` | `CustomTokenObtainPairSerializer` | `n/a` | ALL / view-specific | `authApi.login` (lib/api/auth.ts:59) |
| POST | `/api/auth/logout/` | `logout_view` | `custom` | `n/a` | `IsAuthenticated` | ALL / view-specific | `authApi.logout` (lib/api/auth.ts:78) |
| POST | `/api/auth/password-reset/` | `password_reset_request_view` | `custom` | `n/a` | `AllowAny` | ALL / view-specific | `authApi.passwordReset` (lib/api/auth.ts:126) |
| POST | `/api/auth/password-reset/confirm/` | `password_reset_confirm_view` | `custom` | `n/a` | `AllowAny` | ALL / view-specific | `authApi.passwordResetConfirm` (lib/api/auth.ts:140) |
| GET | `/api/auth/profile/` | `user_profile_view` | `list/custom` | `n/a` | `IsAuthenticated` | OWN | `authApi.getCurrentUser` (lib/api/auth.ts:97) |
| PUT,PATCH | `/api/auth/profile/update/` | `update_profile_view` | `custom` | `n/a` | `IsAuthenticated` | OWN | `authApi.updateProfile` (lib/api/auth.ts:117) |
| POST | `/api/auth/refresh/` | `TokenRefreshView` | `custom` | `n/a` | `n/a` | ALL / view-specific | `authApi.refreshToken` (lib/api/auth.ts:106); `None` (lib/api/client.ts:66) |
| POST | `/api/auth/register/` | `register_view` | `custom` | `n/a` | `AllowAny` | ALL / view-specific | `authApi.register` (lib/api/auth.ts:67) |
| POST | `/api/bulk/assignment/` | `BulkAssignmentView` | `custom` | `n/a` | `IsAuthenticated` | ALL / view-specific | `bulkApi.assignment` (lib/api/bulk.ts:95) |
| POST | `/api/bulk/import-residents/` | `BulkResidentImportView` | `custom` | `n/a` | `IsAuthenticated` | ALL / view-specific | `bulkApi.importResidents` (lib/api/bulk.ts:83) |
| POST | `/api/bulk/import-supervisors/` | `BulkSupervisorImportView` | `custom` | `n/a` | `IsAuthenticated` | ALL / view-specific | `bulkApi.importSupervisors` (lib/api/bulk.ts:68) |
| POST | `/api/bulk/import-trainees/` | `BulkTraineeImportView` | `custom` | `n/a` | `IsAuthenticated` | ALL / view-specific | `bulkApi.importTrainees` (lib/api/bulk.ts:53) |
| POST | `/api/bulk/import/` | `BulkImportView` | `custom` | `n/a` | `IsAuthenticated` | ALL / view-specific | `bulkApi.import` (lib/api/bulk.ts:38) |
| POST | `/api/bulk/review/` | `BulkReviewView` | `custom` | `n/a` | `IsAuthenticated` | ALL / view-specific | `bulkApi.review` (lib/api/bulk.ts:103) |
| GET | `/api/certificates/my/` | `PGCertificatesListView` | `list/custom` | `n/a` | `IsAuthenticated, IsPGUser` | OWN | `certificatesApi.getMyCertificates` (lib/api/certificates.ts:22) |
| GET | `/api/certificates/my/<int:pk>/download/` | `PGCertificateDownloadView` | `retrieve/custom` | `n/a` | `IsAuthenticated, IsPGUser` | OWN | `certificatesApi.downloadCertificate` (lib/api/certificates.ts:45) |
| PATCH | `/api/logbook/<int:pk>/verify/` | `VerifyLogbookEntryView` | `update/destroy/custom` | `n/a` | `CanVerifyLogbookEntry` | SUPERVISEES \| ALL(admin) | `logbookApi.verify` (lib/api/logbook.ts:79) |
| GET,POST | `/api/logbook/my/` | `PGLogbookEntryListCreateView` | `list,create` | `n/a` | `IsAuthenticated, IsPGUser` | OWN | `logbookApi.getMyEntries` (lib/api/logbook.ts:90); `logbookApi.createMyEntry` (lib/api/logbook.ts:100) |
| PATCH | `/api/logbook/my/<int:pk>/` | `PGLogbookEntryDetailView` | `update/destroy/custom` | `n/a` | `IsAuthenticated, IsPGUser` | OWN | `logbookApi.updateMyEntry` (lib/api/logbook.ts:108) |
| POST | `/api/logbook/my/<int:pk>/submit/` | `PGLogbookEntrySubmitView` | `custom` | `n/a` | `IsAuthenticated, IsPGUser` | OWN | `logbookApi.submitMyEntry` (lib/api/logbook.ts:116) |
| GET | `/api/logbook/pending/` | `PendingLogbookEntriesView` | `list/custom` | `n/a` | `CanViewPendingLogbookQueue` | SUPERVISEES \| ALL(admin/utrmc read-only) | `logbookApi.getPending` (lib/api/logbook.ts:68) |
| GET | `/api/notifications/` | `NotificationListView` | `list/custom` | `NotificationSerializer` | `IsAuthenticated` | OWN | `notificationsApi.list` (lib/api/notifications.ts:30); `notificationsApi.getUnread` (lib/api/notifications.ts:39) |
| POST | `/api/notifications/mark-read/` | `NotificationMarkReadView` | `custom` | `n/a` | `IsAuthenticated` | OWN | `notificationsApi.markRead` (lib/api/notifications.ts:59) |
| GET,PATCH | `/api/notifications/preferences/` | `NotificationPreferenceView` | `custom` | `n/a` | `IsAuthenticated` | OWN | `notificationsApi.getPreferences` (lib/api/notifications.ts:69); `notificationsApi.updatePreferences` (lib/api/notifications.ts:77) |
| GET | `/api/notifications/unread-count/` | `NotificationUnreadCountView` | `list/custom` | `n/a` | `IsAuthenticated` | OWN | `notificationsApi.getUnreadCount` (lib/api/notifications.ts:50) |
| POST | `/api/reports/generate/` | `ReportGenerateView` | `custom` | `n/a` | `IsAuthenticated` | ALL / view-specific | `reportsApi.generate` (lib/api/reports.ts:48) |
| GET,POST | `/api/reports/scheduled/` | `ScheduledReportListCreateView` | `list,create` | `ScheduledReportSerializer` | `IsAuthenticated` | ALL / view-specific | `reportsApi.getScheduled` (lib/api/reports.ts:59); `reportsApi.schedule` (lib/api/reports.ts:67) |
| GET,PUT,PATCH | `/api/reports/scheduled/<int:pk>/` | `ScheduledReportDetailView` | `update/destroy/custom` | `ScheduledReportSerializer` | `IsAuthenticated` | ALL / view-specific | `reportsApi.getScheduledDetail` (lib/api/reports.ts:75) |
| GET | `/api/reports/templates/` | `ReportTemplateListView` | `list/custom` | `ReportTemplateSerializer` | `IsAuthenticated` | ALL / view-specific | `reportsApi.getTemplates` (lib/api/reports.ts:40) |
| PATCH | `/api/rotations/<int:pk>/utrmc-approve/` | `UTRMCRotationOverrideApproveView` | `update/destroy/custom` | `n/a` | `IsAuthenticated, IsUTRMCAdminUser, CanApproveRotationOverride` | ALL (utrmc_admin only) | [backend-only] no current Next.js consumer found by static scan |
| GET,POST | `/api/rotations/hospital-departments/` | `HospitalDepartmentViewSet` | `create,list` | `HospitalDepartmentSerializer` | `ReadAnyWriteUTRMCAdmin` | ALL read; utrmc_admin write | [future] canonical reference-data endpoint not yet consumed by Next.js UI |
| DELETE,GET,PATCH,PUT | `/api/rotations/hospital-departments/(?P<pk>[/.]+)/` | `HospitalDepartmentViewSet` | `destroy,partial_update,retrieve,update` | `HospitalDepartmentSerializer` | `ReadAnyWriteUTRMCAdmin` | ALL read; utrmc_admin write | [future] canonical reference-data endpoint not yet consumed by Next.js UI |
| DELETE,GET,PATCH,PUT | `/api/rotations/hospital-departments/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?` | `HospitalDepartmentViewSet` | `destroy,partial_update,retrieve,update` | `HospitalDepartmentSerializer` | `ReadAnyWriteUTRMCAdmin` | ALL read; utrmc_admin write | [internal] DRF format-suffix duplicate route |
| GET,POST | `/api/rotations/hospital-departments\.(?P<format>[a-z0-9]+)/?` | `HospitalDepartmentViewSet` | `create,list` | `HospitalDepartmentSerializer` | `ReadAnyWriteUTRMCAdmin` | ALL / view-specific | [internal] DRF format-suffix duplicate route |
| GET,POST | `/api/rotations/hospitals/` | `HospitalViewSet` | `create,list` | `HospitalSerializer` | `ReadAnyWriteAdminOrUTRMCAdmin` | ALL read; admin/utrmc_admin write | [future] canonical reference-data endpoint not yet consumed by Next.js UI |
| DELETE,GET,PATCH,PUT | `/api/rotations/hospitals/(?P<pk>[/.]+)/` | `HospitalViewSet` | `destroy,partial_update,retrieve,update` | `HospitalSerializer` | `ReadAnyWriteAdminOrUTRMCAdmin` | ALL read; admin/utrmc_admin write | [future] canonical reference-data endpoint not yet consumed by Next.js UI |
| DELETE,GET,PATCH,PUT | `/api/rotations/hospitals/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?` | `HospitalViewSet` | `destroy,partial_update,retrieve,update` | `HospitalSerializer` | `ReadAnyWriteAdminOrUTRMCAdmin` | ALL read; admin/utrmc_admin write | [internal] DRF format-suffix duplicate route |
| GET,POST | `/api/rotations/hospitals\.(?P<format>[a-z0-9]+)/?` | `HospitalViewSet` | `create,list` | `HospitalSerializer` | `ReadAnyWriteAdminOrUTRMCAdmin` | ALL / view-specific | [internal] DRF format-suffix duplicate route |
| GET | `/api/rotations/my/` | `PGMyRotationsListView` | `list/custom` | `n/a` | `IsAuthenticated, IsPGUser` | OWN | `rotationsApi.getMyRotations` (lib/api/rotations.ts:25) |
| GET | `/api/rotations/my/<int:pk>/` | `PGMyRotationDetailView` | `retrieve/custom` | `n/a` | `IsAuthenticated, IsPGUser` | OWN | `rotationsApi.getMyRotation` (lib/api/rotations.ts:33) |
| GET | `/api/search/` | `GlobalSearchView` | `list/custom` | `n/a` | `IsAuthenticated` | ALL / view-specific | `searchApi.search` (lib/api/search.ts:34) |
| GET | `/api/search/history/` | `SearchHistoryView` | `list/custom` | `n/a` | `IsAuthenticated` | ALL / view-specific | `searchApi.getHistory` (lib/api/search.ts:44) |
| GET | `/api/search/suggestions/` | `SearchSuggestionsView` | `list/custom` | `n/a` | `IsAuthenticated` | ALL / view-specific | `searchApi.getSuggestions` (lib/api/search.ts:52) |
| GET | `/api/users/assigned-pgs/` | `SupervisorAssignedPGsView` | `list/custom` | `n/a` | `IsAuthenticated, IsSupervisor` | ALL / view-specific | `usersApi.getAssignedPGs` (lib/api/users.ts:15) |
| GET | `/cases/api/diagnoses/` | `sims.cases.views` | `list/custom` | `n/a` | `n/a` | ALL / view-specific | [backend-only] legacy Django template/AJAX endpoint |
| GET | `/cases/api/procedures/` | `sims.cases.views` | `list/custom` | `n/a` | `n/a` | ALL / view-specific | [backend-only] legacy Django template/AJAX endpoint |
| GET | `/certificates/api/<int:pk>/verify/` | `sims.certificates.views` | `retrieve/custom` | `n/a` | `n/a` | ALL / view-specific | [backend-only] legacy Django template/AJAX endpoint |
| GET | `/certificates/api/quick-stats/` | `sims.certificates.views` | `list/custom` | `n/a` | `n/a` | ALL / view-specific | [backend-only] legacy Django template/AJAX endpoint |
| GET | `/certificates/api/stats/` | `sims.certificates.views` | `list/custom` | `n/a` | `n/a` | ALL / view-specific | [backend-only] legacy Django template/AJAX endpoint |
| GET | `/certificates/api/update-statistics/` | `sims.certificates.views` | `list/custom` | `n/a` | `n/a` | ALL / view-specific | [backend-only] legacy Django template/AJAX endpoint |
| GET | `/logbook/api/entry/<int:entry_id>/complexity/` | `sims.logbook.views` | `retrieve/custom` | `n/a` | `n/a` | ALL / view-specific | [backend-only] legacy Django template/AJAX endpoint |
| GET | `/logbook/api/stats/` | `sims.logbook.views` | `list/custom` | `n/a` | `n/a` | ALL / view-specific | [backend-only] legacy Django template/AJAX endpoint |
| GET | `/logbook/api/template/<int:template_id>/preview/` | `sims.logbook.views` | `retrieve/custom` | `n/a` | `n/a` | ALL / view-specific | [backend-only] legacy Django template/AJAX endpoint |
| GET | `/logbook/api/update-statistics/` | `sims.logbook.views` | `list/custom` | `n/a` | `n/a` | ALL / view-specific | [backend-only] legacy Django template/AJAX endpoint |
| GET,POST | `/results/api/exams/` | `ExamViewSet` | `create,list` | `ExamSerializer` | `IsAuthenticated` | ALL / view-specific | `resultsApi.list` (lib/api/results.ts:54); `resultsApi.create` (lib/api/results.ts:62) |
| DELETE,GET,PATCH,PUT | `/results/api/exams/(?P<pk>[/.]+)/` | `ExamViewSet` | `destroy,partial_update,retrieve,update` | `ExamSerializer` | `IsAuthenticated` | ALL / view-specific | `resultsApi.delete` (lib/api/results.ts:70); `resultsApi.get` (lib/api/results.ts:58); `resultsApi.update` (lib/api/results.ts:66) |
| GET | `/results/api/exams/(?P<pk>[/.]+)/scores/` | `ExamViewSet` | `scores` | `ExamSerializer` | `IsAuthenticated` | ALL / view-specific | `resultsApi.getScores` (lib/api/results.ts:73) |
| GET | `/results/api/exams/(?P<pk>[/.]+)/scores\.(?P<format>[a-z0-9]+)/?` | `ExamViewSet` | `scores` | `ExamSerializer` | `IsAuthenticated` | ALL / view-specific | [internal] DRF format-suffix duplicate route |
| GET | `/results/api/exams/(?P<pk>[/.]+)/statistics/` | `ExamViewSet` | `statistics` | `ExamSerializer` | `IsAuthenticated` | ALL / view-specific | `resultsApi.getStatistics` (lib/api/results.ts:77) |
| GET | `/results/api/exams/(?P<pk>[/.]+)/statistics\.(?P<format>[a-z0-9]+)/?` | `ExamViewSet` | `statistics` | `ExamSerializer` | `IsAuthenticated` | ALL / view-specific | [internal] DRF format-suffix duplicate route |
| DELETE,GET,PATCH,PUT | `/results/api/exams/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?` | `ExamViewSet` | `destroy,partial_update,retrieve,update` | `ExamSerializer` | `IsAuthenticated` | ALL / view-specific | [internal] DRF format-suffix duplicate route |
| GET,POST | `/results/api/exams\.(?P<format>[a-z0-9]+)/?` | `ExamViewSet` | `create,list` | `ExamSerializer` | `IsAuthenticated` | ALL / view-specific | [internal] DRF format-suffix duplicate route |
| GET,POST | `/results/api/scores/` | `ScoreViewSet` | `create,list` | `ScoreSerializer` | `IsAuthenticated` | ALL / view-specific | `resultsApi.list` (lib/api/results.ts:87); `resultsApi.create` (lib/api/results.ts:95) |
| DELETE,GET,PATCH,PUT | `/results/api/scores/(?P<pk>[/.]+)/` | `ScoreViewSet` | `destroy,partial_update,retrieve,update` | `ScoreSerializer` | `IsAuthenticated` | ALL / view-specific | `resultsApi.delete` (lib/api/results.ts:103); `resultsApi.get` (lib/api/results.ts:91); `resultsApi.update` (lib/api/results.ts:99) |
| DELETE,GET,PATCH,PUT | `/results/api/scores/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?` | `ScoreViewSet` | `destroy,partial_update,retrieve,update` | `ScoreSerializer` | `IsAuthenticated` | ALL / view-specific | [internal] DRF format-suffix duplicate route |
| GET | `/results/api/scores/my_scores/` | `ScoreViewSet` | `my_scores` | `ScoreSerializer` | `IsAuthenticated` | OWN | `resultsApi.getMyScores` (lib/api/results.ts:106) |
| GET | `/results/api/scores/my_scores\.(?P<format>[a-z0-9]+)/?` | `ScoreViewSet` | `my_scores` | `ScoreSerializer` | `IsAuthenticated` | ALL / view-specific | [internal] DRF format-suffix duplicate route |
| GET,POST | `/results/api/scores\.(?P<format>[a-z0-9]+)/?` | `ScoreViewSet` | `create,list` | `ScoreSerializer` | `IsAuthenticated` | ALL / view-specific | [internal] DRF format-suffix duplicate route |
| GET | `/rotations/api/calendar/` | `sims.rotations.views` | `list/custom` | `n/a` | `n/a` | ALL / view-specific | [backend-only] legacy Django template/AJAX endpoint |
| GET | `/rotations/api/departments/<int:hospital_id>/` | `sims.rotations.views` | `retrieve/custom` | `n/a` | `n/a` | ALL / view-specific | [backend-only] legacy Django template/AJAX endpoint |
| GET | `/rotations/api/quick-stats/` | `sims.rotations.views` | `list/custom` | `n/a` | `n/a` | ALL / view-specific | [backend-only] legacy Django template/AJAX endpoint |
| GET | `/rotations/api/stats/` | `sims.rotations.views` | `list/custom` | `n/a` | `n/a` | ALL / view-specific | [backend-only] legacy Django template/AJAX endpoint |
| GET | `/users/api/admin/stats/` | `sims.users.views` | `list/custom` | `n/a` | `n/a` | ALL / view-specific | [backend-only] legacy Django template/AJAX endpoint |
| GET | `/users/api/stats/` | `sims.users.views` | `list/custom` | `n/a` | `n/a` | ALL / view-specific | [backend-only] legacy Django template/AJAX endpoint |
| GET | `/users/api/supervisors/specialty/<str:specialty>/` | `sims.users.views` | `retrieve/custom` | `n/a` | `n/a` | ALL / view-specific | [backend-only] legacy Django template/AJAX endpoint |
| GET | `/users/api/user-performance/` | `sims.users.views` | `list/custom` | `n/a` | `n/a` | ALL / view-specific | [backend-only] legacy Django template/AJAX endpoint |
| GET | `/users/api/user-statistics/` | `sims.users.views` | `list/custom` | `n/a` | `n/a` | ALL / view-specific | [backend-only] legacy Django template/AJAX endpoint |
| GET | `/users/api/user/<int:pk>/stats/` | `sims.users.views` | `retrieve/custom` | `n/a` | `n/a` | ALL / view-specific | [backend-only] legacy Django template/AJAX endpoint |
| GET | `/users/api/users/search/` | `sims.users.views` | `list/custom` | `n/a` | `n/a` | ALL / view-specific | [backend-only] legacy Django template/AJAX endpoint |

## B) Frontend Inventory
Notes:
- Token/cookie application for `apiClient` calls is centralized in `frontend/lib/api/client.ts` and auth cookie mirroring in `frontend/store/authStore.ts` + `frontend/lib/auth/cookies.ts`.
- Adapter/normalizer column identifies where payload alias/shape normalization occurs; non-core endpoints often use direct responses.

| Caller (file:function) | Method | URL Path Template | Token/Cookie Application | Adapter/Normalizer | Pages/Components invoking | Backend Match |
|---|---|---|---|---|---|---|
| lib/api/academics.ts:48 academicsApi.list | GET | `'/academics/api/departments/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `GET,POST /academics/api/departments/` |
| lib/api/academics.ts:52 academicsApi.get | GET | ``/academics/api/departments/${id}/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `DELETE,GET,PATCH,PUT /academics/api/departments/(?P<pk>[/.]+)/` |
| lib/api/academics.ts:56 academicsApi.create | POST | `'/academics/api/departments/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `GET,POST /academics/api/departments/` |
| lib/api/academics.ts:60 academicsApi.update | PUT | ``/academics/api/departments/${id}/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `DELETE,GET,PATCH,PUT /academics/api/departments/(?P<pk>[/.]+)/` |
| lib/api/academics.ts:64 academicsApi.delete | DELETE | ``/academics/api/departments/${id}/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `DELETE,GET,PATCH,PUT /academics/api/departments/(?P<pk>[/.]+)/` |
| lib/api/academics.ts:73 academicsApi.list | GET | `'/academics/api/batches/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `GET,POST /academics/api/batches/` |
| lib/api/academics.ts:77 academicsApi.get | GET | ``/academics/api/batches/${id}/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `DELETE,GET,PATCH,PUT /academics/api/batches/(?P<pk>[/.]+)/` |
| lib/api/academics.ts:81 academicsApi.create | POST | `'/academics/api/batches/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `GET,POST /academics/api/batches/` |
| lib/api/academics.ts:85 academicsApi.update | PUT | ``/academics/api/batches/${id}/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `DELETE,GET,PATCH,PUT /academics/api/batches/(?P<pk>[/.]+)/` |
| lib/api/academics.ts:89 academicsApi.delete | DELETE | ``/academics/api/batches/${id}/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `DELETE,GET,PATCH,PUT /academics/api/batches/(?P<pk>[/.]+)/` |
| lib/api/academics.ts:92 academicsApi.getStudents | GET | ``/academics/api/batches/${id}/students/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `GET /academics/api/batches/(?P<pk>[/.]+)/students/` |
| lib/api/academics.ts:102 academicsApi.list | GET | `'/academics/api/students/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `GET,POST /academics/api/students/` |
| lib/api/academics.ts:106 academicsApi.get | GET | ``/academics/api/students/${id}/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `DELETE,GET,PATCH,PUT /academics/api/students/(?P<pk>[/.]+)/` |
| lib/api/academics.ts:110 academicsApi.create | POST | `'/academics/api/students/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `GET,POST /academics/api/students/` |
| lib/api/academics.ts:114 academicsApi.update | PUT | ``/academics/api/students/${id}/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `DELETE,GET,PATCH,PUT /academics/api/students/(?P<pk>[/.]+)/` |
| lib/api/academics.ts:118 academicsApi.delete | DELETE | ``/academics/api/students/${id}/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `DELETE,GET,PATCH,PUT /academics/api/students/(?P<pk>[/.]+)/` |
| lib/api/academics.ts:121 academicsApi.updateStatus | POST | ``/academics/api/students/${id}/update_status/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `POST /academics/api/students/(?P<pk>[/.]+)/update_status/` |
| lib/api/analytics.ts:42 analyticsApi.getDashboardOverview | GET | `'/api/analytics/dashboard/overview/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/dashboard/admin/page.tsx:29` | `GET /api/analytics/dashboard/overview/` |
| lib/api/analytics.ts:50 analyticsApi.getTrends | GET | `'/api/analytics/dashboard/trends/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/dashboard/admin/analytics/page.tsx:30` | `GET /api/analytics/dashboard/trends/` |
| lib/api/analytics.ts:58 analyticsApi.getCompliance | GET | `'/api/analytics/dashboard/compliance/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/dashboard/admin/analytics/page.tsx:38` | `GET /api/analytics/dashboard/compliance/` |
| lib/api/analytics.ts:66 analyticsApi.getPerformance | GET | `'/api/analytics/performance/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/dashboard/admin/analytics/page.tsx:34` | `GET /api/analytics/performance/` |
| lib/api/attendance.ts:38 attendanceApi.getSummary | GET | `'/api/attendance/summary/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/dashboard/pg/page.tsx:62` | `GET /api/attendance/summary/` |
| lib/api/attendance.ts:49 attendanceApi.bulkUpload | POST | `'/api/attendance/upload/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `POST /api/attendance/upload/` |
| lib/api/audit.ts:31 auditApi.getActivityLogs | GET | `'/api/audit/activity/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/dashboard/admin/audit-logs/page.tsx:41` | `GET /api/audit/activity/` |
| lib/api/audit.ts:39 auditApi.getReports | GET | `'/api/audit/reports/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `GET,POST /api/audit/reports/` |
| lib/api/audit.ts:47 auditApi.createReport | POST | `'/api/audit/reports/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `GET,POST /api/audit/reports/` |
| lib/api/auth.ts:59 authApi.login | POST | `'/api/auth/login/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/login/page.tsx:35` | `POST /api/auth/login/` |
| lib/api/auth.ts:67 authApi.register | POST | `'/api/auth/register/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/register/page.tsx:120` | `POST /api/auth/register/` |
| lib/api/auth.ts:78 authApi.logout | POST | `'/api/auth/logout/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `components/layout/DashboardLayout.tsx:13` | `POST /api/auth/logout/` |
| lib/api/auth.ts:97 authApi.getCurrentUser | GET | `'/api/auth/profile/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/dashboard/pg/page.tsx:60` | `GET /api/auth/profile/` |
| lib/api/auth.ts:106 authApi.refreshToken | POST | `'/api/auth/refresh/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `POST /api/auth/refresh/` |
| lib/api/auth.ts:117 authApi.updateProfile | PATCH | `'/api/auth/profile/update/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `PUT,PATCH /api/auth/profile/update/` |
| lib/api/auth.ts:126 authApi.passwordReset | POST | `'/api/auth/password-reset/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `POST /api/auth/password-reset/` |
| lib/api/auth.ts:140 authApi.passwordResetConfirm | POST | `'/api/auth/password-reset/confirm/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `POST /api/auth/password-reset/confirm/` |
| lib/api/auth.ts:153 authApi.changePassword | POST | `'/api/auth/change-password/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `POST /api/auth/change-password/` |
| lib/api/bulk.ts:38 bulkApi.import | POST | `'/api/bulk/import/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/dashboard/admin/bulk-import/page.tsx:54` | `POST /api/bulk/import/` |
| lib/api/bulk.ts:53 bulkApi.importTrainees | POST | `'/api/bulk/import-trainees/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/dashboard/admin/bulk-import/page.tsx:45` | `POST /api/bulk/import-trainees/` |
| lib/api/bulk.ts:68 bulkApi.importSupervisors | POST | `'/api/bulk/import-supervisors/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/dashboard/admin/bulk-import/page.tsx:48` | `POST /api/bulk/import-supervisors/` |
| lib/api/bulk.ts:83 bulkApi.importResidents | POST | `'/api/bulk/import-residents/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/dashboard/admin/bulk-import/page.tsx:51` | `POST /api/bulk/import-residents/` |
| lib/api/bulk.ts:95 bulkApi.assignment | POST | `'/api/bulk/assignment/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `POST /api/bulk/assignment/` |
| lib/api/bulk.ts:103 bulkApi.review | POST | `'/api/bulk/review/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `POST /api/bulk/review/` |
| lib/api/certificates.ts:22 certificatesApi.getMyCertificates | GET | `'/api/certificates/my/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/dashboard/pg/certificates/page.tsx:49` | `GET /api/certificates/my/` |
| lib/api/certificates.ts:45 certificatesApi.downloadCertificate | GET | `(dynamic via certificatesApi.getCertificateDownloadUrl)` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/dashboard/pg/certificates/page.tsx:79` | `GET /api/certificates/my/<int:pk>/download/` |
| lib/api/client.ts:66 (interceptor/internal) | POST | ``${API_URL}/api/auth/refresh/`` | axios direct call in apiClient interceptor (frontend/lib/api/client.ts) | `(none/direct)` | (no current page call found) | `POST /api/auth/refresh/` |
| lib/api/logbook.ts:68 logbookApi.getPending | GET | `'/api/logbook/pending/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `frontend/lib/adapters/logbookAdapter.ts` | `app/dashboard/supervisor/logbooks/page.tsx:44`; `app/dashboard/supervisor/page.tsx:45` | `GET /api/logbook/pending/` |
| lib/api/logbook.ts:79 logbookApi.verify | PATCH | ``/api/logbook/${id}/verify/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `frontend/lib/adapters/logbookAdapter.ts` | `app/dashboard/supervisor/logbooks/page.tsx:67`; `app/dashboard/supervisor/page.tsx:71` | `PATCH /api/logbook/<int:pk>/verify/` |
| lib/api/logbook.ts:90 logbookApi.getMyEntries | GET | `'/api/logbook/my/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `frontend/lib/adapters/logbookAdapter.ts` | `app/dashboard/pg/logbook/page.tsx:40` | `GET,POST /api/logbook/my/` |
| lib/api/logbook.ts:100 logbookApi.createMyEntry | POST | `'/api/logbook/my/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `frontend/lib/adapters/logbookAdapter.ts` | `app/dashboard/pg/logbook/page.tsx:90` | `GET,POST /api/logbook/my/` |
| lib/api/logbook.ts:108 logbookApi.updateMyEntry | PATCH | ``/api/logbook/my/${id}/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `frontend/lib/adapters/logbookAdapter.ts` | `app/dashboard/pg/logbook/page.tsx:87` | `PATCH /api/logbook/my/<int:pk>/` |
| lib/api/logbook.ts:116 logbookApi.submitMyEntry | POST | ``/api/logbook/my/${id}/submit/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `frontend/lib/adapters/logbookAdapter.ts` | `app/dashboard/pg/logbook/page.tsx:112` | `POST /api/logbook/my/<int:pk>/submit/` |
| lib/api/notifications.ts:30 notificationsApi.list | GET | `'/api/notifications/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/dashboard/pg/notifications/page.tsx:33` | `GET /api/notifications/` |
| lib/api/notifications.ts:39 notificationsApi.getUnread | GET | `'/api/notifications/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/dashboard/pg/notifications/page.tsx:36` | `GET /api/notifications/` |
| lib/api/notifications.ts:50 notificationsApi.getUnreadCount | GET | `'/api/notifications/unread-count/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/dashboard/admin/page.tsx:30`; `app/dashboard/pg/notifications/page.tsx:38`; `app/dashboard/pg/page.tsx:61`; `app/dashboard/supervisor/page.tsx:46` | `GET /api/notifications/unread-count/` |
| lib/api/notifications.ts:59 notificationsApi.markRead | POST | ``/api/notifications/mark-read/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/dashboard/pg/notifications/page.tsx:67`; `app/dashboard/pg/notifications/page.tsx:83` | `POST /api/notifications/mark-read/` |
| lib/api/notifications.ts:69 notificationsApi.getPreferences | GET | `'/api/notifications/preferences/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `GET,PATCH /api/notifications/preferences/` |
| lib/api/notifications.ts:77 notificationsApi.updatePreferences | PATCH | `'/api/notifications/preferences/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `GET,PATCH /api/notifications/preferences/` |
| lib/api/reports.ts:40 reportsApi.getTemplates | GET | `'/api/reports/templates/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `GET /api/reports/templates/` |
| lib/api/reports.ts:48 reportsApi.generate | POST | `'/api/reports/generate/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `POST /api/reports/generate/` |
| lib/api/reports.ts:59 reportsApi.getScheduled | GET | `'/api/reports/scheduled/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `GET,POST /api/reports/scheduled/` |
| lib/api/reports.ts:67 reportsApi.schedule | POST | `'/api/reports/scheduled/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `GET,POST /api/reports/scheduled/` |
| lib/api/reports.ts:75 reportsApi.getScheduledDetail | GET | ``/api/reports/scheduled/${id}/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `GET,PUT,PATCH /api/reports/scheduled/<int:pk>/` |
| lib/api/results.ts:54 resultsApi.list | GET | `'/results/api/exams/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `GET,POST /results/api/exams/` |
| lib/api/results.ts:58 resultsApi.get | GET | ``/results/api/exams/${id}/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `DELETE,GET,PATCH,PUT /results/api/exams/(?P<pk>[/.]+)/` |
| lib/api/results.ts:62 resultsApi.create | POST | `'/results/api/exams/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `GET,POST /results/api/exams/` |
| lib/api/results.ts:66 resultsApi.update | PUT | ``/results/api/exams/${id}/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `DELETE,GET,PATCH,PUT /results/api/exams/(?P<pk>[/.]+)/` |
| lib/api/results.ts:70 resultsApi.delete | DELETE | ``/results/api/exams/${id}/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `DELETE,GET,PATCH,PUT /results/api/exams/(?P<pk>[/.]+)/` |
| lib/api/results.ts:73 resultsApi.getScores | GET | ``/results/api/exams/${id}/scores/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `GET /results/api/exams/(?P<pk>[/.]+)/scores/` |
| lib/api/results.ts:77 resultsApi.getStatistics | GET | ``/results/api/exams/${id}/statistics/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `GET /results/api/exams/(?P<pk>[/.]+)/statistics/` |
| lib/api/results.ts:87 resultsApi.list | GET | `'/results/api/scores/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `GET,POST /results/api/scores/` |
| lib/api/results.ts:91 resultsApi.get | GET | ``/results/api/scores/${id}/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `DELETE,GET,PATCH,PUT /results/api/scores/(?P<pk>[/.]+)/` |
| lib/api/results.ts:95 resultsApi.create | POST | `'/results/api/scores/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `GET,POST /results/api/scores/` |
| lib/api/results.ts:99 resultsApi.update | PUT | ``/results/api/scores/${id}/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `DELETE,GET,PATCH,PUT /results/api/scores/(?P<pk>[/.]+)/` |
| lib/api/results.ts:103 resultsApi.delete | DELETE | ``/results/api/scores/${id}/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `DELETE,GET,PATCH,PUT /results/api/scores/(?P<pk>[/.]+)/` |
| lib/api/results.ts:106 resultsApi.getMyScores | GET | `'/results/api/scores/my_scores/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | (no current page call found) | `GET /results/api/scores/my_scores/` |
| lib/api/rotations.ts:25 rotationsApi.getMyRotations | GET | `'/api/rotations/my/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `frontend/lib/adapters/rotationAdapter.ts` | `app/dashboard/pg/rotations/page.tsx:95` | `GET /api/rotations/my/` |
| lib/api/rotations.ts:33 rotationsApi.getMyRotation | GET | ``/api/rotations/my/${id}/`` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `frontend/lib/adapters/rotationAdapter.ts` | (no current page call found) | `GET /api/rotations/my/<int:pk>/` |
| lib/api/search.ts:34 searchApi.search | GET | `'/api/search/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/dashboard/search/page.tsx:39` | `GET /api/search/` |
| lib/api/search.ts:44 searchApi.getHistory | GET | `'/api/search/history/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/dashboard/search/page.tsx:66` | `GET /api/search/history/` |
| lib/api/search.ts:52 searchApi.getSuggestions | GET | `'/api/search/suggestions/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/dashboard/search/page.tsx:40` | `GET /api/search/suggestions/` |
| lib/api/users.ts:15 usersApi.getAssignedPGs | GET | `'/api/users/assigned-pgs/'` | apiClient auth header via frontend/lib/api/client.ts; middleware cookies mirrored via auth store/cookies | `(none/direct)` | `app/dashboard/supervisor/pgs/page.tsx:24` | `GET /api/users/assigned-pgs/` |

Middleware gating notes (static evidence):
- Gated routes: `/dashboard/:path*` via matcher in `frontend/middleware.ts:91`.
- Cookies read: `pgsims_access_token`, `pgsims_user_role`, `pgsims_access_exp` in `frontend/middleware.ts:59`, `frontend/middleware.ts:68`, `frontend/middleware.ts:69`.
- Invalid/expired cookie behavior: redirect `/login` + clear cookies in `frontend/middleware.ts:73`-`frontend/middleware.ts:79`.
- Admin fallback access is allowed in middleware for `/dashboard/pg/*`, `/dashboard/supervisor/*`, and `/dashboard/utrmc/*`: `frontend/middleware.ts:41`-`frontend/middleware.ts:48`.
- Client-side `ProtectedRoute` also permits admin as fallback for role-scoped pages: `frontend/components/auth/ProtectedRoute.tsx:17`-`frontend/components/auth/ProtectedRoute.tsx:18`, `frontend/components/auth/ProtectedRoute.tsx:29`-`frontend/components/auth/ProtectedRoute.tsx:31`.

## C) Bidirectional Cross-Link Map
### C1. Backend Endpoint -> Frontend Consumer(s)

| Backend Endpoint | Frontend Consumers | Status |
|---|---|---|
| `GET /academics/api/batches/; POST /academics/api/batches/` | `academicsApi.list` (lib/api/academics.ts:73); `academicsApi.create` (lib/api/academics.ts:81) | USED |
| `DELETE /academics/api/batches/(?P<pk>[/.]+)/; GET /academics/api/batches/(?P<pk>[/.]+)/; PATCH /academics/api/batches/(?P<pk>[/.]+)/; PUT /academics/api/batches/(?P<pk>[/.]+)/` | `academicsApi.delete` (lib/api/academics.ts:89); `academicsApi.get` (lib/api/academics.ts:77); `academicsApi.update` (lib/api/academics.ts:85) | USED |
| `GET /academics/api/batches/(?P<pk>[/.]+)/students/` | `academicsApi.getStudents` (lib/api/academics.ts:92) | USED |
| `GET /academics/api/batches/(?P<pk>[/.]+)/students\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `DELETE /academics/api/batches/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?; GET /academics/api/batches/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?; PATCH /academics/api/batches/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?; PUT /academics/api/batches/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `GET /academics/api/batches\.(?P<format>[a-z0-9]+)/?; POST /academics/api/batches\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `GET /academics/api/departments/; POST /academics/api/departments/` | `academicsApi.list` (lib/api/academics.ts:48); `academicsApi.create` (lib/api/academics.ts:56) | USED |
| `DELETE /academics/api/departments/(?P<pk>[/.]+)/; GET /academics/api/departments/(?P<pk>[/.]+)/; PATCH /academics/api/departments/(?P<pk>[/.]+)/; PUT /academics/api/departments/(?P<pk>[/.]+)/` | `academicsApi.delete` (lib/api/academics.ts:64); `academicsApi.get` (lib/api/academics.ts:52); `academicsApi.update` (lib/api/academics.ts:60) | USED |
| `DELETE /academics/api/departments/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?; GET /academics/api/departments/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?; PATCH /academics/api/departments/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?; PUT /academics/api/departments/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `GET /academics/api/departments\.(?P<format>[a-z0-9]+)/?; POST /academics/api/departments\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `GET /academics/api/students/; POST /academics/api/students/` | `academicsApi.list` (lib/api/academics.ts:102); `academicsApi.create` (lib/api/academics.ts:110) | USED |
| `DELETE /academics/api/students/(?P<pk>[/.]+)/; GET /academics/api/students/(?P<pk>[/.]+)/; PATCH /academics/api/students/(?P<pk>[/.]+)/; PUT /academics/api/students/(?P<pk>[/.]+)/` | `academicsApi.delete` (lib/api/academics.ts:118); `academicsApi.get` (lib/api/academics.ts:106); `academicsApi.update` (lib/api/academics.ts:114) | USED |
| `POST /academics/api/students/(?P<pk>[/.]+)/update_status/` | `academicsApi.updateStatus` (lib/api/academics.ts:121) | USED |
| `POST /academics/api/students/(?P<pk>[/.]+)/update_status\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `DELETE /academics/api/students/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?; GET /academics/api/students/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?; PATCH /academics/api/students/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?; PUT /academics/api/students/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `GET /academics/api/students\.(?P<format>[a-z0-9]+)/?; POST /academics/api/students\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `GET /api/analytics/comparative/` | - | [backend-only] no current Next.js consumer found by static scan |
| `GET /api/analytics/dashboard/compliance/` | `analyticsApi.getCompliance` (lib/api/analytics.ts:58) | USED |
| `GET /api/analytics/dashboard/overview/` | `analyticsApi.getDashboardOverview` (lib/api/analytics.ts:42) | USED |
| `GET /api/analytics/dashboard/trends/` | `analyticsApi.getTrends` (lib/api/analytics.ts:50) | USED |
| `GET /api/analytics/performance/` | `analyticsApi.getPerformance` (lib/api/analytics.ts:66) | USED |
| `GET /api/analytics/trends/` | - | [backend-only] no current Next.js consumer found by static scan |
| `GET /api/attendance/summary/` | `attendanceApi.getSummary` (lib/api/attendance.ts:38) | USED |
| `POST /api/attendance/upload/` | `attendanceApi.bulkUpload` (lib/api/attendance.ts:49) | USED |
| `GET /api/audit/activity/` | `auditApi.getActivityLogs` (lib/api/audit.ts:31) | USED |
| `GET /api/audit/activity/(?P<pk>[/.]+)/` | - | [admin-only/system-only] exposed for admin operations; current pages may use subset only |
| `GET /api/audit/activity/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `GET /api/audit/activity/export/` | - | [admin-only/system-only] exposed for admin operations; current pages may use subset only |
| `GET /api/audit/activity/export\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `GET /api/audit/activity\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `GET /api/audit/reports/; POST /api/audit/reports/` | `auditApi.getReports` (lib/api/audit.ts:39); `auditApi.createReport` (lib/api/audit.ts:47) | USED |
| `GET /api/audit/reports/latest/` | - | [admin-only/system-only] exposed for admin operations; current pages may use subset only |
| `GET /api/audit/reports/latest\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `GET /api/audit/reports\.(?P<format>[a-z0-9]+)/?; POST /api/audit/reports\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `POST /api/auth/change-password/` | `authApi.changePassword` (lib/api/auth.ts:153) | USED |
| `POST /api/auth/login/` | `authApi.login` (lib/api/auth.ts:59) | USED |
| `POST /api/auth/logout/` | `authApi.logout` (lib/api/auth.ts:78) | USED |
| `POST /api/auth/password-reset/` | `authApi.passwordReset` (lib/api/auth.ts:126) | USED |
| `POST /api/auth/password-reset/confirm/` | `authApi.passwordResetConfirm` (lib/api/auth.ts:140) | USED |
| `GET /api/auth/profile/` | `authApi.getCurrentUser` (lib/api/auth.ts:97) | USED |
| `PUT /api/auth/profile/update/; PATCH /api/auth/profile/update/` | `authApi.updateProfile` (lib/api/auth.ts:117) | USED |
| `POST /api/auth/refresh/` | `authApi.refreshToken` (lib/api/auth.ts:106); `None` (lib/api/client.ts:66) | USED |
| `POST /api/auth/register/` | `authApi.register` (lib/api/auth.ts:67) | USED |
| `POST /api/bulk/assignment/` | `bulkApi.assignment` (lib/api/bulk.ts:95) | USED |
| `POST /api/bulk/import-residents/` | `bulkApi.importResidents` (lib/api/bulk.ts:83) | USED |
| `POST /api/bulk/import-supervisors/` | `bulkApi.importSupervisors` (lib/api/bulk.ts:68) | USED |
| `POST /api/bulk/import-trainees/` | `bulkApi.importTrainees` (lib/api/bulk.ts:53) | USED |
| `POST /api/bulk/import/` | `bulkApi.import` (lib/api/bulk.ts:38) | USED |
| `POST /api/bulk/review/` | `bulkApi.review` (lib/api/bulk.ts:103) | USED |
| `GET /api/certificates/my/` | `certificatesApi.getMyCertificates` (lib/api/certificates.ts:22) | USED |
| `GET /api/certificates/my/<int:pk>/download/` | `certificatesApi.downloadCertificate` (lib/api/certificates.ts:45) | USED |
| `PATCH /api/logbook/<int:pk>/verify/` | `logbookApi.verify` (lib/api/logbook.ts:79) | USED |
| `GET /api/logbook/my/; POST /api/logbook/my/` | `logbookApi.getMyEntries` (lib/api/logbook.ts:90); `logbookApi.createMyEntry` (lib/api/logbook.ts:100) | USED |
| `PATCH /api/logbook/my/<int:pk>/` | `logbookApi.updateMyEntry` (lib/api/logbook.ts:108) | USED |
| `POST /api/logbook/my/<int:pk>/submit/` | `logbookApi.submitMyEntry` (lib/api/logbook.ts:116) | USED |
| `GET /api/logbook/pending/` | `logbookApi.getPending` (lib/api/logbook.ts:68) | USED |
| `GET /api/notifications/` | `notificationsApi.list` (lib/api/notifications.ts:30); `notificationsApi.getUnread` (lib/api/notifications.ts:39) | USED |
| `POST /api/notifications/mark-read/` | `notificationsApi.markRead` (lib/api/notifications.ts:59) | USED |
| `GET /api/notifications/preferences/; PATCH /api/notifications/preferences/` | `notificationsApi.getPreferences` (lib/api/notifications.ts:69); `notificationsApi.updatePreferences` (lib/api/notifications.ts:77) | USED |
| `GET /api/notifications/unread-count/` | `notificationsApi.getUnreadCount` (lib/api/notifications.ts:50) | USED |
| `POST /api/reports/generate/` | `reportsApi.generate` (lib/api/reports.ts:48) | USED |
| `GET /api/reports/scheduled/; POST /api/reports/scheduled/` | `reportsApi.getScheduled` (lib/api/reports.ts:59); `reportsApi.schedule` (lib/api/reports.ts:67) | USED |
| `GET /api/reports/scheduled/<int:pk>/; PUT /api/reports/scheduled/<int:pk>/; PATCH /api/reports/scheduled/<int:pk>/` | `reportsApi.getScheduledDetail` (lib/api/reports.ts:75) | USED |
| `GET /api/reports/templates/` | `reportsApi.getTemplates` (lib/api/reports.ts:40) | USED |
| `PATCH /api/rotations/<int:pk>/utrmc-approve/` | - | [backend-only] no current Next.js consumer found by static scan |
| `GET /api/rotations/hospital-departments/; POST /api/rotations/hospital-departments/` | - | [future] canonical reference-data endpoint not yet consumed by Next.js UI |
| `DELETE /api/rotations/hospital-departments/(?P<pk>[/.]+)/; GET /api/rotations/hospital-departments/(?P<pk>[/.]+)/; PATCH /api/rotations/hospital-departments/(?P<pk>[/.]+)/; PUT /api/rotations/hospital-departments/(?P<pk>[/.]+)/` | - | [future] canonical reference-data endpoint not yet consumed by Next.js UI |
| `DELETE /api/rotations/hospital-departments/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?; GET /api/rotations/hospital-departments/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?; PATCH /api/rotations/hospital-departments/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?; PUT /api/rotations/hospital-departments/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `GET /api/rotations/hospital-departments\.(?P<format>[a-z0-9]+)/?; POST /api/rotations/hospital-departments\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `GET /api/rotations/hospitals/; POST /api/rotations/hospitals/` | - | [future] canonical reference-data endpoint not yet consumed by Next.js UI |
| `DELETE /api/rotations/hospitals/(?P<pk>[/.]+)/; GET /api/rotations/hospitals/(?P<pk>[/.]+)/; PATCH /api/rotations/hospitals/(?P<pk>[/.]+)/; PUT /api/rotations/hospitals/(?P<pk>[/.]+)/` | - | [future] canonical reference-data endpoint not yet consumed by Next.js UI |
| `DELETE /api/rotations/hospitals/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?; GET /api/rotations/hospitals/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?; PATCH /api/rotations/hospitals/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?; PUT /api/rotations/hospitals/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `GET /api/rotations/hospitals\.(?P<format>[a-z0-9]+)/?; POST /api/rotations/hospitals\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `GET /api/rotations/my/` | `rotationsApi.getMyRotations` (lib/api/rotations.ts:25) | USED |
| `GET /api/rotations/my/<int:pk>/` | `rotationsApi.getMyRotation` (lib/api/rotations.ts:33) | USED |
| `GET /api/search/` | `searchApi.search` (lib/api/search.ts:34) | USED |
| `GET /api/search/history/` | `searchApi.getHistory` (lib/api/search.ts:44) | USED |
| `GET /api/search/suggestions/` | `searchApi.getSuggestions` (lib/api/search.ts:52) | USED |
| `GET /api/users/assigned-pgs/` | `usersApi.getAssignedPGs` (lib/api/users.ts:15) | USED |
| `GET /cases/api/diagnoses/` | - | [backend-only] legacy Django template/AJAX endpoint |
| `GET /cases/api/procedures/` | - | [backend-only] legacy Django template/AJAX endpoint |
| `GET /certificates/api/<int:pk>/verify/` | - | [backend-only] legacy Django template/AJAX endpoint |
| `GET /certificates/api/quick-stats/` | - | [backend-only] legacy Django template/AJAX endpoint |
| `GET /certificates/api/stats/` | - | [backend-only] legacy Django template/AJAX endpoint |
| `GET /certificates/api/update-statistics/` | - | [backend-only] legacy Django template/AJAX endpoint |
| `GET /logbook/api/entry/<int:entry_id>/complexity/` | - | [backend-only] legacy Django template/AJAX endpoint |
| `GET /logbook/api/stats/` | - | [backend-only] legacy Django template/AJAX endpoint |
| `GET /logbook/api/template/<int:template_id>/preview/` | - | [backend-only] legacy Django template/AJAX endpoint |
| `GET /logbook/api/update-statistics/` | - | [backend-only] legacy Django template/AJAX endpoint |
| `GET /results/api/exams/; POST /results/api/exams/` | `resultsApi.list` (lib/api/results.ts:54); `resultsApi.create` (lib/api/results.ts:62) | USED |
| `DELETE /results/api/exams/(?P<pk>[/.]+)/; GET /results/api/exams/(?P<pk>[/.]+)/; PATCH /results/api/exams/(?P<pk>[/.]+)/; PUT /results/api/exams/(?P<pk>[/.]+)/` | `resultsApi.delete` (lib/api/results.ts:70); `resultsApi.get` (lib/api/results.ts:58); `resultsApi.update` (lib/api/results.ts:66) | USED |
| `GET /results/api/exams/(?P<pk>[/.]+)/scores/` | `resultsApi.getScores` (lib/api/results.ts:73) | USED |
| `GET /results/api/exams/(?P<pk>[/.]+)/scores\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `GET /results/api/exams/(?P<pk>[/.]+)/statistics/` | `resultsApi.getStatistics` (lib/api/results.ts:77) | USED |
| `GET /results/api/exams/(?P<pk>[/.]+)/statistics\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `DELETE /results/api/exams/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?; GET /results/api/exams/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?; PATCH /results/api/exams/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?; PUT /results/api/exams/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `GET /results/api/exams\.(?P<format>[a-z0-9]+)/?; POST /results/api/exams\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `GET /results/api/scores/; POST /results/api/scores/` | `resultsApi.list` (lib/api/results.ts:87); `resultsApi.create` (lib/api/results.ts:95) | USED |
| `DELETE /results/api/scores/(?P<pk>[/.]+)/; GET /results/api/scores/(?P<pk>[/.]+)/; PATCH /results/api/scores/(?P<pk>[/.]+)/; PUT /results/api/scores/(?P<pk>[/.]+)/` | `resultsApi.delete` (lib/api/results.ts:103); `resultsApi.get` (lib/api/results.ts:91); `resultsApi.update` (lib/api/results.ts:99) | USED |
| `DELETE /results/api/scores/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?; GET /results/api/scores/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?; PATCH /results/api/scores/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?; PUT /results/api/scores/(?P<pk>[/.]+)\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `GET /results/api/scores/my_scores/` | `resultsApi.getMyScores` (lib/api/results.ts:106) | USED |
| `GET /results/api/scores/my_scores\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `GET /results/api/scores\.(?P<format>[a-z0-9]+)/?; POST /results/api/scores\.(?P<format>[a-z0-9]+)/?` | - | [internal] DRF format-suffix duplicate route |
| `GET /rotations/api/calendar/` | - | [backend-only] legacy Django template/AJAX endpoint |
| `GET /rotations/api/departments/<int:hospital_id>/` | - | [backend-only] legacy Django template/AJAX endpoint |
| `GET /rotations/api/quick-stats/` | - | [backend-only] legacy Django template/AJAX endpoint |
| `GET /rotations/api/stats/` | - | [backend-only] legacy Django template/AJAX endpoint |
| `GET /users/api/admin/stats/` | - | [backend-only] legacy Django template/AJAX endpoint |
| `GET /users/api/stats/` | - | [backend-only] legacy Django template/AJAX endpoint |
| `GET /users/api/supervisors/specialty/<str:specialty>/` | - | [backend-only] legacy Django template/AJAX endpoint |
| `GET /users/api/user-performance/` | - | [backend-only] legacy Django template/AJAX endpoint |
| `GET /users/api/user-statistics/` | - | [backend-only] legacy Django template/AJAX endpoint |
| `GET /users/api/user/<int:pk>/stats/` | - | [backend-only] legacy Django template/AJAX endpoint |
| `GET /users/api/users/search/` | - | [backend-only] legacy Django template/AJAX endpoint |

### C2. Frontend Call -> Backend Endpoint Match

| Frontend Call | Backend Match | Status |
|---|---|---|
| GET '/academics/api/departments/' (lib/api/academics.ts:48 academicsApi.list) | `GET,POST /academics/api/departments/` | MATCHED |
| GET `/academics/api/departments/${id}/` (lib/api/academics.ts:52 academicsApi.get) | `DELETE,GET,PATCH,PUT /academics/api/departments/(?P<pk>[/.]+)/` | MATCHED |
| POST '/academics/api/departments/' (lib/api/academics.ts:56 academicsApi.create) | `GET,POST /academics/api/departments/` | MATCHED |
| PUT `/academics/api/departments/${id}/` (lib/api/academics.ts:60 academicsApi.update) | `DELETE,GET,PATCH,PUT /academics/api/departments/(?P<pk>[/.]+)/` | MATCHED |
| DELETE `/academics/api/departments/${id}/` (lib/api/academics.ts:64 academicsApi.delete) | `DELETE,GET,PATCH,PUT /academics/api/departments/(?P<pk>[/.]+)/` | MATCHED |
| GET '/academics/api/batches/' (lib/api/academics.ts:73 academicsApi.list) | `GET,POST /academics/api/batches/` | MATCHED |
| GET `/academics/api/batches/${id}/` (lib/api/academics.ts:77 academicsApi.get) | `DELETE,GET,PATCH,PUT /academics/api/batches/(?P<pk>[/.]+)/` | MATCHED |
| POST '/academics/api/batches/' (lib/api/academics.ts:81 academicsApi.create) | `GET,POST /academics/api/batches/` | MATCHED |
| PUT `/academics/api/batches/${id}/` (lib/api/academics.ts:85 academicsApi.update) | `DELETE,GET,PATCH,PUT /academics/api/batches/(?P<pk>[/.]+)/` | MATCHED |
| DELETE `/academics/api/batches/${id}/` (lib/api/academics.ts:89 academicsApi.delete) | `DELETE,GET,PATCH,PUT /academics/api/batches/(?P<pk>[/.]+)/` | MATCHED |
| GET `/academics/api/batches/${id}/students/` (lib/api/academics.ts:92 academicsApi.getStudents) | `GET /academics/api/batches/(?P<pk>[/.]+)/students/` | MATCHED |
| GET '/academics/api/students/' (lib/api/academics.ts:102 academicsApi.list) | `GET,POST /academics/api/students/` | MATCHED |
| GET `/academics/api/students/${id}/` (lib/api/academics.ts:106 academicsApi.get) | `DELETE,GET,PATCH,PUT /academics/api/students/(?P<pk>[/.]+)/` | MATCHED |
| POST '/academics/api/students/' (lib/api/academics.ts:110 academicsApi.create) | `GET,POST /academics/api/students/` | MATCHED |
| PUT `/academics/api/students/${id}/` (lib/api/academics.ts:114 academicsApi.update) | `DELETE,GET,PATCH,PUT /academics/api/students/(?P<pk>[/.]+)/` | MATCHED |
| DELETE `/academics/api/students/${id}/` (lib/api/academics.ts:118 academicsApi.delete) | `DELETE,GET,PATCH,PUT /academics/api/students/(?P<pk>[/.]+)/` | MATCHED |
| POST `/academics/api/students/${id}/update_status/` (lib/api/academics.ts:121 academicsApi.updateStatus) | `POST /academics/api/students/(?P<pk>[/.]+)/update_status/` | MATCHED |
| GET '/api/analytics/dashboard/overview/' (lib/api/analytics.ts:42 analyticsApi.getDashboardOverview) | `GET /api/analytics/dashboard/overview/` | MATCHED |
| GET '/api/analytics/dashboard/trends/' (lib/api/analytics.ts:50 analyticsApi.getTrends) | `GET /api/analytics/dashboard/trends/` | MATCHED |
| GET '/api/analytics/dashboard/compliance/' (lib/api/analytics.ts:58 analyticsApi.getCompliance) | `GET /api/analytics/dashboard/compliance/` | MATCHED |
| GET '/api/analytics/performance/' (lib/api/analytics.ts:66 analyticsApi.getPerformance) | `GET /api/analytics/performance/` | MATCHED |
| GET '/api/attendance/summary/' (lib/api/attendance.ts:38 attendanceApi.getSummary) | `GET /api/attendance/summary/` | MATCHED |
| POST '/api/attendance/upload/' (lib/api/attendance.ts:49 attendanceApi.bulkUpload) | `POST /api/attendance/upload/` | MATCHED |
| GET '/api/audit/activity/' (lib/api/audit.ts:31 auditApi.getActivityLogs) | `GET /api/audit/activity/` | MATCHED |
| GET '/api/audit/reports/' (lib/api/audit.ts:39 auditApi.getReports) | `GET,POST /api/audit/reports/` | MATCHED |
| POST '/api/audit/reports/' (lib/api/audit.ts:47 auditApi.createReport) | `GET,POST /api/audit/reports/` | MATCHED |
| POST '/api/auth/login/' (lib/api/auth.ts:59 authApi.login) | `POST /api/auth/login/` | MATCHED |
| POST '/api/auth/register/' (lib/api/auth.ts:67 authApi.register) | `POST /api/auth/register/` | MATCHED |
| POST '/api/auth/logout/' (lib/api/auth.ts:78 authApi.logout) | `POST /api/auth/logout/` | MATCHED |
| GET '/api/auth/profile/' (lib/api/auth.ts:97 authApi.getCurrentUser) | `GET /api/auth/profile/` | MATCHED |
| POST '/api/auth/refresh/' (lib/api/auth.ts:106 authApi.refreshToken) | `POST /api/auth/refresh/` | MATCHED |
| PATCH '/api/auth/profile/update/' (lib/api/auth.ts:117 authApi.updateProfile) | `PUT,PATCH /api/auth/profile/update/` | MATCHED |
| POST '/api/auth/password-reset/' (lib/api/auth.ts:126 authApi.passwordReset) | `POST /api/auth/password-reset/` | MATCHED |
| POST '/api/auth/password-reset/confirm/' (lib/api/auth.ts:140 authApi.passwordResetConfirm) | `POST /api/auth/password-reset/confirm/` | MATCHED |
| POST '/api/auth/change-password/' (lib/api/auth.ts:153 authApi.changePassword) | `POST /api/auth/change-password/` | MATCHED |
| POST '/api/bulk/import/' (lib/api/bulk.ts:38 bulkApi.import) | `POST /api/bulk/import/` | MATCHED |
| POST '/api/bulk/import-trainees/' (lib/api/bulk.ts:53 bulkApi.importTrainees) | `POST /api/bulk/import-trainees/` | MATCHED |
| POST '/api/bulk/import-supervisors/' (lib/api/bulk.ts:68 bulkApi.importSupervisors) | `POST /api/bulk/import-supervisors/` | MATCHED |
| POST '/api/bulk/import-residents/' (lib/api/bulk.ts:83 bulkApi.importResidents) | `POST /api/bulk/import-residents/` | MATCHED |
| POST '/api/bulk/assignment/' (lib/api/bulk.ts:95 bulkApi.assignment) | `POST /api/bulk/assignment/` | MATCHED |
| POST '/api/bulk/review/' (lib/api/bulk.ts:103 bulkApi.review) | `POST /api/bulk/review/` | MATCHED |
| GET '/api/certificates/my/' (lib/api/certificates.ts:22 certificatesApi.getMyCertificates) | `GET /api/certificates/my/` | MATCHED |
| GET (dynamic via certificatesApi.getCertificateDownloadUrl) (lib/api/certificates.ts:45 certificatesApi.downloadCertificate) | `GET /api/certificates/my/<int:pk>/download/` | MATCHED |
| POST `${API_URL}/api/auth/refresh/` (lib/api/client.ts:66 ) | `POST /api/auth/refresh/` | MATCHED |
| GET '/api/logbook/pending/' (lib/api/logbook.ts:68 logbookApi.getPending) | `GET /api/logbook/pending/` | MATCHED |
| PATCH `/api/logbook/${id}/verify/` (lib/api/logbook.ts:79 logbookApi.verify) | `PATCH /api/logbook/<int:pk>/verify/` | MATCHED |
| GET '/api/logbook/my/' (lib/api/logbook.ts:90 logbookApi.getMyEntries) | `GET,POST /api/logbook/my/` | MATCHED |
| POST '/api/logbook/my/' (lib/api/logbook.ts:100 logbookApi.createMyEntry) | `GET,POST /api/logbook/my/` | MATCHED |
| PATCH `/api/logbook/my/${id}/` (lib/api/logbook.ts:108 logbookApi.updateMyEntry) | `PATCH /api/logbook/my/<int:pk>/` | MATCHED |
| POST `/api/logbook/my/${id}/submit/` (lib/api/logbook.ts:116 logbookApi.submitMyEntry) | `POST /api/logbook/my/<int:pk>/submit/` | MATCHED |
| GET '/api/notifications/' (lib/api/notifications.ts:30 notificationsApi.list) | `GET /api/notifications/` | MATCHED |
| GET '/api/notifications/' (lib/api/notifications.ts:39 notificationsApi.getUnread) | `GET /api/notifications/` | MATCHED |
| GET '/api/notifications/unread-count/' (lib/api/notifications.ts:50 notificationsApi.getUnreadCount) | `GET /api/notifications/unread-count/` | MATCHED |
| POST `/api/notifications/mark-read/` (lib/api/notifications.ts:59 notificationsApi.markRead) | `POST /api/notifications/mark-read/` | MATCHED |
| GET '/api/notifications/preferences/' (lib/api/notifications.ts:69 notificationsApi.getPreferences) | `GET,PATCH /api/notifications/preferences/` | MATCHED |
| PATCH '/api/notifications/preferences/' (lib/api/notifications.ts:77 notificationsApi.updatePreferences) | `GET,PATCH /api/notifications/preferences/` | MATCHED |
| GET '/api/reports/templates/' (lib/api/reports.ts:40 reportsApi.getTemplates) | `GET /api/reports/templates/` | MATCHED |
| POST '/api/reports/generate/' (lib/api/reports.ts:48 reportsApi.generate) | `POST /api/reports/generate/` | MATCHED |
| GET '/api/reports/scheduled/' (lib/api/reports.ts:59 reportsApi.getScheduled) | `GET,POST /api/reports/scheduled/` | MATCHED |
| POST '/api/reports/scheduled/' (lib/api/reports.ts:67 reportsApi.schedule) | `GET,POST /api/reports/scheduled/` | MATCHED |
| GET `/api/reports/scheduled/${id}/` (lib/api/reports.ts:75 reportsApi.getScheduledDetail) | `GET,PUT,PATCH /api/reports/scheduled/<int:pk>/` | MATCHED |
| GET '/results/api/exams/' (lib/api/results.ts:54 resultsApi.list) | `GET,POST /results/api/exams/` | MATCHED |
| GET `/results/api/exams/${id}/` (lib/api/results.ts:58 resultsApi.get) | `DELETE,GET,PATCH,PUT /results/api/exams/(?P<pk>[/.]+)/` | MATCHED |
| POST '/results/api/exams/' (lib/api/results.ts:62 resultsApi.create) | `GET,POST /results/api/exams/` | MATCHED |
| PUT `/results/api/exams/${id}/` (lib/api/results.ts:66 resultsApi.update) | `DELETE,GET,PATCH,PUT /results/api/exams/(?P<pk>[/.]+)/` | MATCHED |
| DELETE `/results/api/exams/${id}/` (lib/api/results.ts:70 resultsApi.delete) | `DELETE,GET,PATCH,PUT /results/api/exams/(?P<pk>[/.]+)/` | MATCHED |
| GET `/results/api/exams/${id}/scores/` (lib/api/results.ts:73 resultsApi.getScores) | `GET /results/api/exams/(?P<pk>[/.]+)/scores/` | MATCHED |
| GET `/results/api/exams/${id}/statistics/` (lib/api/results.ts:77 resultsApi.getStatistics) | `GET /results/api/exams/(?P<pk>[/.]+)/statistics/` | MATCHED |
| GET '/results/api/scores/' (lib/api/results.ts:87 resultsApi.list) | `GET,POST /results/api/scores/` | MATCHED |
| GET `/results/api/scores/${id}/` (lib/api/results.ts:91 resultsApi.get) | `DELETE,GET,PATCH,PUT /results/api/scores/(?P<pk>[/.]+)/` | MATCHED |
| POST '/results/api/scores/' (lib/api/results.ts:95 resultsApi.create) | `GET,POST /results/api/scores/` | MATCHED |
| PUT `/results/api/scores/${id}/` (lib/api/results.ts:99 resultsApi.update) | `DELETE,GET,PATCH,PUT /results/api/scores/(?P<pk>[/.]+)/` | MATCHED |
| DELETE `/results/api/scores/${id}/` (lib/api/results.ts:103 resultsApi.delete) | `DELETE,GET,PATCH,PUT /results/api/scores/(?P<pk>[/.]+)/` | MATCHED |
| GET '/results/api/scores/my_scores/' (lib/api/results.ts:106 resultsApi.getMyScores) | `GET /results/api/scores/my_scores/` | MATCHED |
| GET '/api/rotations/my/' (lib/api/rotations.ts:25 rotationsApi.getMyRotations) | `GET /api/rotations/my/` | MATCHED |
| GET `/api/rotations/my/${id}/` (lib/api/rotations.ts:33 rotationsApi.getMyRotation) | `GET /api/rotations/my/<int:pk>/` | MATCHED |
| GET '/api/search/' (lib/api/search.ts:34 searchApi.search) | `GET /api/search/` | MATCHED |
| GET '/api/search/history/' (lib/api/search.ts:44 searchApi.getHistory) | `GET /api/search/history/` | MATCHED |
| GET '/api/search/suggestions/' (lib/api/search.ts:52 searchApi.getSuggestions) | `GET /api/search/suggestions/` | MATCHED |
| GET '/api/users/assigned-pgs/' (lib/api/users.ts:15 usersApi.getAssignedPGs) | `GET /api/users/assigned-pgs/` | MATCHED |

## D) Payload / Contract Alignment
### Logbook workflow (status + feedback aliases + submitted alias)
Backend evidence:
- `feedback` aliases `supervisor_feedback` in serializer: `backend/sims/logbook/api_serializers.py:8`-`backend/sims/logbook/api_serializers.py:11`
- Verify endpoint accepts both `feedback` and `supervisor_feedback`: `backend/sims/logbook/api_views.py:162`-`backend/sims/logbook/api_views.py:167`
- Verify response returns both `supervisor_feedback` and `feedback`: `backend/sims/logbook/api_views.py:201`-`backend/sims/logbook/api_views.py:208`

Frontend normalization evidence:
- Logbook adapter prefers `feedback`, falls back to `supervisor_feedback` / `supervisor_comments`: `frontend/lib/adapters/logbookAdapter.ts:12`-`frontend/lib/adapters/logbookAdapter.ts:17`
- Logbook adapter normalizes submitted timestamp alias (`submitted_at` fallback to `submitted_to_supervisor_at`): `frontend/lib/adapters/logbookAdapter.ts:39`-`frontend/lib/adapters/logbookAdapter.ts:40`
- PG and supervisor logbook pages use the adapter + shared status utility: `frontend/app/dashboard/pg/logbook/page.tsx:40`-`frontend/app/dashboard/pg/logbook/page.tsx:42`, `frontend/app/dashboard/supervisor/logbooks/page.tsx:44`-`frontend/app/dashboard/supervisor/logbooks/page.tsx:46`

Assessment: **Aligned for core logbook flow**.

### Rotations (canonical hospital + department objects)
Backend evidence:
- `RotationSummarySerializer` emits nested `department` and `hospital` objects: `backend/sims/rotations/api_serializers.py:77`-`backend/sims/rotations/api_serializers.py:130`

Frontend normalization / display evidence:
- Rotations API type expects object-shaped `department` and `hospital`: `frontend/lib/api/rotations.ts:7`-`frontend/lib/api/rotations.ts:18`
- Rotation adapter normalizes object/string drift into `{id,name,code}`: `frontend/lib/adapters/rotationAdapter.ts:10`-`frontend/lib/adapters/rotationAdapter.ts:25`
- PG rotations page displays canonical hospital/department objects (names + codes): `frontend/app/dashboard/pg/rotations/page.tsx:23`-`frontend/app/dashboard/pg/rotations/page.tsx:44`, `frontend/app/dashboard/pg/rotations/page.tsx:95`-`frontend/app/dashboard/pg/rotations/page.tsx:97`

Assessment: **Aligned for canonical rotation display**.

### Status terminology lock (`pending` -> `Submitted`)
Evidence:
- Single shared status mapping utility: `frontend/lib/ui/status.ts:10`-`frontend/lib/ui/status.ts:27`
- Shared badge utility: `frontend/lib/ui/status.ts:29`-`frontend/lib/ui/status.ts:44`
- Core pages use shared utility for labels/badges: `frontend/app/dashboard/pg/logbook/page.tsx:144`-`frontend/app/dashboard/pg/logbook/page.tsx:148`, `frontend/app/dashboard/supervisor/logbooks/page.tsx:125`-`frontend/app/dashboard/supervisor/logbooks/page.tsx:130`, `frontend/app/dashboard/supervisor/page.tsx:122`-`frontend/app/dashboard/supervisor/page.tsx:123`

Assessment: **Aligned**.

### Auth + middleware cookie contract (frontend gate convenience)
- Refresh token exchange still uses backend `/api/auth/refresh/`: `backend/sims/users/api_urls.py:13`-`backend/sims/users/api_urls.py:15`, `frontend/lib/api/client.ts:52`-`frontend/lib/api/client.ts:85`
- Cookie mirror stores only access/role/exp (refresh token remains localStorage-only): `frontend/lib/auth/cookies.ts:45`-`frontend/lib/auth/cookies.ts:75`

Assessment: **Aligned**.

### Method mismatch fixes (previous FAIL items)
- Bulk review frontend call now uses `POST /api/bulk/review/`: `frontend/lib/api/bulk.ts:102`-`frontend/lib/api/bulk.ts:104` (backend `post`: `backend/sims/bulk/views.py:41`-`backend/sims/bulk/views.py:46`)
- Notifications preferences update now uses `PATCH /api/notifications/preferences/`: `frontend/lib/api/notifications.ts:76`-`frontend/lib/api/notifications.ts:78` (backend `patch`: `backend/sims/notifications/views.py:74`-`backend/sims/notifications/views.py:79`)

## E) RBAC + Route Gating Alignment
### Backend RBAC enforcement (authoritative)
- Shared DRF permission classes include `ReadAnyWriteAdminOnly` and `ReadAnyWriteAdminOrUTRMCAdmin`: `backend/sims/common_permissions.py:76`-`backend/sims/common_permissions.py:112`
- Option A reference-data authority applied:
  - Department writes: admin only (`ReadAnyWriteAdminOnly`) — `backend/sims/academics/views.py:9`-`backend/sims/academics/views.py:15`
  - Hospital writes: admin only (`ReadAnyWriteAdminOnly`) — `backend/sims/rotations/api_views.py:29`-`backend/sims/rotations/api_views.py:35`
  - HospitalDepartment writes: UTRMC admin primary + admin recovery (`ReadAnyWriteAdminOrUTRMCAdmin`) — `backend/sims/rotations/api_views.py:44`-`backend/sims/rotations/api_views.py:53`
- Logbook supervisees-only/object-level checks and UTRMC read-only queue access remain enforced: `backend/sims/logbook/api_views.py:45`-`backend/sims/logbook/api_views.py:56`, `backend/sims/logbook/api_views.py:111`-`backend/sims/logbook/api_views.py:123`

### Frontend route-group gating alignment
- `/dashboard/pg/*` allows `pg` + `admin`: `frontend/middleware.ts:43`
- `/dashboard/supervisor/*` allows `supervisor` + `admin`: `frontend/middleware.ts:44`
- `/dashboard/admin/*` allows `admin` only: `frontend/middleware.ts:45`
- `/dashboard/utrmc/*` allows `utrmc_user` / `utrmc_admin` + `admin`: `frontend/middleware.ts:46`-`frontend/middleware.ts:48`
- Client guard mirrors admin fallback to avoid post-hydration redirects: `frontend/components/auth/ProtectedRoute.tsx:17`-`frontend/components/auth/ProtectedRoute.tsx:18`

### Middleware cookie contract verification
- Reads only access/role/exp cookies: `frontend/middleware.ts:59`, `frontend/middleware.ts:68`-`frontend/middleware.ts:71`
- Invalid/expired => redirect `/login` and clear cookies: `frontend/middleware.ts:73`-`frontend/middleware.ts:79`
- Negative gate E2E (invalid cookies): `frontend/e2e/login.spec.ts:73`-`frontend/e2e/login.spec.ts:95`
- Positive admin fallback E2E (admin -> PG route): `frontend/e2e/login.spec.ts:97`-`frontend/e2e/login.spec.ts:101`
- UTRMC role mismatch redirect E2E: `frontend/e2e/utrmc_readonly_dashboard.spec.ts:18`-`frontend/e2e/utrmc_readonly_dashboard.spec.ts:23`

Assessment: **Aligned**.

## F) Gaps / Drift Risks (with evidence)
No critical frontend/backend method or path mismatches were found in this pass.

Non-blocking / informational risks:
1. **Dynamic URL parser limitation (documentation tooling only)**
   - `certificatesApi.downloadCertificate` constructs URL via helper before calling `apiClient.get(url, ...)`: `frontend/lib/api/certificates.ts:30`-`frontend/lib/api/certificates.ts:46`
   - Backend endpoint exists and is matched manually for truth-map normalization: `backend/sims/certificates/api_urls.py:8`-`backend/sims/certificates/api_urls.py:10`

2. **Duplicate/overlapping endpoint surfaces increase integration noise (non-breaking)**
   - Legacy Django AJAX endpoints (`/logbook/api/*`, `/rotations/api/*`, `/users/api/*`) coexist with Next.js-facing `/api/*` endpoints.
   - DRF format-suffix duplicate routes remain visible in resolver inventory and are classified as `[internal]`.

## G) Verdict
**PASS**

PASS criteria satisfied:
- Every frontend API call has a backend match (dynamic certificate download URL justified and mapped).
- Every backend endpoint in scope is either consumed or explicitly classified.
- No critical payload mismatch found in core flows (logbook, rotations, auth/middleware cookie contract).
- Admin fallback route-gating alignment is implemented in middleware (and mirrored in `ProtectedRoute`).

