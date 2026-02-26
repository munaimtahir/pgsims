# INTEGRATION TRUTH-MAP

## A) Backend Inventory
| Method | Path | View | Action | Serializer | Permission |
|---|---|---|---|---|---|
| ANY | `admin/auth/group/` | changelist_view | func | None | None |
| ANY | `admin/auth/group/add/` | add_view | func | None | None |
| ANY | `admin/auth/group/<path:object_id>/history/` | history_view | func | None | None |
| ANY | `admin/auth/group/<path:object_id>/delete/` | delete_view | func | None | None |
| ANY | `admin/auth/group/<path:object_id>/change/` | change_view | func | None | None |
| GET | `admin/auth/group/<path:object_id>/` | RedirectView | custom/standard | None | None |
| POST | `admin/auth/group/<path:object_id>/` | RedirectView | custom/standard | None | None |
| PUT | `admin/auth/group/<path:object_id>/` | RedirectView | custom/standard | None | None |
| PATCH | `admin/auth/group/<path:object_id>/` | RedirectView | custom/standard | None | None |
| DELETE | `admin/auth/group/<path:object_id>/` | RedirectView | custom/standard | None | None |
| TRACE | `admin/auth/group/<path:object_id>/` | RedirectView | custom/standard | None | None |
| GET | `users/api/users/search/` | UserSearchAPIView | custom/standard | None | None |
| POST | `users/api/users/search/` | UserSearchAPIView | custom/standard | None | None |
| PUT | `users/api/users/search/` | UserSearchAPIView | custom/standard | None | None |
| PATCH | `users/api/users/search/` | UserSearchAPIView | custom/standard | None | None |
| DELETE | `users/api/users/search/` | UserSearchAPIView | custom/standard | None | None |
| TRACE | `users/api/users/search/` | UserSearchAPIView | custom/standard | None | None |
| GET | `users/api/supervisors/specialty/<str:specialty>/` | SupervisorsBySpecialtyAPIView | custom/standard | None | None |
| POST | `users/api/supervisors/specialty/<str:specialty>/` | SupervisorsBySpecialtyAPIView | custom/standard | None | None |
| PUT | `users/api/supervisors/specialty/<str:specialty>/` | SupervisorsBySpecialtyAPIView | custom/standard | None | None |
| PATCH | `users/api/supervisors/specialty/<str:specialty>/` | SupervisorsBySpecialtyAPIView | custom/standard | None | None |
| DELETE | `users/api/supervisors/specialty/<str:specialty>/` | SupervisorsBySpecialtyAPIView | custom/standard | None | None |
| TRACE | `users/api/supervisors/specialty/<str:specialty>/` | SupervisorsBySpecialtyAPIView | custom/standard | None | None |
| GET | `users/api/user/<int:pk>/stats/` | UserStatsAPIView | custom/standard | None | None |
| POST | `users/api/user/<int:pk>/stats/` | UserStatsAPIView | custom/standard | None | None |
| PUT | `users/api/user/<int:pk>/stats/` | UserStatsAPIView | custom/standard | None | None |
| PATCH | `users/api/user/<int:pk>/stats/` | UserStatsAPIView | custom/standard | None | None |
| DELETE | `users/api/user/<int:pk>/stats/` | UserStatsAPIView | custom/standard | None | None |
| TRACE | `users/api/user/<int:pk>/stats/` | UserStatsAPIView | custom/standard | None | None |
| GET | `users/api/stats/` | UserListStatsAPIView | custom/standard | None | None |
| POST | `users/api/stats/` | UserListStatsAPIView | custom/standard | None | None |
| PUT | `users/api/stats/` | UserListStatsAPIView | custom/standard | None | None |
| PATCH | `users/api/stats/` | UserListStatsAPIView | custom/standard | None | None |
| DELETE | `users/api/stats/` | UserListStatsAPIView | custom/standard | None | None |
| TRACE | `users/api/stats/` | UserListStatsAPIView | custom/standard | None | None |
| ANY | `users/api/admin/stats/` | admin_stats_api | func | None | None |
| GET | `users/api/user-statistics/` | UserStatisticsAPIView | custom/standard | None | None |
| POST | `users/api/user-statistics/` | UserStatisticsAPIView | custom/standard | None | None |
| PUT | `users/api/user-statistics/` | UserStatisticsAPIView | custom/standard | None | None |
| PATCH | `users/api/user-statistics/` | UserStatisticsAPIView | custom/standard | None | None |
| DELETE | `users/api/user-statistics/` | UserStatisticsAPIView | custom/standard | None | None |
| TRACE | `users/api/user-statistics/` | UserStatisticsAPIView | custom/standard | None | None |
| GET | `users/api/user-performance/` | UserPerformanceAPIView | custom/standard | None | None |
| POST | `users/api/user-performance/` | UserPerformanceAPIView | custom/standard | None | None |
| PUT | `users/api/user-performance/` | UserPerformanceAPIView | custom/standard | None | None |
| PATCH | `users/api/user-performance/` | UserPerformanceAPIView | custom/standard | None | None |
| DELETE | `users/api/user-performance/` | UserPerformanceAPIView | custom/standard | None | None |
| TRACE | `users/api/user-performance/` | UserPerformanceAPIView | custom/standard | None | None |
| ANY | `rotations/api/calendar/` | rotation_calendar_api | func | None | None |
| ANY | `rotations/api/stats/` | rotation_stats_api | func | None | None |
| ANY | `rotations/api/quick-stats/` | rotation_quick_stats | func | None | None |
| ANY | `rotations/api/departments/<int:hospital_id>/` | department_by_hospital_api | func | None | None |
| ANY | `certificates/api/stats/` | certificate_stats_api | func | None | None |
| ANY | `certificates/api/quick-stats/` | certificate_quick_stats | func | None | None |
| ANY | `certificates/api/<int:pk>/verify/` | certificate_verification_api | func | None | None |
| ANY | `certificates/api/update-statistics/` | update_certificate_statistics | func | None | None |
| ANY | `logbook/api/stats/` | logbook_stats_api | func | None | None |
| ANY | `logbook/api/template/<int:template_id>/preview/` | template_preview_api | func | None | None |
| ANY | `logbook/api/entry/<int:entry_id>/complexity/` | entry_complexity_api | func | None | None |
| ANY | `logbook/api/update-statistics/` | update_logbook_statistics | func | None | None |
| ANY | `cases/api/diagnoses/` | get_diagnoses_json | func | None | None |
| ANY | `cases/api/procedures/` | get_procedures_json | func | None | None |
| ANY | `api/audit/^activity/$` | ActivityLogViewSet | func | None | None |
| ANY | `api/audit/^activity/export/$` | ActivityLogViewSet | func | None | None |
| ANY | `api/audit/^activity/(?P<pk>[^/.]+)/$` | ActivityLogViewSet | func | None | None |
| ANY | `api/audit/^reports/$` | AuditReportViewSet | func | None | None |
| ANY | `api/audit/^reports/latest/$` | AuditReportViewSet | func | None | None |
| GET | `api/audit/` | APIRootView | custom/standard | None | IsAuthenticated |
| POST | `api/audit/` | APIRootView | custom/standard | None | IsAuthenticated |
| PUT | `api/audit/` | APIRootView | custom/standard | None | IsAuthenticated |
| PATCH | `api/audit/` | APIRootView | custom/standard | None | IsAuthenticated |
| DELETE | `api/audit/` | APIRootView | custom/standard | None | IsAuthenticated |
| TRACE | `api/audit/` | APIRootView | custom/standard | None | IsAuthenticated |
| GET | `api/search/` | GlobalSearchView | custom/standard | None | IsAuthenticated |
| POST | `api/search/` | GlobalSearchView | custom/standard | None | IsAuthenticated |
| PUT | `api/search/` | GlobalSearchView | custom/standard | None | IsAuthenticated |
| PATCH | `api/search/` | GlobalSearchView | custom/standard | None | IsAuthenticated |
| DELETE | `api/search/` | GlobalSearchView | custom/standard | None | IsAuthenticated |
| TRACE | `api/search/` | GlobalSearchView | custom/standard | None | IsAuthenticated |
| GET | `api/search/history/` | SearchHistoryView | custom/standard | None | IsAuthenticated |
| POST | `api/search/history/` | SearchHistoryView | custom/standard | None | IsAuthenticated |
| PUT | `api/search/history/` | SearchHistoryView | custom/standard | None | IsAuthenticated |
| PATCH | `api/search/history/` | SearchHistoryView | custom/standard | None | IsAuthenticated |
| DELETE | `api/search/history/` | SearchHistoryView | custom/standard | None | IsAuthenticated |
| TRACE | `api/search/history/` | SearchHistoryView | custom/standard | None | IsAuthenticated |
| GET | `api/search/suggestions/` | SearchSuggestionsView | custom/standard | None | IsAuthenticated |
| POST | `api/search/suggestions/` | SearchSuggestionsView | custom/standard | None | IsAuthenticated |
| PUT | `api/search/suggestions/` | SearchSuggestionsView | custom/standard | None | IsAuthenticated |
| PATCH | `api/search/suggestions/` | SearchSuggestionsView | custom/standard | None | IsAuthenticated |
| DELETE | `api/search/suggestions/` | SearchSuggestionsView | custom/standard | None | IsAuthenticated |
| TRACE | `api/search/suggestions/` | SearchSuggestionsView | custom/standard | None | IsAuthenticated |
| GET | `api/analytics/trends/` | TrendAnalyticsView | custom/standard | None | IsAuthenticated |
| POST | `api/analytics/trends/` | TrendAnalyticsView | custom/standard | None | IsAuthenticated |
| PUT | `api/analytics/trends/` | TrendAnalyticsView | custom/standard | None | IsAuthenticated |
| PATCH | `api/analytics/trends/` | TrendAnalyticsView | custom/standard | None | IsAuthenticated |
| DELETE | `api/analytics/trends/` | TrendAnalyticsView | custom/standard | None | IsAuthenticated |
| TRACE | `api/analytics/trends/` | TrendAnalyticsView | custom/standard | None | IsAuthenticated |
| GET | `api/analytics/comparative/` | ComparativeAnalyticsView | custom/standard | None | IsAuthenticated |
| POST | `api/analytics/comparative/` | ComparativeAnalyticsView | custom/standard | None | IsAuthenticated |
| PUT | `api/analytics/comparative/` | ComparativeAnalyticsView | custom/standard | None | IsAuthenticated |
| PATCH | `api/analytics/comparative/` | ComparativeAnalyticsView | custom/standard | None | IsAuthenticated |
| DELETE | `api/analytics/comparative/` | ComparativeAnalyticsView | custom/standard | None | IsAuthenticated |
| TRACE | `api/analytics/comparative/` | ComparativeAnalyticsView | custom/standard | None | IsAuthenticated |
| GET | `api/analytics/performance/` | PerformanceMetricsView | custom/standard | None | IsAuthenticated |
| POST | `api/analytics/performance/` | PerformanceMetricsView | custom/standard | None | IsAuthenticated |
| PUT | `api/analytics/performance/` | PerformanceMetricsView | custom/standard | None | IsAuthenticated |
| PATCH | `api/analytics/performance/` | PerformanceMetricsView | custom/standard | None | IsAuthenticated |
| DELETE | `api/analytics/performance/` | PerformanceMetricsView | custom/standard | None | IsAuthenticated |
| TRACE | `api/analytics/performance/` | PerformanceMetricsView | custom/standard | None | IsAuthenticated |
| GET | `api/analytics/dashboard/overview/` | DashboardOverviewView | custom/standard | None | IsAuthenticated |
| POST | `api/analytics/dashboard/overview/` | DashboardOverviewView | custom/standard | None | IsAuthenticated |
| PUT | `api/analytics/dashboard/overview/` | DashboardOverviewView | custom/standard | None | IsAuthenticated |
| PATCH | `api/analytics/dashboard/overview/` | DashboardOverviewView | custom/standard | None | IsAuthenticated |
| DELETE | `api/analytics/dashboard/overview/` | DashboardOverviewView | custom/standard | None | IsAuthenticated |
| TRACE | `api/analytics/dashboard/overview/` | DashboardOverviewView | custom/standard | None | IsAuthenticated |
| GET | `api/analytics/dashboard/trends/` | DashboardTrendsView | custom/standard | None | IsAuthenticated |
| POST | `api/analytics/dashboard/trends/` | DashboardTrendsView | custom/standard | None | IsAuthenticated |
| PUT | `api/analytics/dashboard/trends/` | DashboardTrendsView | custom/standard | None | IsAuthenticated |
| PATCH | `api/analytics/dashboard/trends/` | DashboardTrendsView | custom/standard | None | IsAuthenticated |
| DELETE | `api/analytics/dashboard/trends/` | DashboardTrendsView | custom/standard | None | IsAuthenticated |
| TRACE | `api/analytics/dashboard/trends/` | DashboardTrendsView | custom/standard | None | IsAuthenticated |
| GET | `api/analytics/dashboard/compliance/` | DashboardComplianceView | custom/standard | None | IsAuthenticated |
| POST | `api/analytics/dashboard/compliance/` | DashboardComplianceView | custom/standard | None | IsAuthenticated |
| PUT | `api/analytics/dashboard/compliance/` | DashboardComplianceView | custom/standard | None | IsAuthenticated |
| PATCH | `api/analytics/dashboard/compliance/` | DashboardComplianceView | custom/standard | None | IsAuthenticated |
| DELETE | `api/analytics/dashboard/compliance/` | DashboardComplianceView | custom/standard | None | IsAuthenticated |
| TRACE | `api/analytics/dashboard/compliance/` | DashboardComplianceView | custom/standard | None | IsAuthenticated |
| GET | `api/bulk/review/` | BulkReviewView | custom/standard | None | IsAuthenticated |
| POST | `api/bulk/review/` | BulkReviewView | custom/standard | None | IsAuthenticated |
| PUT | `api/bulk/review/` | BulkReviewView | custom/standard | None | IsAuthenticated |
| PATCH | `api/bulk/review/` | BulkReviewView | custom/standard | None | IsAuthenticated |
| DELETE | `api/bulk/review/` | BulkReviewView | custom/standard | None | IsAuthenticated |
| TRACE | `api/bulk/review/` | BulkReviewView | custom/standard | None | IsAuthenticated |
| GET | `api/bulk/assignment/` | BulkAssignmentView | custom/standard | None | IsAuthenticated |
| POST | `api/bulk/assignment/` | BulkAssignmentView | custom/standard | None | IsAuthenticated |
| PUT | `api/bulk/assignment/` | BulkAssignmentView | custom/standard | None | IsAuthenticated |
| PATCH | `api/bulk/assignment/` | BulkAssignmentView | custom/standard | None | IsAuthenticated |
| DELETE | `api/bulk/assignment/` | BulkAssignmentView | custom/standard | None | IsAuthenticated |
| TRACE | `api/bulk/assignment/` | BulkAssignmentView | custom/standard | None | IsAuthenticated |
| GET | `api/bulk/import/` | BulkImportView | custom/standard | None | IsAuthenticated |
| POST | `api/bulk/import/` | BulkImportView | custom/standard | None | IsAuthenticated |
| PUT | `api/bulk/import/` | BulkImportView | custom/standard | None | IsAuthenticated |
| PATCH | `api/bulk/import/` | BulkImportView | custom/standard | None | IsAuthenticated |
| DELETE | `api/bulk/import/` | BulkImportView | custom/standard | None | IsAuthenticated |
| TRACE | `api/bulk/import/` | BulkImportView | custom/standard | None | IsAuthenticated |
| GET | `api/bulk/import-trainees/` | BulkTraineeImportView | custom/standard | None | IsAuthenticated |
| POST | `api/bulk/import-trainees/` | BulkTraineeImportView | custom/standard | None | IsAuthenticated |
| PUT | `api/bulk/import-trainees/` | BulkTraineeImportView | custom/standard | None | IsAuthenticated |
| PATCH | `api/bulk/import-trainees/` | BulkTraineeImportView | custom/standard | None | IsAuthenticated |
| DELETE | `api/bulk/import-trainees/` | BulkTraineeImportView | custom/standard | None | IsAuthenticated |
| TRACE | `api/bulk/import-trainees/` | BulkTraineeImportView | custom/standard | None | IsAuthenticated |
| GET | `api/bulk/import-supervisors/` | BulkSupervisorImportView | custom/standard | None | IsAuthenticated |
| POST | `api/bulk/import-supervisors/` | BulkSupervisorImportView | custom/standard | None | IsAuthenticated |
| PUT | `api/bulk/import-supervisors/` | BulkSupervisorImportView | custom/standard | None | IsAuthenticated |
| PATCH | `api/bulk/import-supervisors/` | BulkSupervisorImportView | custom/standard | None | IsAuthenticated |
| DELETE | `api/bulk/import-supervisors/` | BulkSupervisorImportView | custom/standard | None | IsAuthenticated |
| TRACE | `api/bulk/import-supervisors/` | BulkSupervisorImportView | custom/standard | None | IsAuthenticated |
| GET | `api/bulk/import-residents/` | BulkResidentImportView | custom/standard | None | IsAuthenticated |
| POST | `api/bulk/import-residents/` | BulkResidentImportView | custom/standard | None | IsAuthenticated |
| PUT | `api/bulk/import-residents/` | BulkResidentImportView | custom/standard | None | IsAuthenticated |
| PATCH | `api/bulk/import-residents/` | BulkResidentImportView | custom/standard | None | IsAuthenticated |
| DELETE | `api/bulk/import-residents/` | BulkResidentImportView | custom/standard | None | IsAuthenticated |
| TRACE | `api/bulk/import-residents/` | BulkResidentImportView | custom/standard | None | IsAuthenticated |
| GET | `api/notifications/` | NotificationListView | custom/standard | NotificationSerializer | IsAuthenticated |
| POST | `api/notifications/` | NotificationListView | custom/standard | NotificationSerializer | IsAuthenticated |
| PUT | `api/notifications/` | NotificationListView | custom/standard | NotificationSerializer | IsAuthenticated |
| PATCH | `api/notifications/` | NotificationListView | custom/standard | NotificationSerializer | IsAuthenticated |
| DELETE | `api/notifications/` | NotificationListView | custom/standard | NotificationSerializer | IsAuthenticated |
| TRACE | `api/notifications/` | NotificationListView | custom/standard | NotificationSerializer | IsAuthenticated |
| GET | `api/notifications/mark-read/` | NotificationMarkReadView | custom/standard | None | IsAuthenticated |
| POST | `api/notifications/mark-read/` | NotificationMarkReadView | custom/standard | None | IsAuthenticated |
| PUT | `api/notifications/mark-read/` | NotificationMarkReadView | custom/standard | None | IsAuthenticated |
| PATCH | `api/notifications/mark-read/` | NotificationMarkReadView | custom/standard | None | IsAuthenticated |
| DELETE | `api/notifications/mark-read/` | NotificationMarkReadView | custom/standard | None | IsAuthenticated |
| TRACE | `api/notifications/mark-read/` | NotificationMarkReadView | custom/standard | None | IsAuthenticated |
| GET | `api/notifications/preferences/` | NotificationPreferenceView | custom/standard | None | IsAuthenticated |
| POST | `api/notifications/preferences/` | NotificationPreferenceView | custom/standard | None | IsAuthenticated |
| PUT | `api/notifications/preferences/` | NotificationPreferenceView | custom/standard | None | IsAuthenticated |
| PATCH | `api/notifications/preferences/` | NotificationPreferenceView | custom/standard | None | IsAuthenticated |
| DELETE | `api/notifications/preferences/` | NotificationPreferenceView | custom/standard | None | IsAuthenticated |
| TRACE | `api/notifications/preferences/` | NotificationPreferenceView | custom/standard | None | IsAuthenticated |
| GET | `api/notifications/unread-count/` | NotificationUnreadCountView | custom/standard | None | IsAuthenticated |
| POST | `api/notifications/unread-count/` | NotificationUnreadCountView | custom/standard | None | IsAuthenticated |
| PUT | `api/notifications/unread-count/` | NotificationUnreadCountView | custom/standard | None | IsAuthenticated |
| PATCH | `api/notifications/unread-count/` | NotificationUnreadCountView | custom/standard | None | IsAuthenticated |
| DELETE | `api/notifications/unread-count/` | NotificationUnreadCountView | custom/standard | None | IsAuthenticated |
| TRACE | `api/notifications/unread-count/` | NotificationUnreadCountView | custom/standard | None | IsAuthenticated |
| GET | `api/reports/templates/` | ReportTemplateListView | custom/standard | ReportTemplateSerializer | IsAuthenticated |
| POST | `api/reports/templates/` | ReportTemplateListView | custom/standard | ReportTemplateSerializer | IsAuthenticated |
| PUT | `api/reports/templates/` | ReportTemplateListView | custom/standard | ReportTemplateSerializer | IsAuthenticated |
| PATCH | `api/reports/templates/` | ReportTemplateListView | custom/standard | ReportTemplateSerializer | IsAuthenticated |
| DELETE | `api/reports/templates/` | ReportTemplateListView | custom/standard | ReportTemplateSerializer | IsAuthenticated |
| TRACE | `api/reports/templates/` | ReportTemplateListView | custom/standard | ReportTemplateSerializer | IsAuthenticated |
| GET | `api/reports/generate/` | ReportGenerateView | custom/standard | None | IsAuthenticated |
| POST | `api/reports/generate/` | ReportGenerateView | custom/standard | None | IsAuthenticated |
| PUT | `api/reports/generate/` | ReportGenerateView | custom/standard | None | IsAuthenticated |
| PATCH | `api/reports/generate/` | ReportGenerateView | custom/standard | None | IsAuthenticated |
| DELETE | `api/reports/generate/` | ReportGenerateView | custom/standard | None | IsAuthenticated |
| TRACE | `api/reports/generate/` | ReportGenerateView | custom/standard | None | IsAuthenticated |
| GET | `api/reports/scheduled/` | ScheduledReportListCreateView | custom/standard | ScheduledReportSerializer | IsAuthenticated |
| POST | `api/reports/scheduled/` | ScheduledReportListCreateView | custom/standard | ScheduledReportSerializer | IsAuthenticated |
| PUT | `api/reports/scheduled/` | ScheduledReportListCreateView | custom/standard | ScheduledReportSerializer | IsAuthenticated |
| PATCH | `api/reports/scheduled/` | ScheduledReportListCreateView | custom/standard | ScheduledReportSerializer | IsAuthenticated |
| DELETE | `api/reports/scheduled/` | ScheduledReportListCreateView | custom/standard | ScheduledReportSerializer | IsAuthenticated |
| TRACE | `api/reports/scheduled/` | ScheduledReportListCreateView | custom/standard | ScheduledReportSerializer | IsAuthenticated |
| GET | `api/reports/scheduled/<int:pk>/` | ScheduledReportDetailView | custom/standard | ScheduledReportSerializer | IsAuthenticated |
| POST | `api/reports/scheduled/<int:pk>/` | ScheduledReportDetailView | custom/standard | ScheduledReportSerializer | IsAuthenticated |
| PUT | `api/reports/scheduled/<int:pk>/` | ScheduledReportDetailView | custom/standard | ScheduledReportSerializer | IsAuthenticated |
| PATCH | `api/reports/scheduled/<int:pk>/` | ScheduledReportDetailView | custom/standard | ScheduledReportSerializer | IsAuthenticated |
| DELETE | `api/reports/scheduled/<int:pk>/` | ScheduledReportDetailView | custom/standard | ScheduledReportSerializer | IsAuthenticated |
| TRACE | `api/reports/scheduled/<int:pk>/` | ScheduledReportDetailView | custom/standard | ScheduledReportSerializer | IsAuthenticated |
| GET | `api/logbook/pending/` | PendingLogbookEntriesView | custom/standard | None | CanViewPendingLogbookQueue |
| POST | `api/logbook/pending/` | PendingLogbookEntriesView | custom/standard | None | CanViewPendingLogbookQueue |
| PUT | `api/logbook/pending/` | PendingLogbookEntriesView | custom/standard | None | CanViewPendingLogbookQueue |
| PATCH | `api/logbook/pending/` | PendingLogbookEntriesView | custom/standard | None | CanViewPendingLogbookQueue |
| DELETE | `api/logbook/pending/` | PendingLogbookEntriesView | custom/standard | None | CanViewPendingLogbookQueue |
| TRACE | `api/logbook/pending/` | PendingLogbookEntriesView | custom/standard | None | CanViewPendingLogbookQueue |
| GET | `api/logbook/<int:pk>/verify/` | VerifyLogbookEntryView | custom/standard | None | CanVerifyLogbookEntry |
| POST | `api/logbook/<int:pk>/verify/` | VerifyLogbookEntryView | custom/standard | None | CanVerifyLogbookEntry |
| PUT | `api/logbook/<int:pk>/verify/` | VerifyLogbookEntryView | custom/standard | None | CanVerifyLogbookEntry |
| PATCH | `api/logbook/<int:pk>/verify/` | VerifyLogbookEntryView | custom/standard | None | CanVerifyLogbookEntry |
| DELETE | `api/logbook/<int:pk>/verify/` | VerifyLogbookEntryView | custom/standard | None | CanVerifyLogbookEntry |
| TRACE | `api/logbook/<int:pk>/verify/` | VerifyLogbookEntryView | custom/standard | None | CanVerifyLogbookEntry |
| GET | `api/logbook/my/` | PGLogbookEntryListCreateView | custom/standard | None | IsAuthenticated, IsPGUser |
| POST | `api/logbook/my/` | PGLogbookEntryListCreateView | custom/standard | None | IsAuthenticated, IsPGUser |
| PUT | `api/logbook/my/` | PGLogbookEntryListCreateView | custom/standard | None | IsAuthenticated, IsPGUser |
| PATCH | `api/logbook/my/` | PGLogbookEntryListCreateView | custom/standard | None | IsAuthenticated, IsPGUser |
| DELETE | `api/logbook/my/` | PGLogbookEntryListCreateView | custom/standard | None | IsAuthenticated, IsPGUser |
| TRACE | `api/logbook/my/` | PGLogbookEntryListCreateView | custom/standard | None | IsAuthenticated, IsPGUser |
| GET | `api/logbook/my/<int:pk>/` | PGLogbookEntryDetailView | custom/standard | None | IsAuthenticated, IsPGUser |
| POST | `api/logbook/my/<int:pk>/` | PGLogbookEntryDetailView | custom/standard | None | IsAuthenticated, IsPGUser |
| PUT | `api/logbook/my/<int:pk>/` | PGLogbookEntryDetailView | custom/standard | None | IsAuthenticated, IsPGUser |
| PATCH | `api/logbook/my/<int:pk>/` | PGLogbookEntryDetailView | custom/standard | None | IsAuthenticated, IsPGUser |
| DELETE | `api/logbook/my/<int:pk>/` | PGLogbookEntryDetailView | custom/standard | None | IsAuthenticated, IsPGUser |
| TRACE | `api/logbook/my/<int:pk>/` | PGLogbookEntryDetailView | custom/standard | None | IsAuthenticated, IsPGUser |
| GET | `api/logbook/my/<int:pk>/submit/` | PGLogbookEntrySubmitView | custom/standard | None | IsAuthenticated, IsPGUser |
| POST | `api/logbook/my/<int:pk>/submit/` | PGLogbookEntrySubmitView | custom/standard | None | IsAuthenticated, IsPGUser |
| PUT | `api/logbook/my/<int:pk>/submit/` | PGLogbookEntrySubmitView | custom/standard | None | IsAuthenticated, IsPGUser |
| PATCH | `api/logbook/my/<int:pk>/submit/` | PGLogbookEntrySubmitView | custom/standard | None | IsAuthenticated, IsPGUser |
| DELETE | `api/logbook/my/<int:pk>/submit/` | PGLogbookEntrySubmitView | custom/standard | None | IsAuthenticated, IsPGUser |
| TRACE | `api/logbook/my/<int:pk>/submit/` | PGLogbookEntrySubmitView | custom/standard | None | IsAuthenticated, IsPGUser |
| ANY | `api/rotations/^hospitals/$` | HospitalViewSet | func | None | None |
| ANY | `api/rotations/^hospitals/(?P<pk>[^/.]+)/$` | HospitalViewSet | func | None | None |
| ANY | `api/rotations/^hospital-departments/$` | HospitalDepartmentViewSet | func | None | None |
| ANY | `api/rotations/^hospital-departments/(?P<pk>[^/.]+)/$` | HospitalDepartmentViewSet | func | None | None |
| GET | `api/rotations/` | APIRootView | custom/standard | None | IsAuthenticated |
| POST | `api/rotations/` | APIRootView | custom/standard | None | IsAuthenticated |
| PUT | `api/rotations/` | APIRootView | custom/standard | None | IsAuthenticated |
| PATCH | `api/rotations/` | APIRootView | custom/standard | None | IsAuthenticated |
| DELETE | `api/rotations/` | APIRootView | custom/standard | None | IsAuthenticated |
| TRACE | `api/rotations/` | APIRootView | custom/standard | None | IsAuthenticated |
| GET | `api/rotations/my/` | PGMyRotationsListView | custom/standard | None | IsAuthenticated, IsPGUser |
| POST | `api/rotations/my/` | PGMyRotationsListView | custom/standard | None | IsAuthenticated, IsPGUser |
| PUT | `api/rotations/my/` | PGMyRotationsListView | custom/standard | None | IsAuthenticated, IsPGUser |
| PATCH | `api/rotations/my/` | PGMyRotationsListView | custom/standard | None | IsAuthenticated, IsPGUser |
| DELETE | `api/rotations/my/` | PGMyRotationsListView | custom/standard | None | IsAuthenticated, IsPGUser |
| TRACE | `api/rotations/my/` | PGMyRotationsListView | custom/standard | None | IsAuthenticated, IsPGUser |
| GET | `api/rotations/my/<int:pk>/` | PGMyRotationDetailView | custom/standard | None | IsAuthenticated, IsPGUser |
| POST | `api/rotations/my/<int:pk>/` | PGMyRotationDetailView | custom/standard | None | IsAuthenticated, IsPGUser |
| PUT | `api/rotations/my/<int:pk>/` | PGMyRotationDetailView | custom/standard | None | IsAuthenticated, IsPGUser |
| PATCH | `api/rotations/my/<int:pk>/` | PGMyRotationDetailView | custom/standard | None | IsAuthenticated, IsPGUser |
| DELETE | `api/rotations/my/<int:pk>/` | PGMyRotationDetailView | custom/standard | None | IsAuthenticated, IsPGUser |
| TRACE | `api/rotations/my/<int:pk>/` | PGMyRotationDetailView | custom/standard | None | IsAuthenticated, IsPGUser |
| GET | `api/rotations/<int:pk>/utrmc-approve/` | UTRMCRotationOverrideApproveView | custom/standard | None | IsAuthenticated, IsUTRMCAdminUser, CanApproveRotationOverride |
| POST | `api/rotations/<int:pk>/utrmc-approve/` | UTRMCRotationOverrideApproveView | custom/standard | None | IsAuthenticated, IsUTRMCAdminUser, CanApproveRotationOverride |
| PUT | `api/rotations/<int:pk>/utrmc-approve/` | UTRMCRotationOverrideApproveView | custom/standard | None | IsAuthenticated, IsUTRMCAdminUser, CanApproveRotationOverride |
| PATCH | `api/rotations/<int:pk>/utrmc-approve/` | UTRMCRotationOverrideApproveView | custom/standard | None | IsAuthenticated, IsUTRMCAdminUser, CanApproveRotationOverride |
| DELETE | `api/rotations/<int:pk>/utrmc-approve/` | UTRMCRotationOverrideApproveView | custom/standard | None | IsAuthenticated, IsUTRMCAdminUser, CanApproveRotationOverride |
| TRACE | `api/rotations/<int:pk>/utrmc-approve/` | UTRMCRotationOverrideApproveView | custom/standard | None | IsAuthenticated, IsUTRMCAdminUser, CanApproveRotationOverride |
| GET | `api/certificates/my/` | PGCertificatesListView | custom/standard | None | IsAuthenticated, IsPGUser |
| POST | `api/certificates/my/` | PGCertificatesListView | custom/standard | None | IsAuthenticated, IsPGUser |
| PUT | `api/certificates/my/` | PGCertificatesListView | custom/standard | None | IsAuthenticated, IsPGUser |
| PATCH | `api/certificates/my/` | PGCertificatesListView | custom/standard | None | IsAuthenticated, IsPGUser |
| DELETE | `api/certificates/my/` | PGCertificatesListView | custom/standard | None | IsAuthenticated, IsPGUser |
| TRACE | `api/certificates/my/` | PGCertificatesListView | custom/standard | None | IsAuthenticated, IsPGUser |
| GET | `api/certificates/my/<int:pk>/download/` | PGCertificateDownloadView | custom/standard | None | IsAuthenticated, IsPGUser |
| POST | `api/certificates/my/<int:pk>/download/` | PGCertificateDownloadView | custom/standard | None | IsAuthenticated, IsPGUser |
| PUT | `api/certificates/my/<int:pk>/download/` | PGCertificateDownloadView | custom/standard | None | IsAuthenticated, IsPGUser |
| PATCH | `api/certificates/my/<int:pk>/download/` | PGCertificateDownloadView | custom/standard | None | IsAuthenticated, IsPGUser |
| DELETE | `api/certificates/my/<int:pk>/download/` | PGCertificateDownloadView | custom/standard | None | IsAuthenticated, IsPGUser |
| TRACE | `api/certificates/my/<int:pk>/download/` | PGCertificateDownloadView | custom/standard | None | IsAuthenticated, IsPGUser |
| GET | `api/attendance/upload/` | BulkAttendanceUploadView | custom/standard | None | IsAuthenticated |
| POST | `api/attendance/upload/` | BulkAttendanceUploadView | custom/standard | None | IsAuthenticated |
| PUT | `api/attendance/upload/` | BulkAttendanceUploadView | custom/standard | None | IsAuthenticated |
| PATCH | `api/attendance/upload/` | BulkAttendanceUploadView | custom/standard | None | IsAuthenticated |
| DELETE | `api/attendance/upload/` | BulkAttendanceUploadView | custom/standard | None | IsAuthenticated |
| TRACE | `api/attendance/upload/` | BulkAttendanceUploadView | custom/standard | None | IsAuthenticated |
| GET | `api/attendance/summary/` | AttendanceSummaryView | custom/standard | None | IsAuthenticated |
| POST | `api/attendance/summary/` | AttendanceSummaryView | custom/standard | None | IsAuthenticated |
| PUT | `api/attendance/summary/` | AttendanceSummaryView | custom/standard | None | IsAuthenticated |
| PATCH | `api/attendance/summary/` | AttendanceSummaryView | custom/standard | None | IsAuthenticated |
| DELETE | `api/attendance/summary/` | AttendanceSummaryView | custom/standard | None | IsAuthenticated |
| TRACE | `api/attendance/summary/` | AttendanceSummaryView | custom/standard | None | IsAuthenticated |
| GET | `api/users/assigned-pgs/` | SupervisorAssignedPGsView | custom/standard | None | IsAuthenticated, IsSupervisor |
| POST | `api/users/assigned-pgs/` | SupervisorAssignedPGsView | custom/standard | None | IsAuthenticated, IsSupervisor |
| PUT | `api/users/assigned-pgs/` | SupervisorAssignedPGsView | custom/standard | None | IsAuthenticated, IsSupervisor |
| PATCH | `api/users/assigned-pgs/` | SupervisorAssignedPGsView | custom/standard | None | IsAuthenticated, IsSupervisor |
| DELETE | `api/users/assigned-pgs/` | SupervisorAssignedPGsView | custom/standard | None | IsAuthenticated, IsSupervisor |
| TRACE | `api/users/assigned-pgs/` | SupervisorAssignedPGsView | custom/standard | None | IsAuthenticated, IsSupervisor |
| ANY | `academics/api/^departments/$` | DepartmentViewSet | func | None | None |
| ANY | `academics/api/^departments/(?P<pk>[^/.]+)/$` | DepartmentViewSet | func | None | None |
| ANY | `academics/api/^batches/$` | BatchViewSet | func | None | None |
| ANY | `academics/api/^batches/(?P<pk>[^/.]+)/$` | BatchViewSet | func | None | None |
| ANY | `academics/api/^batches/(?P<pk>[^/.]+)/students/$` | BatchViewSet | func | None | None |
| ANY | `academics/api/^students/$` | StudentProfileViewSet | func | None | None |
| ANY | `academics/api/^students/(?P<pk>[^/.]+)/$` | StudentProfileViewSet | func | None | None |
| ANY | `academics/api/^students/(?P<pk>[^/.]+)/update_status/$` | StudentProfileViewSet | func | None | None |
| GET | `academics/api/` | APIRootView | custom/standard | None | IsAuthenticated |
| POST | `academics/api/` | APIRootView | custom/standard | None | IsAuthenticated |
| PUT | `academics/api/` | APIRootView | custom/standard | None | IsAuthenticated |
| PATCH | `academics/api/` | APIRootView | custom/standard | None | IsAuthenticated |
| DELETE | `academics/api/` | APIRootView | custom/standard | None | IsAuthenticated |
| TRACE | `academics/api/` | APIRootView | custom/standard | None | IsAuthenticated |
| ANY | `results/api/^exams/$` | ExamViewSet | func | None | None |
| ANY | `results/api/^exams/(?P<pk>[^/.]+)/$` | ExamViewSet | func | None | None |
| ANY | `results/api/^exams/(?P<pk>[^/.]+)/scores/$` | ExamViewSet | func | None | None |
| ANY | `results/api/^exams/(?P<pk>[^/.]+)/statistics/$` | ExamViewSet | func | None | None |
| ANY | `results/api/^scores/$` | ScoreViewSet | func | None | None |
| ANY | `results/api/^scores/my_scores/$` | ScoreViewSet | func | None | None |
| ANY | `results/api/^scores/(?P<pk>[^/.]+)/$` | ScoreViewSet | func | None | None |
| GET | `results/api/` | APIRootView | custom/standard | None | IsAuthenticated |
| POST | `results/api/` | APIRootView | custom/standard | None | IsAuthenticated |
| PUT | `results/api/` | APIRootView | custom/standard | None | IsAuthenticated |
| PATCH | `results/api/` | APIRootView | custom/standard | None | IsAuthenticated |
| DELETE | `results/api/` | APIRootView | custom/standard | None | IsAuthenticated |
| TRACE | `results/api/` | APIRootView | custom/standard | None | IsAuthenticated |
| GET | `api/auth/login/` | CustomTokenObtainPairView | custom/standard | CustomTokenObtainPairSerializer | None |
| POST | `api/auth/login/` | CustomTokenObtainPairView | custom/standard | CustomTokenObtainPairSerializer | None |
| PUT | `api/auth/login/` | CustomTokenObtainPairView | custom/standard | CustomTokenObtainPairSerializer | None |
| PATCH | `api/auth/login/` | CustomTokenObtainPairView | custom/standard | CustomTokenObtainPairSerializer | None |
| DELETE | `api/auth/login/` | CustomTokenObtainPairView | custom/standard | CustomTokenObtainPairSerializer | None |
| TRACE | `api/auth/login/` | CustomTokenObtainPairView | custom/standard | CustomTokenObtainPairSerializer | None |
| GET | `api/auth/refresh/` | TokenRefreshView | custom/standard | None | None |
| POST | `api/auth/refresh/` | TokenRefreshView | custom/standard | None | None |
| PUT | `api/auth/refresh/` | TokenRefreshView | custom/standard | None | None |
| PATCH | `api/auth/refresh/` | TokenRefreshView | custom/standard | None | None |
| DELETE | `api/auth/refresh/` | TokenRefreshView | custom/standard | None | None |
| TRACE | `api/auth/refresh/` | TokenRefreshView | custom/standard | None | None |
| POST | `api/auth/logout/` | logout_view | custom/standard | None | IsAuthenticated |
| POST | `api/auth/register/` | register_view | custom/standard | None | AllowAny |
| GET | `api/auth/profile/` | user_profile_view | custom/standard | None | IsAuthenticated |
| PATCH | `api/auth/profile/update/` | update_profile_view | custom/standard | None | IsAuthenticated |
| PUT | `api/auth/profile/update/` | update_profile_view | custom/standard | None | IsAuthenticated |
| POST | `api/auth/password-reset/` | password_reset_request_view | custom/standard | None | AllowAny |
| POST | `api/auth/password-reset/confirm/` | password_reset_confirm_view | custom/standard | None | AllowAny |
| POST | `api/auth/change-password/` | change_password_view | custom/standard | None | IsAuthenticated |

## B) Frontend Inventory
| Method | URL | Caller File | Line | Adapter / Notes |
|---|---|---|---|---|
| GET | `/api/users/assigned-pgs/` | lib/api/users.ts | 15 | |
| GET | `/api/certificates/my/` | lib/api/certificates.ts | 22 | |
| POST | `/api/auth/login/` | lib/api/auth.ts | 59 | |
| POST | `/api/auth/register/` | lib/api/auth.ts | 67 | |
| POST | `/api/auth/logout/` | lib/api/auth.ts | 78 | |
| GET | `/api/auth/profile/` | lib/api/auth.ts | 97 | |
| POST | `/api/auth/refresh/` | lib/api/auth.ts | 106 | |
| PATCH | `/api/auth/profile/update/` | lib/api/auth.ts | 117 | |
| POST | `/api/auth/password-reset/` | lib/api/auth.ts | 126 | |
| POST | `/api/auth/password-reset/confirm/` | lib/api/auth.ts | 140 | |
| POST | `/api/auth/change-password/` | lib/api/auth.ts | 153 | |
| GET | `/api/logbook/pending/` | lib/api/logbook.ts | 68 | |
| POST | `/api/logbook/my/` | lib/api/logbook.ts | 100 | |
| PATCH | `/api/logbook/my/${id}/` | lib/api/logbook.ts | 108 | |
| POST | `/api/logbook/my/${id}/submit/` | lib/api/logbook.ts | 116 | |
| GET | `/api/attendance/summary/` | lib/api/attendance.ts | 38 | |
| POST | `/api/attendance/upload/` | lib/api/attendance.ts | 49 | |
| GET | `/api/search/` | lib/api/search.ts | 34 | |
| GET | `/api/search/history/` | lib/api/search.ts | 44 | |
| GET | `/api/search/suggestions/` | lib/api/search.ts | 52 | |
| GET | `/api/rotations/my/` | lib/api/rotations.ts | 25 | |
| GET | `/api/rotations/my/${id}/` | lib/api/rotations.ts | 33 | |
| GET | `/api/analytics/dashboard/overview/` | lib/api/analytics.ts | 42 | |
| GET | `/api/analytics/dashboard/trends/` | lib/api/analytics.ts | 50 | |
| GET | `/api/analytics/dashboard/compliance/` | lib/api/analytics.ts | 58 | |
| GET | `/api/analytics/performance/` | lib/api/analytics.ts | 66 | |
| POST | `/api/bulk/import/` | lib/api/bulk.ts | 38 | |
| POST | `/api/bulk/import-trainees/` | lib/api/bulk.ts | 53 | |
| POST | `/api/bulk/import-supervisors/` | lib/api/bulk.ts | 68 | |
| POST | `/api/bulk/import-residents/` | lib/api/bulk.ts | 83 | |
| POST | `/api/bulk/assignment/` | lib/api/bulk.ts | 95 | |
| POST | `/api/bulk/review/` | lib/api/bulk.ts | 103 | |
| GET | `/api/notifications/` | lib/api/notifications.ts | 30 | |
| GET | `/api/notifications/` | lib/api/notifications.ts | 39 | |
| GET | `/api/notifications/unread-count/` | lib/api/notifications.ts | 50 | |
| POST | `/api/notifications/mark-read/` | lib/api/notifications.ts | 59 | |
| GET | `/api/notifications/preferences/` | lib/api/notifications.ts | 69 | |
| PATCH | `/api/notifications/preferences/` | lib/api/notifications.ts | 77 | |
| GET | `/academics/api/departments/` | lib/api/academics.ts | 48 | |
| GET | `/academics/api/departments/${id}/` | lib/api/academics.ts | 52 | |
| POST | `/academics/api/departments/` | lib/api/academics.ts | 56 | |
| PUT | `/academics/api/departments/${id}/` | lib/api/academics.ts | 60 | |
| DELETE | `/academics/api/departments/${id}/` | lib/api/academics.ts | 64 | |
| GET | `/academics/api/batches/` | lib/api/academics.ts | 73 | |
| GET | `/academics/api/batches/${id}/` | lib/api/academics.ts | 77 | |
| POST | `/academics/api/batches/` | lib/api/academics.ts | 81 | |
| PUT | `/academics/api/batches/${id}/` | lib/api/academics.ts | 85 | |
| DELETE | `/academics/api/batches/${id}/` | lib/api/academics.ts | 89 | |
| GET | `/academics/api/batches/${id}/students/` | lib/api/academics.ts | 92 | |
| GET | `/academics/api/students/` | lib/api/academics.ts | 102 | |
| GET | `/academics/api/students/${id}/` | lib/api/academics.ts | 106 | |
| POST | `/academics/api/students/` | lib/api/academics.ts | 110 | |
| PUT | `/academics/api/students/${id}/` | lib/api/academics.ts | 114 | |
| DELETE | `/academics/api/students/${id}/` | lib/api/academics.ts | 118 | |
| POST | `/academics/api/students/${id}/update_status/` | lib/api/academics.ts | 121 | |
| GET | `/api/audit/activity/` | lib/api/audit.ts | 31 | |
| GET | `/api/audit/reports/` | lib/api/audit.ts | 39 | |
| POST | `/api/audit/reports/` | lib/api/audit.ts | 47 | |
| GET | `/results/api/exams/` | lib/api/results.ts | 54 | |
| GET | `/results/api/exams/${id}/` | lib/api/results.ts | 58 | |
| POST | `/results/api/exams/` | lib/api/results.ts | 62 | |
| PUT | `/results/api/exams/${id}/` | lib/api/results.ts | 66 | |
| DELETE | `/results/api/exams/${id}/` | lib/api/results.ts | 70 | |
| GET | `/results/api/exams/${id}/scores/` | lib/api/results.ts | 73 | |
| GET | `/results/api/exams/${id}/statistics/` | lib/api/results.ts | 77 | |
| GET | `/results/api/scores/` | lib/api/results.ts | 87 | |
| GET | `/results/api/scores/${id}/` | lib/api/results.ts | 91 | |
| POST | `/results/api/scores/` | lib/api/results.ts | 95 | |
| PUT | `/results/api/scores/${id}/` | lib/api/results.ts | 99 | |
| DELETE | `/results/api/scores/${id}/` | lib/api/results.ts | 103 | |
| GET | `/results/api/scores/my_scores/` | lib/api/results.ts | 106 | |
| GET | `/api/reports/templates/` | lib/api/reports.ts | 40 | |
| POST | `/api/reports/generate/` | lib/api/reports.ts | 48 | |
| GET | `/api/reports/scheduled/` | lib/api/reports.ts | 59 | |
| POST | `/api/reports/scheduled/` | lib/api/reports.ts | 67 | |
| GET | `/api/reports/scheduled/${id}/` | lib/api/reports.ts | 75 | |

## C) Bidirectional Cross-Link Map
### Backend to Frontend
- **ANY admin/auth/group/** -> [Django-admin-only]
- **ANY admin/auth/group/add/** -> [Django-admin-only]
- **ANY admin/auth/group/<path:object_id>/history/** -> [Django-admin-only]
- **ANY admin/auth/group/<path:object_id>/delete/** -> [Django-admin-only]
- **ANY admin/auth/group/<path:object_id>/change/** -> [Django-admin-only]
- **GET admin/auth/group/<path:object_id>/** -> [Django-admin-only]
- **POST admin/auth/group/<path:object_id>/** -> [Django-admin-only]
- **PUT admin/auth/group/<path:object_id>/** -> [Django-admin-only]
- **PATCH admin/auth/group/<path:object_id>/** -> [Django-admin-only]
- **DELETE admin/auth/group/<path:object_id>/** -> [Django-admin-only]
- **TRACE admin/auth/group/<path:object_id>/** -> [Django-admin-only]
- **GET users/api/users/search/** -> lib/api/search.ts (GET)
- **POST users/api/users/search/** -> [backend-only/future]
- **PUT users/api/users/search/** -> [backend-only/future]
- **PATCH users/api/users/search/** -> [backend-only/future]
- **DELETE users/api/users/search/** -> [backend-only/future]
- **TRACE users/api/users/search/** -> [backend-only/future]
- **GET users/api/supervisors/specialty/<str:specialty>/** -> [backend-only/future]
- **POST users/api/supervisors/specialty/<str:specialty>/** -> [backend-only/future]
- **PUT users/api/supervisors/specialty/<str:specialty>/** -> [backend-only/future]
- **PATCH users/api/supervisors/specialty/<str:specialty>/** -> [backend-only/future]
- **DELETE users/api/supervisors/specialty/<str:specialty>/** -> [backend-only/future]
- **TRACE users/api/supervisors/specialty/<str:specialty>/** -> [backend-only/future]
- **GET users/api/user/<int:pk>/stats/** -> [backend-only/future]
- **POST users/api/user/<int:pk>/stats/** -> [backend-only/future]
- **PUT users/api/user/<int:pk>/stats/** -> [backend-only/future]
- **PATCH users/api/user/<int:pk>/stats/** -> [backend-only/future]
- **DELETE users/api/user/<int:pk>/stats/** -> [backend-only/future]
- **TRACE users/api/user/<int:pk>/stats/** -> [backend-only/future]
- **GET users/api/stats/** -> [backend-only/future]
- **POST users/api/stats/** -> [backend-only/future]
- **PUT users/api/stats/** -> [backend-only/future]
- **PATCH users/api/stats/** -> [backend-only/future]
- **DELETE users/api/stats/** -> [backend-only/future]
- **TRACE users/api/stats/** -> [backend-only/future]
- **ANY users/api/admin/stats/** -> [Django-admin-only]
- **GET users/api/user-statistics/** -> [backend-only/future]
- **POST users/api/user-statistics/** -> [backend-only/future]
- **PUT users/api/user-statistics/** -> [backend-only/future]
- **PATCH users/api/user-statistics/** -> [backend-only/future]
- **DELETE users/api/user-statistics/** -> [backend-only/future]
- **TRACE users/api/user-statistics/** -> [backend-only/future]
- **GET users/api/user-performance/** -> [backend-only/future]
- **POST users/api/user-performance/** -> [backend-only/future]
- **PUT users/api/user-performance/** -> [backend-only/future]
- **PATCH users/api/user-performance/** -> [backend-only/future]
- **DELETE users/api/user-performance/** -> [backend-only/future]
- **TRACE users/api/user-performance/** -> [backend-only/future]
- **ANY rotations/api/calendar/** -> [backend-only/future]
- **ANY rotations/api/stats/** -> [backend-only/future]
- **ANY rotations/api/quick-stats/** -> [backend-only/future]
- **ANY rotations/api/departments/<int:hospital_id>/** -> [backend-only/future]
- **ANY certificates/api/stats/** -> [backend-only/future]
- **ANY certificates/api/quick-stats/** -> [backend-only/future]
- **ANY certificates/api/<int:pk>/verify/** -> [backend-only/future]
- **ANY certificates/api/update-statistics/** -> [backend-only/future]
- **ANY logbook/api/stats/** -> [backend-only/future]
- **ANY logbook/api/template/<int:template_id>/preview/** -> [backend-only/future]
- **ANY logbook/api/entry/<int:entry_id>/complexity/** -> [backend-only/future]
- **ANY logbook/api/update-statistics/** -> [backend-only/future]
- **ANY cases/api/diagnoses/** -> [backend-only/future]
- **ANY cases/api/procedures/** -> [backend-only/future]
- **ANY api/audit/^activity/$** -> lib/api/audit.ts (GET)
- **ANY api/audit/^activity/export/$** -> lib/api/audit.ts (GET)
- **ANY api/audit/^activity/(?P<pk>[^/.]+)/$** -> lib/api/audit.ts (GET)
- **ANY api/audit/^reports/$** -> lib/api/audit.ts (POST), lib/api/audit.ts (GET)
- **ANY api/audit/^reports/latest/$** -> lib/api/audit.ts (POST), lib/api/audit.ts (GET)
- **GET api/audit/** -> [system-only]
- **POST api/audit/** -> [system-only]
- **PUT api/audit/** -> [system-only]
- **PATCH api/audit/** -> [system-only]
- **DELETE api/audit/** -> [system-only]
- **TRACE api/audit/** -> [system-only]
- **GET api/search/** -> lib/api/search.ts (GET)
- **POST api/search/** -> [backend-only/future]
- **PUT api/search/** -> [backend-only/future]
- **PATCH api/search/** -> [backend-only/future]
- **DELETE api/search/** -> [backend-only/future]
- **TRACE api/search/** -> [backend-only/future]
- **GET api/search/history/** -> lib/api/search.ts (GET)
- **POST api/search/history/** -> [backend-only/future]
- **PUT api/search/history/** -> [backend-only/future]
- **PATCH api/search/history/** -> [backend-only/future]
- **DELETE api/search/history/** -> [backend-only/future]
- **TRACE api/search/history/** -> [backend-only/future]
- **GET api/search/suggestions/** -> lib/api/search.ts (GET)
- **POST api/search/suggestions/** -> [backend-only/future]
- **PUT api/search/suggestions/** -> [backend-only/future]
- **PATCH api/search/suggestions/** -> [backend-only/future]
- **DELETE api/search/suggestions/** -> [backend-only/future]
- **TRACE api/search/suggestions/** -> [backend-only/future]
- **GET api/analytics/trends/** -> [backend-only/future]
- **POST api/analytics/trends/** -> [backend-only/future]
- **PUT api/analytics/trends/** -> [backend-only/future]
- **PATCH api/analytics/trends/** -> [backend-only/future]
- **DELETE api/analytics/trends/** -> [backend-only/future]
- **TRACE api/analytics/trends/** -> [backend-only/future]
- **GET api/analytics/comparative/** -> [backend-only/future]
- **POST api/analytics/comparative/** -> [backend-only/future]
- **PUT api/analytics/comparative/** -> [backend-only/future]
- **PATCH api/analytics/comparative/** -> [backend-only/future]
- **DELETE api/analytics/comparative/** -> [backend-only/future]
- **TRACE api/analytics/comparative/** -> [backend-only/future]
- **GET api/analytics/performance/** -> lib/api/analytics.ts (GET)
- **POST api/analytics/performance/** -> [backend-only/future]
- **PUT api/analytics/performance/** -> [backend-only/future]
- **PATCH api/analytics/performance/** -> [backend-only/future]
- **DELETE api/analytics/performance/** -> [backend-only/future]
- **TRACE api/analytics/performance/** -> [backend-only/future]
- **GET api/analytics/dashboard/overview/** -> lib/api/analytics.ts (GET)
- **POST api/analytics/dashboard/overview/** -> [backend-only/future]
- **PUT api/analytics/dashboard/overview/** -> [backend-only/future]
- **PATCH api/analytics/dashboard/overview/** -> [backend-only/future]
- **DELETE api/analytics/dashboard/overview/** -> [backend-only/future]
- **TRACE api/analytics/dashboard/overview/** -> [backend-only/future]
- **GET api/analytics/dashboard/trends/** -> lib/api/analytics.ts (GET)
- **POST api/analytics/dashboard/trends/** -> [backend-only/future]
- **PUT api/analytics/dashboard/trends/** -> [backend-only/future]
- **PATCH api/analytics/dashboard/trends/** -> [backend-only/future]
- **DELETE api/analytics/dashboard/trends/** -> [backend-only/future]
- **TRACE api/analytics/dashboard/trends/** -> [backend-only/future]
- **GET api/analytics/dashboard/compliance/** -> lib/api/analytics.ts (GET)
- **POST api/analytics/dashboard/compliance/** -> [backend-only/future]
- **PUT api/analytics/dashboard/compliance/** -> [backend-only/future]
- **PATCH api/analytics/dashboard/compliance/** -> [backend-only/future]
- **DELETE api/analytics/dashboard/compliance/** -> [backend-only/future]
- **TRACE api/analytics/dashboard/compliance/** -> [backend-only/future]
- **GET api/bulk/review/** -> [backend-only/future]
- **POST api/bulk/review/** -> lib/api/bulk.ts (POST)
- **PUT api/bulk/review/** -> [backend-only/future]
- **PATCH api/bulk/review/** -> [backend-only/future]
- **DELETE api/bulk/review/** -> [backend-only/future]
- **TRACE api/bulk/review/** -> [backend-only/future]
- **GET api/bulk/assignment/** -> [backend-only/future]
- **POST api/bulk/assignment/** -> lib/api/bulk.ts (POST)
- **PUT api/bulk/assignment/** -> [backend-only/future]
- **PATCH api/bulk/assignment/** -> [backend-only/future]
- **DELETE api/bulk/assignment/** -> [backend-only/future]
- **TRACE api/bulk/assignment/** -> [backend-only/future]
- **GET api/bulk/import/** -> [backend-only/future]
- **POST api/bulk/import/** -> lib/api/bulk.ts (POST)
- **PUT api/bulk/import/** -> [backend-only/future]
- **PATCH api/bulk/import/** -> [backend-only/future]
- **DELETE api/bulk/import/** -> [backend-only/future]
- **TRACE api/bulk/import/** -> [backend-only/future]
- **GET api/bulk/import-trainees/** -> [backend-only/future]
- **POST api/bulk/import-trainees/** -> lib/api/bulk.ts (POST)
- **PUT api/bulk/import-trainees/** -> [backend-only/future]
- **PATCH api/bulk/import-trainees/** -> [backend-only/future]
- **DELETE api/bulk/import-trainees/** -> [backend-only/future]
- **TRACE api/bulk/import-trainees/** -> [backend-only/future]
- **GET api/bulk/import-supervisors/** -> [backend-only/future]
- **POST api/bulk/import-supervisors/** -> lib/api/bulk.ts (POST)
- **PUT api/bulk/import-supervisors/** -> [backend-only/future]
- **PATCH api/bulk/import-supervisors/** -> [backend-only/future]
- **DELETE api/bulk/import-supervisors/** -> [backend-only/future]
- **TRACE api/bulk/import-supervisors/** -> [backend-only/future]
- **GET api/bulk/import-residents/** -> [backend-only/future]
- **POST api/bulk/import-residents/** -> lib/api/bulk.ts (POST)
- **PUT api/bulk/import-residents/** -> [backend-only/future]
- **PATCH api/bulk/import-residents/** -> [backend-only/future]
- **DELETE api/bulk/import-residents/** -> [backend-only/future]
- **TRACE api/bulk/import-residents/** -> [backend-only/future]
- **GET api/notifications/** -> lib/api/notifications.ts (GET)
- **POST api/notifications/** -> [backend-only/future]
- **PUT api/notifications/** -> [backend-only/future]
- **PATCH api/notifications/** -> [backend-only/future]
- **DELETE api/notifications/** -> [backend-only/future]
- **TRACE api/notifications/** -> [backend-only/future]
- **GET api/notifications/mark-read/** -> lib/api/notifications.ts (GET)
- **POST api/notifications/mark-read/** -> lib/api/notifications.ts (POST)
- **PUT api/notifications/mark-read/** -> [backend-only/future]
- **PATCH api/notifications/mark-read/** -> [backend-only/future]
- **DELETE api/notifications/mark-read/** -> [backend-only/future]
- **TRACE api/notifications/mark-read/** -> [backend-only/future]
- **GET api/notifications/preferences/** -> lib/api/notifications.ts (GET)
- **POST api/notifications/preferences/** -> [backend-only/future]
- **PUT api/notifications/preferences/** -> [backend-only/future]
- **PATCH api/notifications/preferences/** -> lib/api/notifications.ts (PATCH)
- **DELETE api/notifications/preferences/** -> [backend-only/future]
- **TRACE api/notifications/preferences/** -> [backend-only/future]
- **GET api/notifications/unread-count/** -> lib/api/notifications.ts (GET)
- **POST api/notifications/unread-count/** -> [backend-only/future]
- **PUT api/notifications/unread-count/** -> [backend-only/future]
- **PATCH api/notifications/unread-count/** -> [backend-only/future]
- **DELETE api/notifications/unread-count/** -> [backend-only/future]
- **TRACE api/notifications/unread-count/** -> [backend-only/future]
- **GET api/reports/templates/** -> lib/api/reports.ts (GET)
- **POST api/reports/templates/** -> [backend-only/future]
- **PUT api/reports/templates/** -> [backend-only/future]
- **PATCH api/reports/templates/** -> [backend-only/future]
- **DELETE api/reports/templates/** -> [backend-only/future]
- **TRACE api/reports/templates/** -> [backend-only/future]
- **GET api/reports/generate/** -> [backend-only/future]
- **POST api/reports/generate/** -> lib/api/reports.ts (POST)
- **PUT api/reports/generate/** -> [backend-only/future]
- **PATCH api/reports/generate/** -> [backend-only/future]
- **DELETE api/reports/generate/** -> [backend-only/future]
- **TRACE api/reports/generate/** -> [backend-only/future]
- **GET api/reports/scheduled/** -> lib/api/reports.ts (GET)
- **POST api/reports/scheduled/** -> lib/api/reports.ts (POST)
- **PUT api/reports/scheduled/** -> [backend-only/future]
- **PATCH api/reports/scheduled/** -> [backend-only/future]
- **DELETE api/reports/scheduled/** -> [backend-only/future]
- **TRACE api/reports/scheduled/** -> [backend-only/future]
- **GET api/reports/scheduled/<int:pk>/** -> lib/api/reports.ts (GET)
- **POST api/reports/scheduled/<int:pk>/** -> lib/api/reports.ts (POST)
- **PUT api/reports/scheduled/<int:pk>/** -> [backend-only/future]
- **PATCH api/reports/scheduled/<int:pk>/** -> [backend-only/future]
- **DELETE api/reports/scheduled/<int:pk>/** -> [backend-only/future]
- **TRACE api/reports/scheduled/<int:pk>/** -> [backend-only/future]
- **GET api/logbook/pending/** -> lib/api/logbook.ts (GET)
- **POST api/logbook/pending/** -> [backend-only/future]
- **PUT api/logbook/pending/** -> [backend-only/future]
- **PATCH api/logbook/pending/** -> [backend-only/future]
- **DELETE api/logbook/pending/** -> [backend-only/future]
- **TRACE api/logbook/pending/** -> [backend-only/future]
- **GET api/logbook/<int:pk>/verify/** -> [backend-only/future]
- **POST api/logbook/<int:pk>/verify/** -> [backend-only/future]
- **PUT api/logbook/<int:pk>/verify/** -> [backend-only/future]
- **PATCH api/logbook/<int:pk>/verify/** -> [backend-only/future]
- **DELETE api/logbook/<int:pk>/verify/** -> [backend-only/future]
- **TRACE api/logbook/<int:pk>/verify/** -> [backend-only/future]
- **GET api/logbook/my/** -> [backend-only/future]
- **POST api/logbook/my/** -> lib/api/logbook.ts (POST)
- **PUT api/logbook/my/** -> [backend-only/future]
- **PATCH api/logbook/my/** -> [backend-only/future]
- **DELETE api/logbook/my/** -> [backend-only/future]
- **TRACE api/logbook/my/** -> [backend-only/future]
- **GET api/logbook/my/<int:pk>/** -> [backend-only/future]
- **POST api/logbook/my/<int:pk>/** -> lib/api/logbook.ts (POST)
- **PUT api/logbook/my/<int:pk>/** -> [backend-only/future]
- **PATCH api/logbook/my/<int:pk>/** -> lib/api/logbook.ts (PATCH)
- **DELETE api/logbook/my/<int:pk>/** -> [backend-only/future]
- **TRACE api/logbook/my/<int:pk>/** -> [backend-only/future]
- **GET api/logbook/my/<int:pk>/submit/** -> [backend-only/future]
- **POST api/logbook/my/<int:pk>/submit/** -> lib/api/logbook.ts (POST)
- **PUT api/logbook/my/<int:pk>/submit/** -> [backend-only/future]
- **PATCH api/logbook/my/<int:pk>/submit/** -> lib/api/logbook.ts (PATCH)
- **DELETE api/logbook/my/<int:pk>/submit/** -> [backend-only/future]
- **TRACE api/logbook/my/<int:pk>/submit/** -> [backend-only/future]
- **ANY api/rotations/^hospitals/$** -> [backend-only/future]
- **ANY api/rotations/^hospitals/(?P<pk>[^/.]+)/$** -> [backend-only/future]
- **ANY api/rotations/^hospital-departments/$** -> [backend-only/future]
- **ANY api/rotations/^hospital-departments/(?P<pk>[^/.]+)/$** -> [backend-only/future]
- **GET api/rotations/** -> [system-only]
- **POST api/rotations/** -> [system-only]
- **PUT api/rotations/** -> [system-only]
- **PATCH api/rotations/** -> [system-only]
- **DELETE api/rotations/** -> [system-only]
- **TRACE api/rotations/** -> [system-only]
- **GET api/rotations/my/** -> lib/api/rotations.ts (GET)
- **POST api/rotations/my/** -> [backend-only/future]
- **PUT api/rotations/my/** -> [backend-only/future]
- **PATCH api/rotations/my/** -> [backend-only/future]
- **DELETE api/rotations/my/** -> [backend-only/future]
- **TRACE api/rotations/my/** -> [backend-only/future]
- **GET api/rotations/my/<int:pk>/** -> lib/api/rotations.ts (GET)
- **POST api/rotations/my/<int:pk>/** -> [backend-only/future]
- **PUT api/rotations/my/<int:pk>/** -> [backend-only/future]
- **PATCH api/rotations/my/<int:pk>/** -> [backend-only/future]
- **DELETE api/rotations/my/<int:pk>/** -> [backend-only/future]
- **TRACE api/rotations/my/<int:pk>/** -> [backend-only/future]
- **GET api/rotations/<int:pk>/utrmc-approve/** -> [backend-only/future]
- **POST api/rotations/<int:pk>/utrmc-approve/** -> [backend-only/future]
- **PUT api/rotations/<int:pk>/utrmc-approve/** -> [backend-only/future]
- **PATCH api/rotations/<int:pk>/utrmc-approve/** -> [backend-only/future]
- **DELETE api/rotations/<int:pk>/utrmc-approve/** -> [backend-only/future]
- **TRACE api/rotations/<int:pk>/utrmc-approve/** -> [backend-only/future]
- **GET api/certificates/my/** -> lib/api/certificates.ts (GET)
- **POST api/certificates/my/** -> [backend-only/future]
- **PUT api/certificates/my/** -> [backend-only/future]
- **PATCH api/certificates/my/** -> [backend-only/future]
- **DELETE api/certificates/my/** -> [backend-only/future]
- **TRACE api/certificates/my/** -> [backend-only/future]
- **GET api/certificates/my/<int:pk>/download/** -> lib/api/certificates.ts (GET)
- **POST api/certificates/my/<int:pk>/download/** -> [backend-only/future]
- **PUT api/certificates/my/<int:pk>/download/** -> [backend-only/future]
- **PATCH api/certificates/my/<int:pk>/download/** -> [backend-only/future]
- **DELETE api/certificates/my/<int:pk>/download/** -> [backend-only/future]
- **TRACE api/certificates/my/<int:pk>/download/** -> [backend-only/future]
- **GET api/attendance/upload/** -> [backend-only/future]
- **POST api/attendance/upload/** -> lib/api/attendance.ts (POST)
- **PUT api/attendance/upload/** -> [backend-only/future]
- **PATCH api/attendance/upload/** -> [backend-only/future]
- **DELETE api/attendance/upload/** -> [backend-only/future]
- **TRACE api/attendance/upload/** -> [backend-only/future]
- **GET api/attendance/summary/** -> lib/api/attendance.ts (GET)
- **POST api/attendance/summary/** -> [backend-only/future]
- **PUT api/attendance/summary/** -> [backend-only/future]
- **PATCH api/attendance/summary/** -> [backend-only/future]
- **DELETE api/attendance/summary/** -> [backend-only/future]
- **TRACE api/attendance/summary/** -> [backend-only/future]
- **GET api/users/assigned-pgs/** -> lib/api/users.ts (GET)
- **POST api/users/assigned-pgs/** -> [backend-only/future]
- **PUT api/users/assigned-pgs/** -> [backend-only/future]
- **PATCH api/users/assigned-pgs/** -> [backend-only/future]
- **DELETE api/users/assigned-pgs/** -> [backend-only/future]
- **TRACE api/users/assigned-pgs/** -> [backend-only/future]
- **ANY academics/api/^departments/$** -> lib/api/academics.ts (POST), lib/api/academics.ts (DELETE), lib/api/academics.ts (GET), lib/api/academics.ts (PUT)
- **ANY academics/api/^departments/(?P<pk>[^/.]+)/$** -> lib/api/academics.ts (POST), lib/api/academics.ts (GET)
- **ANY academics/api/^batches/$** -> lib/api/academics.ts (POST), lib/api/academics.ts (DELETE), lib/api/academics.ts (GET), lib/api/academics.ts (PUT)
- **ANY academics/api/^batches/(?P<pk>[^/.]+)/$** -> lib/api/academics.ts (POST), lib/api/academics.ts (GET)
- **ANY academics/api/^batches/(?P<pk>[^/.]+)/students/$** -> lib/api/academics.ts (POST), lib/api/academics.ts (GET)
- **ANY academics/api/^students/$** -> lib/api/academics.ts (POST), lib/api/academics.ts (DELETE), lib/api/academics.ts (GET), lib/api/academics.ts (PUT)
- **ANY academics/api/^students/(?P<pk>[^/.]+)/$** -> lib/api/academics.ts (POST), lib/api/academics.ts (GET)
- **ANY academics/api/^students/(?P<pk>[^/.]+)/update_status/$** -> lib/api/academics.ts (POST), lib/api/academics.ts (GET)
- **GET academics/api/** -> lib/api/academics.ts (GET)
- **POST academics/api/** -> lib/api/academics.ts (POST)
- **PUT academics/api/** -> lib/api/academics.ts (PUT)
- **PATCH academics/api/** -> [system-only]
- **DELETE academics/api/** -> lib/api/academics.ts (DELETE)
- **TRACE academics/api/** -> [system-only]
- **ANY results/api/^exams/$** -> lib/api/results.ts (POST), lib/api/results.ts (GET), lib/api/results.ts (PUT), lib/api/results.ts (DELETE)
- **ANY results/api/^exams/(?P<pk>[^/.]+)/$** -> lib/api/results.ts (POST), lib/api/results.ts (GET)
- **ANY results/api/^exams/(?P<pk>[^/.]+)/scores/$** -> lib/api/results.ts (POST), lib/api/results.ts (GET)
- **ANY results/api/^exams/(?P<pk>[^/.]+)/statistics/$** -> lib/api/results.ts (POST), lib/api/results.ts (GET)
- **ANY results/api/^scores/$** -> lib/api/results.ts (POST), lib/api/results.ts (GET), lib/api/results.ts (PUT), lib/api/results.ts (DELETE)
- **ANY results/api/^scores/my_scores/$** -> lib/api/results.ts (POST), lib/api/results.ts (GET)
- **ANY results/api/^scores/(?P<pk>[^/.]+)/$** -> lib/api/results.ts (POST), lib/api/results.ts (GET)
- **GET results/api/** -> lib/api/results.ts (GET)
- **POST results/api/** -> lib/api/results.ts (POST)
- **PUT results/api/** -> lib/api/results.ts (PUT)
- **PATCH results/api/** -> [system-only]
- **DELETE results/api/** -> lib/api/results.ts (DELETE)
- **TRACE results/api/** -> [system-only]
- **GET api/auth/login/** -> [backend-only/future]
- **POST api/auth/login/** -> lib/api/auth.ts (POST)
- **PUT api/auth/login/** -> [backend-only/future]
- **PATCH api/auth/login/** -> [backend-only/future]
- **DELETE api/auth/login/** -> [backend-only/future]
- **TRACE api/auth/login/** -> [backend-only/future]
- **GET api/auth/refresh/** -> [backend-only/future]
- **POST api/auth/refresh/** -> lib/api/auth.ts (POST)
- **PUT api/auth/refresh/** -> [backend-only/future]
- **PATCH api/auth/refresh/** -> [backend-only/future]
- **DELETE api/auth/refresh/** -> [backend-only/future]
- **TRACE api/auth/refresh/** -> [backend-only/future]
- **POST api/auth/logout/** -> lib/api/auth.ts (POST)
- **POST api/auth/register/** -> lib/api/auth.ts (POST)
- **GET api/auth/profile/** -> lib/api/auth.ts (GET)
- **PATCH api/auth/profile/update/** -> lib/api/auth.ts (PATCH)
- **PUT api/auth/profile/update/** -> [backend-only/future]
- **POST api/auth/password-reset/** -> lib/api/auth.ts (POST)
- **POST api/auth/password-reset/confirm/** -> lib/api/auth.ts (POST)
- **POST api/auth/change-password/** -> lib/api/auth.ts (POST)

### Frontend to Backend
- **GET /api/users/assigned-pgs/** in `lib/api/users.ts` -> `api/users/assigned-pgs/`
- **GET /api/certificates/my/** in `lib/api/certificates.ts` -> `api/certificates/my/`, `api/certificates/my/<int:pk>/download/`
- **POST /api/auth/login/** in `lib/api/auth.ts` -> `api/auth/login/`
- **POST /api/auth/register/** in `lib/api/auth.ts` -> `api/auth/register/`
- **POST /api/auth/logout/** in `lib/api/auth.ts` -> `api/auth/logout/`
- **GET /api/auth/profile/** in `lib/api/auth.ts` -> `api/auth/profile/`
- **POST /api/auth/refresh/** in `lib/api/auth.ts` -> `api/auth/refresh/`
- **PATCH /api/auth/profile/update/** in `lib/api/auth.ts` -> `api/auth/profile/update/`
- **POST /api/auth/password-reset/** in `lib/api/auth.ts` -> `api/auth/password-reset/`, `api/auth/password-reset/confirm/`
- **POST /api/auth/password-reset/confirm/** in `lib/api/auth.ts` -> `api/auth/password-reset/confirm/`
- **POST /api/auth/change-password/** in `lib/api/auth.ts` -> `api/auth/change-password/`
- **GET /api/logbook/pending/** in `lib/api/logbook.ts` -> `api/logbook/pending/`
- **POST /api/logbook/my/** in `lib/api/logbook.ts` -> `api/logbook/my/`, `api/logbook/my/<int:pk>/`, `api/logbook/my/<int:pk>/submit/`
- **PATCH /api/logbook/my/${id}/** in `lib/api/logbook.ts` -> `api/logbook/my/<int:pk>/`, `api/logbook/my/<int:pk>/submit/`
- **POST /api/logbook/my/${id}/submit/** in `lib/api/logbook.ts` -> `api/logbook/my/<int:pk>/submit/`
- **GET /api/attendance/summary/** in `lib/api/attendance.ts` -> `api/attendance/summary/`
- **POST /api/attendance/upload/** in `lib/api/attendance.ts` -> `api/attendance/upload/`
- **GET /api/search/** in `lib/api/search.ts` -> `users/api/users/search/`, `api/search/`, `api/search/history/`, `api/search/suggestions/`
- **GET /api/search/history/** in `lib/api/search.ts` -> `api/search/history/`
- **GET /api/search/suggestions/** in `lib/api/search.ts` -> `api/search/suggestions/`
- **GET /api/rotations/my/** in `lib/api/rotations.ts` -> `api/rotations/my/`, `api/rotations/my/<int:pk>/`
- **GET /api/rotations/my/${id}/** in `lib/api/rotations.ts` -> `api/rotations/my/<int:pk>/`
- **GET /api/analytics/dashboard/overview/** in `lib/api/analytics.ts` -> `api/analytics/dashboard/overview/`
- **GET /api/analytics/dashboard/trends/** in `lib/api/analytics.ts` -> `api/analytics/dashboard/trends/`
- **GET /api/analytics/dashboard/compliance/** in `lib/api/analytics.ts` -> `api/analytics/dashboard/compliance/`
- **GET /api/analytics/performance/** in `lib/api/analytics.ts` -> `api/analytics/performance/`
- **POST /api/bulk/import/** in `lib/api/bulk.ts` -> `api/bulk/import/`, `api/bulk/import-trainees/`, `api/bulk/import-supervisors/`, `api/bulk/import-residents/`
- **POST /api/bulk/import-trainees/** in `lib/api/bulk.ts` -> `api/bulk/import-trainees/`
- **POST /api/bulk/import-supervisors/** in `lib/api/bulk.ts` -> `api/bulk/import-supervisors/`
- **POST /api/bulk/import-residents/** in `lib/api/bulk.ts` -> `api/bulk/import-residents/`
- **POST /api/bulk/assignment/** in `lib/api/bulk.ts` -> `api/bulk/assignment/`
- **POST /api/bulk/review/** in `lib/api/bulk.ts` -> `api/bulk/review/`
- **GET /api/notifications/** in `lib/api/notifications.ts` -> `api/notifications/`, `api/notifications/mark-read/`, `api/notifications/preferences/`, `api/notifications/unread-count/`
- **GET /api/notifications/** in `lib/api/notifications.ts` -> `api/notifications/`, `api/notifications/mark-read/`, `api/notifications/preferences/`, `api/notifications/unread-count/`
- **GET /api/notifications/unread-count/** in `lib/api/notifications.ts` -> `api/notifications/unread-count/`
- **POST /api/notifications/mark-read/** in `lib/api/notifications.ts` -> `api/notifications/mark-read/`
- **GET /api/notifications/preferences/** in `lib/api/notifications.ts` -> `api/notifications/preferences/`
- **PATCH /api/notifications/preferences/** in `lib/api/notifications.ts` -> `api/notifications/preferences/`
- **GET /academics/api/departments/** in `lib/api/academics.ts` -> `academics/api/^departments/$`, `academics/api/^departments\.(?P<format>[a-z0-9]+)/?$`, `academics/api/^departments/(?P<pk>[^/.]+)/$`, `academics/api/^departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `academics/api/`
- **GET /academics/api/departments/${id}/** in `lib/api/academics.ts` -> `academics/api/^departments/$`, `academics/api/`
- **POST /academics/api/departments/** in `lib/api/academics.ts` -> `academics/api/^departments/$`, `academics/api/^departments\.(?P<format>[a-z0-9]+)/?$`, `academics/api/^departments/(?P<pk>[^/.]+)/$`, `academics/api/^departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `academics/api/`
- **PUT /academics/api/departments/${id}/** in `lib/api/academics.ts` -> `academics/api/^departments/$`, `academics/api/`
- **DELETE /academics/api/departments/${id}/** in `lib/api/academics.ts` -> `academics/api/^departments/$`, `academics/api/`
- **GET /academics/api/batches/** in `lib/api/academics.ts` -> `academics/api/^batches/$`, `academics/api/^batches\.(?P<format>[a-z0-9]+)/?$`, `academics/api/^batches/(?P<pk>[^/.]+)/$`, `academics/api/^batches/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `academics/api/^batches/(?P<pk>[^/.]+)/students/$`, `academics/api/^batches/(?P<pk>[^/.]+)/students\.(?P<format>[a-z0-9]+)/?$`, `academics/api/`
- **GET /academics/api/batches/${id}/** in `lib/api/academics.ts` -> `academics/api/^batches/$`, `academics/api/`
- **POST /academics/api/batches/** in `lib/api/academics.ts` -> `academics/api/^batches/$`, `academics/api/^batches\.(?P<format>[a-z0-9]+)/?$`, `academics/api/^batches/(?P<pk>[^/.]+)/$`, `academics/api/^batches/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `academics/api/^batches/(?P<pk>[^/.]+)/students/$`, `academics/api/^batches/(?P<pk>[^/.]+)/students\.(?P<format>[a-z0-9]+)/?$`, `academics/api/`
- **PUT /academics/api/batches/${id}/** in `lib/api/academics.ts` -> `academics/api/^batches/$`, `academics/api/`
- **DELETE /academics/api/batches/${id}/** in `lib/api/academics.ts` -> `academics/api/^batches/$`, `academics/api/`
- **GET /academics/api/batches/${id}/students/** in `lib/api/academics.ts` -> `academics/api/^batches/$`, `academics/api/`
- **GET /academics/api/students/** in `lib/api/academics.ts` -> `academics/api/^students/$`, `academics/api/^students\.(?P<format>[a-z0-9]+)/?$`, `academics/api/^students/(?P<pk>[^/.]+)/$`, `academics/api/^students/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `academics/api/^students/(?P<pk>[^/.]+)/update_status/$`, `academics/api/^students/(?P<pk>[^/.]+)/update_status\.(?P<format>[a-z0-9]+)/?$`, `academics/api/`
- **GET /academics/api/students/${id}/** in `lib/api/academics.ts` -> `academics/api/^students/$`, `academics/api/`
- **POST /academics/api/students/** in `lib/api/academics.ts` -> `academics/api/^students/$`, `academics/api/^students\.(?P<format>[a-z0-9]+)/?$`, `academics/api/^students/(?P<pk>[^/.]+)/$`, `academics/api/^students/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `academics/api/^students/(?P<pk>[^/.]+)/update_status/$`, `academics/api/^students/(?P<pk>[^/.]+)/update_status\.(?P<format>[a-z0-9]+)/?$`, `academics/api/`
- **PUT /academics/api/students/${id}/** in `lib/api/academics.ts` -> `academics/api/^students/$`, `academics/api/`
- **DELETE /academics/api/students/${id}/** in `lib/api/academics.ts` -> `academics/api/^students/$`, `academics/api/`
- **POST /academics/api/students/${id}/update_status/** in `lib/api/academics.ts` -> `academics/api/^students/$`, `academics/api/`
- **GET /api/audit/activity/** in `lib/api/audit.ts` -> `api/audit/^activity/$`, `api/audit/^activity\.(?P<format>[a-z0-9]+)/?$`, `api/audit/^activity/export/$`, `api/audit/^activity/export\.(?P<format>[a-z0-9]+)/?$`, `api/audit/^activity/(?P<pk>[^/.]+)/$`, `api/audit/^activity/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`
- **GET /api/audit/reports/** in `lib/api/audit.ts` -> `api/audit/^reports/$`, `api/audit/^reports\.(?P<format>[a-z0-9]+)/?$`, `api/audit/^reports/latest/$`, `api/audit/^reports/latest\.(?P<format>[a-z0-9]+)/?$`
- **POST /api/audit/reports/** in `lib/api/audit.ts` -> `api/audit/^reports/$`, `api/audit/^reports\.(?P<format>[a-z0-9]+)/?$`, `api/audit/^reports/latest/$`, `api/audit/^reports/latest\.(?P<format>[a-z0-9]+)/?$`
- **GET /results/api/exams/** in `lib/api/results.ts` -> `results/api/^exams/$`, `results/api/^exams\.(?P<format>[a-z0-9]+)/?$`, `results/api/^exams/(?P<pk>[^/.]+)/$`, `results/api/^exams/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `results/api/^exams/(?P<pk>[^/.]+)/scores/$`, `results/api/^exams/(?P<pk>[^/.]+)/scores\.(?P<format>[a-z0-9]+)/?$`, `results/api/^exams/(?P<pk>[^/.]+)/statistics/$`, `results/api/^exams/(?P<pk>[^/.]+)/statistics\.(?P<format>[a-z0-9]+)/?$`, `results/api/`
- **GET /results/api/exams/${id}/** in `lib/api/results.ts` -> `results/api/^exams/$`, `results/api/`
- **POST /results/api/exams/** in `lib/api/results.ts` -> `results/api/^exams/$`, `results/api/^exams\.(?P<format>[a-z0-9]+)/?$`, `results/api/^exams/(?P<pk>[^/.]+)/$`, `results/api/^exams/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `results/api/^exams/(?P<pk>[^/.]+)/scores/$`, `results/api/^exams/(?P<pk>[^/.]+)/scores\.(?P<format>[a-z0-9]+)/?$`, `results/api/^exams/(?P<pk>[^/.]+)/statistics/$`, `results/api/^exams/(?P<pk>[^/.]+)/statistics\.(?P<format>[a-z0-9]+)/?$`, `results/api/`
- **PUT /results/api/exams/${id}/** in `lib/api/results.ts` -> `results/api/^exams/$`, `results/api/`
- **DELETE /results/api/exams/${id}/** in `lib/api/results.ts` -> `results/api/^exams/$`, `results/api/`
- **GET /results/api/exams/${id}/scores/** in `lib/api/results.ts` -> `results/api/^exams/$`, `results/api/`
- **GET /results/api/exams/${id}/statistics/** in `lib/api/results.ts` -> `results/api/^exams/$`, `results/api/`
- **GET /results/api/scores/** in `lib/api/results.ts` -> `results/api/^scores/$`, `results/api/^scores\.(?P<format>[a-z0-9]+)/?$`, `results/api/^scores/my_scores/$`, `results/api/^scores/my_scores\.(?P<format>[a-z0-9]+)/?$`, `results/api/^scores/(?P<pk>[^/.]+)/$`, `results/api/^scores/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `results/api/`
- **GET /results/api/scores/${id}/** in `lib/api/results.ts` -> `results/api/^scores/$`, `results/api/`
- **POST /results/api/scores/** in `lib/api/results.ts` -> `results/api/^scores/$`, `results/api/^scores\.(?P<format>[a-z0-9]+)/?$`, `results/api/^scores/my_scores/$`, `results/api/^scores/my_scores\.(?P<format>[a-z0-9]+)/?$`, `results/api/^scores/(?P<pk>[^/.]+)/$`, `results/api/^scores/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `results/api/`
- **PUT /results/api/scores/${id}/** in `lib/api/results.ts` -> `results/api/^scores/$`, `results/api/`
- **DELETE /results/api/scores/${id}/** in `lib/api/results.ts` -> `results/api/^scores/$`, `results/api/`
- **GET /results/api/scores/my_scores/** in `lib/api/results.ts` -> `results/api/^scores/$`, `results/api/^scores/my_scores/$`, `results/api/^scores/my_scores\.(?P<format>[a-z0-9]+)/?$`, `results/api/`
- **GET /api/reports/templates/** in `lib/api/reports.ts` -> `api/reports/templates/`
- **POST /api/reports/generate/** in `lib/api/reports.ts` -> `api/reports/generate/`
- **GET /api/reports/scheduled/** in `lib/api/reports.ts` -> `api/reports/scheduled/`, `api/reports/scheduled/<int:pk>/`
- **POST /api/reports/scheduled/** in `lib/api/reports.ts` -> `api/reports/scheduled/`, `api/reports/scheduled/<int:pk>/`
- **GET /api/reports/scheduled/${id}/** in `lib/api/reports.ts` -> `api/reports/scheduled/<int:pk>/`

## D) Payload/Contract Alignment
- **Logbook workflow**: Frontend uses `logbookAdapter.ts` which normalizes `feedback`, `supervisor_feedback`, and `supervisor_comments` into `feedback_text`. Status maps 'pending' requests.
- **Rotations**: Frontend uses `rotationAdapter.ts` to normalize `hospital` and `department` nested objects or string IDs uniformly into `{id, name}`.
- **Status terminology**: Matches using adapters.

## E) RBAC + Route Gating Alignment
- Checked `middleware.ts` which confirms strict role routing checking tokens and `pgsims_access_exp`:
  - `/dashboard/pg/*` -> `pg` role
  - `/dashboard/supervisor/*` -> `supervisor` role
  - `/dashboard/utrmc/*` -> `utrmc_user` / `utrmc_admin`
  - `/dashboard/admin/*` -> `admin`
- Unauthenticated or expired tokens redirect to `/login` and clear cookies.

## F) GAPS / DRIFT RISKS
### 1) Unmapped Backend Routes
- `POST users/api/users/search/` - Reason: [backend-only/future]
- `PUT users/api/users/search/` - Reason: [backend-only/future]
- `PATCH users/api/users/search/` - Reason: [backend-only/future]
- `DELETE users/api/users/search/` - Reason: [backend-only/future]
- `TRACE users/api/users/search/` - Reason: [backend-only/future]
- `GET users/api/supervisors/specialty/<str:specialty>/` - Reason: [backend-only/future]
- `POST users/api/supervisors/specialty/<str:specialty>/` - Reason: [backend-only/future]
- `PUT users/api/supervisors/specialty/<str:specialty>/` - Reason: [backend-only/future]
- `PATCH users/api/supervisors/specialty/<str:specialty>/` - Reason: [backend-only/future]
- `DELETE users/api/supervisors/specialty/<str:specialty>/` - Reason: [backend-only/future]
- `TRACE users/api/supervisors/specialty/<str:specialty>/` - Reason: [backend-only/future]
- `GET users/api/user/<int:pk>/stats/` - Reason: [backend-only/future]
- `POST users/api/user/<int:pk>/stats/` - Reason: [backend-only/future]
- `PUT users/api/user/<int:pk>/stats/` - Reason: [backend-only/future]
- `PATCH users/api/user/<int:pk>/stats/` - Reason: [backend-only/future]
- `DELETE users/api/user/<int:pk>/stats/` - Reason: [backend-only/future]
- `TRACE users/api/user/<int:pk>/stats/` - Reason: [backend-only/future]
- `GET users/api/stats/` - Reason: [backend-only/future]
- `POST users/api/stats/` - Reason: [backend-only/future]
- `PUT users/api/stats/` - Reason: [backend-only/future]

- *All frontend calls matched a backend endpoint.*

## G) Verdict
**PASS**. All static frontend API calls map successfully.
