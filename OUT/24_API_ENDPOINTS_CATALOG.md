# API Endpoints Catalog

Total endpoints: 151

## <int:pk>

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| ANY | `/certificates/api/<int:pk>/verify` | `certificate_verification_api` | `custom/standard` | `None` | `` | Authenticated |

## academics

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| GET | `/academics/api` | `APIRootView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |

## admin

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| ANY | `/users/api/admin/stats` | `admin_stats_api` | `custom/standard` | `None` | `` | Authenticated |

## analytics

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| GET | `/api/analytics/comparative` | `ComparativeAnalyticsView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| GET | `/api/analytics/dashboard/compliance` | `DashboardComplianceView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| GET | `/api/analytics/dashboard/overview` | `DashboardOverviewView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| GET | `/api/analytics/dashboard/trends` | `DashboardTrendsView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| POST | `/api/analytics/events` | `AnalyticsEventIngestView` | `custom/standard` | `None` | `IsAuthenticated, AnalyticsAccessPermission` | Authenticated |
| GET | `/api/analytics/events/live` | `AnalyticsLiveView` | `custom/standard` | `None` | `IsAuthenticated, AnalyticsAccessPermission` | Authenticated |
| GET | `/api/analytics/performance` | `PerformanceMetricsView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| GET | `/api/analytics/trends` | `TrendAnalyticsView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| GET | `/api/analytics/v1/filters` | `AnalyticsFiltersView` | `custom/standard` | `None` | `IsAuthenticated, AnalyticsAccessPermission` | Authenticated |
| GET | `/api/analytics/v1/live` | `AnalyticsLiveView` | `custom/standard` | `None` | `IsAuthenticated, AnalyticsAccessPermission` | Authenticated |
| GET | `/api/analytics/v1/quality` | `AnalyticsQualityView` | `custom/standard` | `None` | `IsAuthenticated, AnalyticsAccessPermission` | Authenticated |
| GET | `/api/analytics/v1/tabs/<str:tab>` | `AnalyticsTabView` | `custom/standard` | `None` | `IsAuthenticated, AnalyticsAccessPermission` | Authenticated |
| GET | `/api/analytics/v1/tabs/<str:tab>/export` | `AnalyticsTabExportView` | `custom/standard` | `None` | `IsAuthenticated, AnalyticsAccessPermission` | Authenticated |

## attendance

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| GET | `/api/attendance/summary` | `AttendanceSummaryView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| POST | `/api/attendance/upload` | `BulkAttendanceUploadView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |

## audit

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| GET | `/api/audit` | `APIRootView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| GET | `/api/audit/activity` | `ActivityLogViewSet` | `list` | `ActivityLogSerializer` | `IsAdminUser` | Authenticated |
| GET | `/api/audit/activity/export` | `ActivityLogViewSet` | `export_csv` | `ActivityLogSerializer` | `IsAdminUser` | Authenticated |
| GET | `/api/audit/activity/{pk}` | `ActivityLogViewSet` | `retrieve` | `ActivityLogSerializer` | `IsAdminUser` | Authenticated |
| GET | `/api/audit/reports` | `AuditReportViewSet` | `list` | `AuditReportSerializer` | `IsAdminUser` | Authenticated |
| POST | `/api/audit/reports` | `AuditReportViewSet` | `create` | `AuditReportSerializer` | `IsAdminUser` | Authenticated |
| GET | `/api/audit/reports/latest` | `AuditReportViewSet` | `latest` | `AuditReportSerializer` | `IsAdminUser` | Authenticated |

## auth

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| POST | `/api/auth/change-password` | `change_password_view` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| POST | `/api/auth/login` | `CustomTokenObtainPairView` | `custom/standard` | `CustomTokenObtainPairSerializer` | `` | Authenticated |
| POST | `/api/auth/logout` | `logout_view` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| POST | `/api/auth/password-reset` | `password_reset_request_view` | `custom/standard` | `None` | `AllowAny` | Public |
| POST | `/api/auth/password-reset/confirm` | `password_reset_confirm_view` | `custom/standard` | `None` | `AllowAny` | Public |
| GET | `/api/auth/profile` | `user_profile_view` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| PATCH | `/api/auth/profile/update` | `update_profile_view` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| PUT | `/api/auth/profile/update` | `update_profile_view` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| POST | `/api/auth/refresh` | `TokenRefreshView` | `custom/standard` | `None` | `` | Authenticated |
| POST | `/api/auth/register` | `register_view` | `custom/standard` | `None` | `AllowAny` | Public |

## batches

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| GET | `/academics/api/batches` | `BatchViewSet` | `list` | `BatchSerializer` | `IsAuthenticated` | Authenticated |
| POST | `/academics/api/batches` | `BatchViewSet` | `create` | `BatchSerializer` | `IsAuthenticated` | Authenticated |
| DELETE | `/academics/api/batches/{pk}` | `BatchViewSet` | `destroy` | `BatchSerializer` | `IsAuthenticated` | Authenticated |
| GET | `/academics/api/batches/{pk}` | `BatchViewSet` | `retrieve` | `BatchSerializer` | `IsAuthenticated` | Authenticated |
| PATCH | `/academics/api/batches/{pk}` | `BatchViewSet` | `partial_update` | `BatchSerializer` | `IsAuthenticated` | Authenticated |
| PUT | `/academics/api/batches/{pk}` | `BatchViewSet` | `update` | `BatchSerializer` | `IsAuthenticated` | Authenticated |
| GET | `/academics/api/batches/{pk}/students` | `BatchViewSet` | `students` | `BatchSerializer` | `IsAuthenticated` | Authenticated |

## bulk

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| POST | `/api/bulk/assignment` | `BulkAssignmentView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| GET | `/api/bulk/exports/<str:resource>` | `BulkExportView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| POST | `/api/bulk/import` | `BulkImportView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| POST | `/api/bulk/import-departments` | `BulkDepartmentImportView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| POST | `/api/bulk/import-residents` | `BulkResidentImportView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| POST | `/api/bulk/import-supervisors` | `BulkSupervisorImportView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| POST | `/api/bulk/import-trainees` | `BulkTraineeImportView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| POST | `/api/bulk/review` | `BulkReviewView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |

## calendar

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| ANY | `/rotations/api/calendar` | `rotation_calendar_api` | `custom/standard` | `None` | `` | Authenticated |

## cases

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| POST | `/api/cases/<int:pk>/review` | `CaseReviewActionView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| GET | `/api/cases/categories` | `CaseCategoryListView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| GET | `/api/cases/my` | `PGCaseListCreateView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| POST | `/api/cases/my` | `PGCaseListCreateView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| DELETE | `/api/cases/my/<int:pk>` | `PGCaseDetailView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| GET | `/api/cases/my/<int:pk>` | `PGCaseDetailView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| PATCH | `/api/cases/my/<int:pk>` | `PGCaseDetailView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| POST | `/api/cases/my/<int:pk>/submit` | `PGCaseSubmitView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| GET | `/api/cases/pending` | `PendingCaseListView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| GET | `/api/cases/statistics` | `CaseStatisticsView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |

## certificates

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| GET | `/api/certificates/my` | `PGCertificatesListView` | `custom/standard` | `None` | `IsAuthenticated, IsPGUser` | Authenticated |
| GET | `/api/certificates/my/<int:pk>/download` | `PGCertificateDownloadView` | `custom/standard` | `None` | `IsAuthenticated, IsPGUser` | Authenticated |

## departments

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| GET | `/academics/api/departments` | `DepartmentViewSet` | `list` | `DepartmentSerializer` | `ReadAnyWriteAdminOnly` | Authenticated |
| POST | `/academics/api/departments` | `DepartmentViewSet` | `create` | `DepartmentSerializer` | `ReadAnyWriteAdminOnly` | Authenticated |
| DELETE | `/academics/api/departments/{pk}` | `DepartmentViewSet` | `destroy` | `DepartmentSerializer` | `ReadAnyWriteAdminOnly` | Authenticated |
| GET | `/academics/api/departments/{pk}` | `DepartmentViewSet` | `retrieve` | `DepartmentSerializer` | `ReadAnyWriteAdminOnly` | Authenticated |
| PATCH | `/academics/api/departments/{pk}` | `DepartmentViewSet` | `partial_update` | `DepartmentSerializer` | `ReadAnyWriteAdminOnly` | Authenticated |
| PUT | `/academics/api/departments/{pk}` | `DepartmentViewSet` | `update` | `DepartmentSerializer` | `ReadAnyWriteAdminOnly` | Authenticated |
| ANY | `/rotations/api/departments/<int:hospital_id>` | `department_by_hospital_api` | `custom/standard` | `None` | `` | Authenticated |

## diagnoses

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| ANY | `/cases/api/diagnoses` | `get_diagnoses_json` | `custom/standard` | `None` | `` | Authenticated |

## entry

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| ANY | `/logbook/api/entry/<int:entry_id>/complexity` | `entry_complexity_api` | `custom/standard` | `None` | `` | Authenticated |

## exams

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| GET | `/results/api/exams` | `ExamViewSet` | `list` | `ExamSerializer` | `IsAuthenticated` | Authenticated |
| POST | `/results/api/exams` | `ExamViewSet` | `create` | `ExamSerializer` | `IsAuthenticated` | Authenticated |
| DELETE | `/results/api/exams/{pk}` | `ExamViewSet` | `destroy` | `ExamSerializer` | `IsAuthenticated` | Authenticated |
| GET | `/results/api/exams/{pk}` | `ExamViewSet` | `retrieve` | `ExamSerializer` | `IsAuthenticated` | Authenticated |
| PATCH | `/results/api/exams/{pk}` | `ExamViewSet` | `partial_update` | `ExamSerializer` | `IsAuthenticated` | Authenticated |
| PUT | `/results/api/exams/{pk}` | `ExamViewSet` | `update` | `ExamSerializer` | `IsAuthenticated` | Authenticated |
| GET | `/results/api/exams/{pk}/scores` | `ExamViewSet` | `scores` | `ExamSerializer` | `IsAuthenticated` | Authenticated |
| GET | `/results/api/exams/{pk}/statistics` | `ExamViewSet` | `statistics` | `ExamSerializer` | `IsAuthenticated` | Authenticated |

## logbook

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| PATCH | `/api/logbook/<int:pk>/verify` | `VerifyLogbookEntryView` | `custom/standard` | `None` | `CanVerifyLogbookEntry` | Authenticated |
| GET | `/api/logbook/my` | `PGLogbookEntryListCreateView` | `custom/standard` | `None` | `IsAuthenticated, IsPGUser` | Authenticated |
| POST | `/api/logbook/my` | `PGLogbookEntryListCreateView` | `custom/standard` | `None` | `IsAuthenticated, IsPGUser` | Authenticated |
| PATCH | `/api/logbook/my/<int:pk>` | `PGLogbookEntryDetailView` | `custom/standard` | `None` | `IsAuthenticated, IsPGUser` | Authenticated |
| POST | `/api/logbook/my/<int:pk>/submit` | `PGLogbookEntrySubmitView` | `custom/standard` | `None` | `IsAuthenticated, IsPGUser` | Authenticated |
| GET | `/api/logbook/pending` | `PendingLogbookEntriesView` | `custom/standard` | `None` | `CanViewPendingLogbookQueue` | Authenticated |

## notifications

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| GET | `/api/notifications` | `NotificationListView` | `custom/standard` | `NotificationSerializer` | `IsAuthenticated` | Authenticated |
| POST | `/api/notifications/mark-read` | `NotificationMarkReadView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| GET | `/api/notifications/preferences` | `NotificationPreferenceView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| PATCH | `/api/notifications/preferences` | `NotificationPreferenceView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| GET | `/api/notifications/unread-count` | `NotificationUnreadCountView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |

## procedures

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| ANY | `/cases/api/procedures` | `get_procedures_json` | `custom/standard` | `None` | `` | Authenticated |

## quick-stats

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| ANY | `/certificates/api/quick-stats` | `certificate_quick_stats` | `custom/standard` | `None` | `` | Authenticated |
| ANY | `/rotations/api/quick-stats` | `rotation_quick_stats` | `custom/standard` | `None` | `` | Authenticated |

## reports

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| GET | `/api/reports/catalog` | `ReportCatalogView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| GET | `/api/reports/export/<str:key>` | `ReportExportView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| POST | `/api/reports/generate` | `ReportGenerateView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| GET | `/api/reports/run/<str:key>` | `ReportRunView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| GET | `/api/reports/scheduled` | `ScheduledReportListCreateView` | `custom/standard` | `ScheduledReportSerializer` | `IsAuthenticated` | Authenticated |
| POST | `/api/reports/scheduled` | `ScheduledReportListCreateView` | `custom/standard` | `ScheduledReportSerializer` | `IsAuthenticated` | Authenticated |
| GET | `/api/reports/scheduled/<int:pk>` | `ScheduledReportDetailView` | `custom/standard` | `ScheduledReportSerializer` | `IsAuthenticated` | Authenticated |
| PATCH | `/api/reports/scheduled/<int:pk>` | `ScheduledReportDetailView` | `custom/standard` | `ScheduledReportSerializer` | `IsAuthenticated` | Authenticated |
| PUT | `/api/reports/scheduled/<int:pk>` | `ScheduledReportDetailView` | `custom/standard` | `ScheduledReportSerializer` | `IsAuthenticated` | Authenticated |
| GET | `/api/reports/templates` | `ReportTemplateListView` | `custom/standard` | `ReportTemplateSerializer` | `IsAuthenticated` | Authenticated |

## results

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| GET | `/results/api` | `APIRootView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |

## rotations

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| GET | `/api/rotations` | `APIRootView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| PATCH | `/api/rotations/<int:pk>/utrmc-approve` | `UTRMCRotationOverrideApproveView` | `custom/standard` | `None` | `IsAuthenticated, IsUTRMCAdminUser, CanApproveRotationOverride` | Authenticated |
| GET | `/api/rotations/hospital-departments` | `HospitalDepartmentViewSet` | `list` | `HospitalDepartmentSerializer` | `ReadAnyWriteAdminOrUTRMCAdmin` | Authenticated |
| POST | `/api/rotations/hospital-departments` | `HospitalDepartmentViewSet` | `create` | `HospitalDepartmentSerializer` | `ReadAnyWriteAdminOrUTRMCAdmin` | Authenticated |
| DELETE | `/api/rotations/hospital-departments/{pk}` | `HospitalDepartmentViewSet` | `destroy` | `HospitalDepartmentSerializer` | `ReadAnyWriteAdminOrUTRMCAdmin` | Authenticated |
| GET | `/api/rotations/hospital-departments/{pk}` | `HospitalDepartmentViewSet` | `retrieve` | `HospitalDepartmentSerializer` | `ReadAnyWriteAdminOrUTRMCAdmin` | Authenticated |
| PATCH | `/api/rotations/hospital-departments/{pk}` | `HospitalDepartmentViewSet` | `partial_update` | `HospitalDepartmentSerializer` | `ReadAnyWriteAdminOrUTRMCAdmin` | Authenticated |
| PUT | `/api/rotations/hospital-departments/{pk}` | `HospitalDepartmentViewSet` | `update` | `HospitalDepartmentSerializer` | `ReadAnyWriteAdminOrUTRMCAdmin` | Authenticated |
| GET | `/api/rotations/hospitals` | `HospitalViewSet` | `list` | `HospitalSerializer` | `ReadAnyWriteAdminOnly` | Authenticated |
| POST | `/api/rotations/hospitals` | `HospitalViewSet` | `create` | `HospitalSerializer` | `ReadAnyWriteAdminOnly` | Authenticated |
| DELETE | `/api/rotations/hospitals/{pk}` | `HospitalViewSet` | `destroy` | `HospitalSerializer` | `ReadAnyWriteAdminOnly` | Authenticated |
| GET | `/api/rotations/hospitals/{pk}` | `HospitalViewSet` | `retrieve` | `HospitalSerializer` | `ReadAnyWriteAdminOnly` | Authenticated |
| PATCH | `/api/rotations/hospitals/{pk}` | `HospitalViewSet` | `partial_update` | `HospitalSerializer` | `ReadAnyWriteAdminOnly` | Authenticated |
| PUT | `/api/rotations/hospitals/{pk}` | `HospitalViewSet` | `update` | `HospitalSerializer` | `ReadAnyWriteAdminOnly` | Authenticated |
| GET | `/api/rotations/my` | `PGMyRotationsListView` | `custom/standard` | `None` | `IsAuthenticated, IsPGUser` | Authenticated |
| GET | `/api/rotations/my/<int:pk>` | `PGMyRotationDetailView` | `custom/standard` | `None` | `IsAuthenticated, IsPGUser` | Authenticated |

## scores

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| GET | `/results/api/scores` | `ScoreViewSet` | `list` | `ScoreSerializer` | `IsAuthenticated` | Authenticated |
| POST | `/results/api/scores` | `ScoreViewSet` | `create` | `ScoreSerializer` | `IsAuthenticated` | Authenticated |
| GET | `/results/api/scores/my_scores` | `ScoreViewSet` | `my_scores` | `ScoreSerializer` | `IsAuthenticated` | Authenticated |
| DELETE | `/results/api/scores/{pk}` | `ScoreViewSet` | `destroy` | `ScoreSerializer` | `IsAuthenticated` | Authenticated |
| GET | `/results/api/scores/{pk}` | `ScoreViewSet` | `retrieve` | `ScoreSerializer` | `IsAuthenticated` | Authenticated |
| PATCH | `/results/api/scores/{pk}` | `ScoreViewSet` | `partial_update` | `ScoreSerializer` | `IsAuthenticated` | Authenticated |
| PUT | `/results/api/scores/{pk}` | `ScoreViewSet` | `update` | `ScoreSerializer` | `IsAuthenticated` | Authenticated |

## search

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| GET | `/api/search` | `GlobalSearchView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| GET | `/api/search/history` | `SearchHistoryView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |
| GET | `/api/search/suggestions` | `SearchSuggestionsView` | `custom/standard` | `None` | `IsAuthenticated` | Authenticated |

## stats

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| ANY | `/certificates/api/stats` | `certificate_stats_api` | `custom/standard` | `None` | `` | Authenticated |
| ANY | `/logbook/api/stats` | `logbook_stats_api` | `custom/standard` | `None` | `` | Authenticated |
| ANY | `/rotations/api/stats` | `rotation_stats_api` | `custom/standard` | `None` | `` | Authenticated |
| ANY | `/users/api/stats` | `view` | `custom/standard` | `None` | `` | Authenticated |

## students

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| GET | `/academics/api/students` | `StudentProfileViewSet` | `list` | `StudentProfileSerializer` | `IsAuthenticated` | Authenticated |
| POST | `/academics/api/students` | `StudentProfileViewSet` | `create` | `StudentProfileSerializer` | `IsAuthenticated` | Authenticated |
| DELETE | `/academics/api/students/{pk}` | `StudentProfileViewSet` | `destroy` | `StudentProfileSerializer` | `IsAuthenticated` | Authenticated |
| GET | `/academics/api/students/{pk}` | `StudentProfileViewSet` | `retrieve` | `StudentProfileSerializer` | `IsAuthenticated` | Authenticated |
| PATCH | `/academics/api/students/{pk}` | `StudentProfileViewSet` | `partial_update` | `StudentProfileSerializer` | `IsAuthenticated` | Authenticated |
| PUT | `/academics/api/students/{pk}` | `StudentProfileViewSet` | `update` | `StudentProfileSerializer` | `IsAuthenticated` | Authenticated |
| POST | `/academics/api/students/{pk}/update_status` | `StudentProfileViewSet` | `update_status` | `StudentProfileSerializer` | `IsAuthenticated` | Authenticated |

## supervisors

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| ANY | `/users/api/supervisors/specialty/<str:specialty>` | `view` | `custom/standard` | `None` | `` | Authenticated |

## template

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| ANY | `/logbook/api/template/<int:template_id>/preview` | `template_preview_api` | `custom/standard` | `None` | `` | Authenticated |

## update-statistics

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| ANY | `/certificates/api/update-statistics` | `update_certificate_statistics` | `custom/standard` | `None` | `` | Authenticated |
| ANY | `/logbook/api/update-statistics` | `update_logbook_statistics` | `custom/standard` | `None` | `` | Authenticated |

## user

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| ANY | `/users/api/user/<int:pk>/stats` | `view` | `custom/standard` | `None` | `` | Authenticated |

## user-performance

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| ANY | `/users/api/user-performance` | `view` | `custom/standard` | `None` | `` | Authenticated |

## user-statistics

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| ANY | `/users/api/user-statistics` | `view` | `custom/standard` | `None` | `` | Authenticated |

## users

| Method | Path | View | Action | Serializer | Permissions | Auth |
|---|---|---|---|---|---|---|
| GET | `/api/users/assigned-pgs` | `SupervisorAssignedPGsView` | `custom/standard` | `None` | `IsAuthenticated, IsSupervisor` | Authenticated |
| ANY | `/users/api/users/search` | `view` | `custom/standard` | `None` | `` | Authenticated |

