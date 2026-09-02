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
| ANY | `logbook/api/stats/` | dummy_redirect | func | None | None |
| ANY | `logbook/api/template/<int:template_id>/preview/` | dummy_redirect | func | None | None |
| ANY | `logbook/api/entry/<int:entry_id>/complexity/` | dummy_redirect | func | None | None |
| ANY | `logbook/api/update-statistics/` | dummy_redirect | func | None | None |
| ANY | `rotations/api/departments/<int:hospital_id>/` | department_by_hospital_api | func | None | None |
| ANY | `rotations/api/quick-stats/` | dummy_redirect | func | None | None |
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
| GET | `api/bulk/review/` | BulkReviewView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| POST | `api/bulk/review/` | BulkReviewView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| PUT | `api/bulk/review/` | BulkReviewView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| PATCH | `api/bulk/review/` | BulkReviewView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| DELETE | `api/bulk/review/` | BulkReviewView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| TRACE | `api/bulk/review/` | BulkReviewView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| GET | `api/bulk/assignment/` | BulkAssignmentView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| POST | `api/bulk/assignment/` | BulkAssignmentView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| PUT | `api/bulk/assignment/` | BulkAssignmentView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| PATCH | `api/bulk/assignment/` | BulkAssignmentView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| DELETE | `api/bulk/assignment/` | BulkAssignmentView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| TRACE | `api/bulk/assignment/` | BulkAssignmentView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| GET | `api/bulk/import/` | BulkImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| POST | `api/bulk/import/` | BulkImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| PUT | `api/bulk/import/` | BulkImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| PATCH | `api/bulk/import/` | BulkImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| DELETE | `api/bulk/import/` | BulkImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| TRACE | `api/bulk/import/` | BulkImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| GET | `api/bulk/import-trainees/` | BulkTraineeImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| POST | `api/bulk/import-trainees/` | BulkTraineeImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| PUT | `api/bulk/import-trainees/` | BulkTraineeImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| PATCH | `api/bulk/import-trainees/` | BulkTraineeImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| DELETE | `api/bulk/import-trainees/` | BulkTraineeImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| TRACE | `api/bulk/import-trainees/` | BulkTraineeImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| GET | `api/bulk/import-supervisors/` | BulkSupervisorImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| POST | `api/bulk/import-supervisors/` | BulkSupervisorImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| PUT | `api/bulk/import-supervisors/` | BulkSupervisorImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| PATCH | `api/bulk/import-supervisors/` | BulkSupervisorImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| DELETE | `api/bulk/import-supervisors/` | BulkSupervisorImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| TRACE | `api/bulk/import-supervisors/` | BulkSupervisorImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| GET | `api/bulk/import-residents/` | BulkResidentImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| POST | `api/bulk/import-residents/` | BulkResidentImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| PUT | `api/bulk/import-residents/` | BulkResidentImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| PATCH | `api/bulk/import-residents/` | BulkResidentImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| DELETE | `api/bulk/import-residents/` | BulkResidentImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| TRACE | `api/bulk/import-residents/` | BulkResidentImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| GET | `api/bulk/import-departments/` | BulkDepartmentImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| POST | `api/bulk/import-departments/` | BulkDepartmentImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| PUT | `api/bulk/import-departments/` | BulkDepartmentImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| PATCH | `api/bulk/import-departments/` | BulkDepartmentImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| DELETE | `api/bulk/import-departments/` | BulkDepartmentImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| TRACE | `api/bulk/import-departments/` | BulkDepartmentImportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| GET | `api/bulk/exports/<str:resource>/` | BulkExportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| POST | `api/bulk/exports/<str:resource>/` | BulkExportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| PUT | `api/bulk/exports/<str:resource>/` | BulkExportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| PATCH | `api/bulk/exports/<str:resource>/` | BulkExportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| DELETE | `api/bulk/exports/<str:resource>/` | BulkExportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| TRACE | `api/bulk/exports/<str:resource>/` | BulkExportView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| GET | `api/bulk/templates/<str:resource>/` | BulkTemplateView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| POST | `api/bulk/templates/<str:resource>/` | BulkTemplateView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| PUT | `api/bulk/templates/<str:resource>/` | BulkTemplateView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| PATCH | `api/bulk/templates/<str:resource>/` | BulkTemplateView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| DELETE | `api/bulk/templates/<str:resource>/` | BulkTemplateView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| TRACE | `api/bulk/templates/<str:resource>/` | BulkTemplateView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| GET | `api/bulk/import/<str:entity>/<str:action>/` | BulkImportEntityView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| POST | `api/bulk/import/<str:entity>/<str:action>/` | BulkImportEntityView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| PUT | `api/bulk/import/<str:entity>/<str:action>/` | BulkImportEntityView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| PATCH | `api/bulk/import/<str:entity>/<str:action>/` | BulkImportEntityView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| DELETE | `api/bulk/import/<str:entity>/<str:action>/` | BulkImportEntityView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| TRACE | `api/bulk/import/<str:entity>/<str:action>/` | BulkImportEntityView | custom/standard | BulkEmptySchemaSerializer | IsAuthenticated |
| GET | `api/bulk/flexible/schemas/` | FlexibleSchemasView | custom/standard | None | IsAuthenticated |
| POST | `api/bulk/flexible/schemas/` | FlexibleSchemasView | custom/standard | None | IsAuthenticated |
| PUT | `api/bulk/flexible/schemas/` | FlexibleSchemasView | custom/standard | None | IsAuthenticated |
| PATCH | `api/bulk/flexible/schemas/` | FlexibleSchemasView | custom/standard | None | IsAuthenticated |
| DELETE | `api/bulk/flexible/schemas/` | FlexibleSchemasView | custom/standard | None | IsAuthenticated |
| TRACE | `api/bulk/flexible/schemas/` | FlexibleSchemasView | custom/standard | None | IsAuthenticated |
| GET | `api/bulk/flexible/detect-headers/` | FlexibleDetectHeadersView | custom/standard | None | IsAuthenticated |
| POST | `api/bulk/flexible/detect-headers/` | FlexibleDetectHeadersView | custom/standard | None | IsAuthenticated |
| PUT | `api/bulk/flexible/detect-headers/` | FlexibleDetectHeadersView | custom/standard | None | IsAuthenticated |
| PATCH | `api/bulk/flexible/detect-headers/` | FlexibleDetectHeadersView | custom/standard | None | IsAuthenticated |
| DELETE | `api/bulk/flexible/detect-headers/` | FlexibleDetectHeadersView | custom/standard | None | IsAuthenticated |
| TRACE | `api/bulk/flexible/detect-headers/` | FlexibleDetectHeadersView | custom/standard | None | IsAuthenticated |
| GET | `api/bulk/flexible/validate-mapping/` | FlexibleValidateMappingView | custom/standard | None | IsAuthenticated |
| POST | `api/bulk/flexible/validate-mapping/` | FlexibleValidateMappingView | custom/standard | None | IsAuthenticated |
| PUT | `api/bulk/flexible/validate-mapping/` | FlexibleValidateMappingView | custom/standard | None | IsAuthenticated |
| PATCH | `api/bulk/flexible/validate-mapping/` | FlexibleValidateMappingView | custom/standard | None | IsAuthenticated |
| DELETE | `api/bulk/flexible/validate-mapping/` | FlexibleValidateMappingView | custom/standard | None | IsAuthenticated |
| TRACE | `api/bulk/flexible/validate-mapping/` | FlexibleValidateMappingView | custom/standard | None | IsAuthenticated |
| GET | `api/bulk/flexible/dry-run/` | FlexibleDryRunView | custom/standard | None | IsAuthenticated |
| POST | `api/bulk/flexible/dry-run/` | FlexibleDryRunView | custom/standard | None | IsAuthenticated |
| PUT | `api/bulk/flexible/dry-run/` | FlexibleDryRunView | custom/standard | None | IsAuthenticated |
| PATCH | `api/bulk/flexible/dry-run/` | FlexibleDryRunView | custom/standard | None | IsAuthenticated |
| DELETE | `api/bulk/flexible/dry-run/` | FlexibleDryRunView | custom/standard | None | IsAuthenticated |
| TRACE | `api/bulk/flexible/dry-run/` | FlexibleDryRunView | custom/standard | None | IsAuthenticated |
| GET | `api/bulk/flexible/apply/` | FlexibleImportApplyView | custom/standard | None | IsAuthenticated |
| POST | `api/bulk/flexible/apply/` | FlexibleImportApplyView | custom/standard | None | IsAuthenticated |
| PUT | `api/bulk/flexible/apply/` | FlexibleImportApplyView | custom/standard | None | IsAuthenticated |
| PATCH | `api/bulk/flexible/apply/` | FlexibleImportApplyView | custom/standard | None | IsAuthenticated |
| DELETE | `api/bulk/flexible/apply/` | FlexibleImportApplyView | custom/standard | None | IsAuthenticated |
| TRACE | `api/bulk/flexible/apply/` | FlexibleImportApplyView | custom/standard | None | IsAuthenticated |
| ANY | `api/bulk/flexible/presets/` | MappingPresetViewSet | func | None | None |
| ANY | `api/bulk/flexible/presets/<int:pk>/` | MappingPresetViewSet | func | None | None |
| GET | `api/notifications/` | NotificationListView | custom/standard | NotificationSerializer | IsAuthenticated |
| POST | `api/notifications/` | NotificationListView | custom/standard | NotificationSerializer | IsAuthenticated |
| PUT | `api/notifications/` | NotificationListView | custom/standard | NotificationSerializer | IsAuthenticated |
| PATCH | `api/notifications/` | NotificationListView | custom/standard | NotificationSerializer | IsAuthenticated |
| DELETE | `api/notifications/` | NotificationListView | custom/standard | NotificationSerializer | IsAuthenticated |
| TRACE | `api/notifications/` | NotificationListView | custom/standard | NotificationSerializer | IsAuthenticated |
| GET | `api/notifications/mark-read/` | NotificationMarkReadView | custom/standard | NotificationEmptySchemaSerializer | IsAuthenticated |
| POST | `api/notifications/mark-read/` | NotificationMarkReadView | custom/standard | NotificationEmptySchemaSerializer | IsAuthenticated |
| PUT | `api/notifications/mark-read/` | NotificationMarkReadView | custom/standard | NotificationEmptySchemaSerializer | IsAuthenticated |
| PATCH | `api/notifications/mark-read/` | NotificationMarkReadView | custom/standard | NotificationEmptySchemaSerializer | IsAuthenticated |
| DELETE | `api/notifications/mark-read/` | NotificationMarkReadView | custom/standard | NotificationEmptySchemaSerializer | IsAuthenticated |
| TRACE | `api/notifications/mark-read/` | NotificationMarkReadView | custom/standard | NotificationEmptySchemaSerializer | IsAuthenticated |
| GET | `api/notifications/preferences/` | NotificationPreferenceView | custom/standard | NotificationPreferenceSerializer | IsAuthenticated |
| POST | `api/notifications/preferences/` | NotificationPreferenceView | custom/standard | NotificationPreferenceSerializer | IsAuthenticated |
| PUT | `api/notifications/preferences/` | NotificationPreferenceView | custom/standard | NotificationPreferenceSerializer | IsAuthenticated |
| PATCH | `api/notifications/preferences/` | NotificationPreferenceView | custom/standard | NotificationPreferenceSerializer | IsAuthenticated |
| DELETE | `api/notifications/preferences/` | NotificationPreferenceView | custom/standard | NotificationPreferenceSerializer | IsAuthenticated |
| TRACE | `api/notifications/preferences/` | NotificationPreferenceView | custom/standard | NotificationPreferenceSerializer | IsAuthenticated |
| GET | `api/notifications/unread-count/` | NotificationUnreadCountView | custom/standard | NotificationEmptySchemaSerializer | IsAuthenticated |
| POST | `api/notifications/unread-count/` | NotificationUnreadCountView | custom/standard | NotificationEmptySchemaSerializer | IsAuthenticated |
| PUT | `api/notifications/unread-count/` | NotificationUnreadCountView | custom/standard | NotificationEmptySchemaSerializer | IsAuthenticated |
| PATCH | `api/notifications/unread-count/` | NotificationUnreadCountView | custom/standard | NotificationEmptySchemaSerializer | IsAuthenticated |
| DELETE | `api/notifications/unread-count/` | NotificationUnreadCountView | custom/standard | NotificationEmptySchemaSerializer | IsAuthenticated |
| TRACE | `api/notifications/unread-count/` | NotificationUnreadCountView | custom/standard | NotificationEmptySchemaSerializer | IsAuthenticated |
| GET | `api/schema/` | SpectacularAPIView | custom/standard | None | AllowAny |
| POST | `api/schema/` | SpectacularAPIView | custom/standard | None | AllowAny |
| PUT | `api/schema/` | SpectacularAPIView | custom/standard | None | AllowAny |
| PATCH | `api/schema/` | SpectacularAPIView | custom/standard | None | AllowAny |
| DELETE | `api/schema/` | SpectacularAPIView | custom/standard | None | AllowAny |
| TRACE | `api/schema/` | SpectacularAPIView | custom/standard | None | AllowAny |
| ANY | `api/^hospitals/$` | HospitalViewSet | func | None | None |
| ANY | `api/^hospitals/(?P<pk>[^/.]+)/$` | HospitalViewSet | func | None | None |
| ANY | `api/^hospitals/(?P<pk>[^/.]+)/departments/$` | HospitalViewSet | func | None | None |
| ANY | `api/^departments/$` | DepartmentViewSet | func | None | None |
| ANY | `api/^departments/(?P<pk>[^/.]+)/$` | DepartmentViewSet | func | None | None |
| ANY | `api/^departments/(?P<pk>[^/.]+)/roster/$` | DepartmentViewSet | func | None | None |
| ANY | `api/^hospital-departments/$` | HospitalDepartmentViewSet | func | None | None |
| ANY | `api/^hospital-departments/(?P<pk>[^/.]+)/$` | HospitalDepartmentViewSet | func | None | None |
| ANY | `api/^residents/$` | ResidentProfileViewSet | func | None | None |
| ANY | `api/^residents/(?P<user_id>[^/.]+)/$` | ResidentProfileViewSet | func | None | None |
| ANY | `api/^staff/$` | StaffProfileViewSet | func | None | None |
| ANY | `api/^staff/(?P<user_id>[^/.]+)/$` | StaffProfileViewSet | func | None | None |
| ANY | `api/^department-memberships/$` | DepartmentMembershipViewSet | func | None | None |
| ANY | `api/^department-memberships/(?P<pk>[^/.]+)/$` | DepartmentMembershipViewSet | func | None | None |
| ANY | `api/^hospital-assignments/$` | HospitalAssignmentViewSet | func | None | None |
| ANY | `api/^hospital-assignments/(?P<pk>[^/.]+)/$` | HospitalAssignmentViewSet | func | None | None |
| ANY | `api/^supervision-links/$` | SupervisionLinkViewSet | func | None | None |
| ANY | `api/^supervision-links/(?P<pk>[^/.]+)/$` | SupervisionLinkViewSet | func | None | None |
| ANY | `api/^hod-assignments/$` | HODAssignmentViewSet | func | None | None |
| ANY | `api/^hod-assignments/(?P<pk>[^/.]+)/$` | HODAssignmentViewSet | func | None | None |
| GET | `api/` | APIRootView | custom/standard | None | IsAuthenticated |
| POST | `api/` | APIRootView | custom/standard | None | IsAuthenticated |
| PUT | `api/` | APIRootView | custom/standard | None | IsAuthenticated |
| PATCH | `api/` | APIRootView | custom/standard | None | IsAuthenticated |
| DELETE | `api/` | APIRootView | custom/standard | None | IsAuthenticated |
| TRACE | `api/` | APIRootView | custom/standard | None | IsAuthenticated |
| GET | `api/admin/data-quality/summary` | DataQualitySummaryView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| POST | `api/admin/data-quality/summary` | DataQualitySummaryView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| PUT | `api/admin/data-quality/summary` | DataQualitySummaryView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| PATCH | `api/admin/data-quality/summary` | DataQualitySummaryView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| DELETE | `api/admin/data-quality/summary` | DataQualitySummaryView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| TRACE | `api/admin/data-quality/summary` | DataQualitySummaryView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| GET | `api/admin/data-quality/users` | DataQualityUsersView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| POST | `api/admin/data-quality/users` | DataQualityUsersView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| PUT | `api/admin/data-quality/users` | DataQualityUsersView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| PATCH | `api/admin/data-quality/users` | DataQualityUsersView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| DELETE | `api/admin/data-quality/users` | DataQualityUsersView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| TRACE | `api/admin/data-quality/users` | DataQualityUsersView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| GET | `api/admin/data-quality/recompute` | DataQualityRecomputeView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| POST | `api/admin/data-quality/recompute` | DataQualityRecomputeView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| PUT | `api/admin/data-quality/recompute` | DataQualityRecomputeView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| PATCH | `api/admin/data-quality/recompute` | DataQualityRecomputeView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| DELETE | `api/admin/data-quality/recompute` | DataQualityRecomputeView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| TRACE | `api/admin/data-quality/recompute` | DataQualityRecomputeView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| GET | `api/admin/data-quality/audit` | DataCorrectionAuditView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| POST | `api/admin/data-quality/audit` | DataCorrectionAuditView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| PUT | `api/admin/data-quality/audit` | DataCorrectionAuditView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| PATCH | `api/admin/data-quality/audit` | DataCorrectionAuditView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| DELETE | `api/admin/data-quality/audit` | DataCorrectionAuditView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| TRACE | `api/admin/data-quality/audit` | DataCorrectionAuditView | custom/standard | UserbaseEmptySchemaSerializer | IsAuthenticated |
| GET | `api/users/assigned-pgs/` | SupervisorAssignedPGsView | custom/standard | AssignedPGSerializer | IsAuthenticated, IsSupervisor |
| POST | `api/users/assigned-pgs/` | SupervisorAssignedPGsView | custom/standard | AssignedPGSerializer | IsAuthenticated, IsSupervisor |
| PUT | `api/users/assigned-pgs/` | SupervisorAssignedPGsView | custom/standard | AssignedPGSerializer | IsAuthenticated, IsSupervisor |
| PATCH | `api/users/assigned-pgs/` | SupervisorAssignedPGsView | custom/standard | AssignedPGSerializer | IsAuthenticated, IsSupervisor |
| DELETE | `api/users/assigned-pgs/` | SupervisorAssignedPGsView | custom/standard | AssignedPGSerializer | IsAuthenticated, IsSupervisor |
| TRACE | `api/users/assigned-pgs/` | SupervisorAssignedPGsView | custom/standard | AssignedPGSerializer | IsAuthenticated, IsSupervisor |
| ANY | `api/users/^$` | UserViewSet | func | None | None |
| ANY | `api/users/^(?P<pk>[^/.]+)/$` | UserViewSet | func | None | None |
| GET | `api/users/` | APIRootView | custom/standard | None | IsAuthenticated |
| POST | `api/users/` | APIRootView | custom/standard | None | IsAuthenticated |
| PUT | `api/users/` | APIRootView | custom/standard | None | IsAuthenticated |
| PATCH | `api/users/` | APIRootView | custom/standard | None | IsAuthenticated |
| DELETE | `api/users/` | APIRootView | custom/standard | None | IsAuthenticated |
| TRACE | `api/users/` | APIRootView | custom/standard | None | IsAuthenticated |
| GET | `api/programs/<int:program_id>/policy/` | ProgramPolicyView | custom/standard | ProgramPolicySerializer | IsAuthenticated |
| POST | `api/programs/<int:program_id>/policy/` | ProgramPolicyView | custom/standard | ProgramPolicySerializer | IsAuthenticated |
| PUT | `api/programs/<int:program_id>/policy/` | ProgramPolicyView | custom/standard | ProgramPolicySerializer | IsAuthenticated |
| PATCH | `api/programs/<int:program_id>/policy/` | ProgramPolicyView | custom/standard | ProgramPolicySerializer | IsAuthenticated |
| DELETE | `api/programs/<int:program_id>/policy/` | ProgramPolicyView | custom/standard | ProgramPolicySerializer | IsAuthenticated |
| TRACE | `api/programs/<int:program_id>/policy/` | ProgramPolicyView | custom/standard | ProgramPolicySerializer | IsAuthenticated |
| ANY | `api/programs/<int:program_id>/milestones/^$` | ProgramMilestoneViewSet | func | None | None |
| ANY | `api/programs/<int:program_id>/milestones/^(?P<pk>[^/.]+)/$` | ProgramMilestoneViewSet | func | None | None |
| GET | `api/programs/<int:program_id>/milestones/` | APIRootView | custom/standard | None | IsAuthenticated |
| POST | `api/programs/<int:program_id>/milestones/` | APIRootView | custom/standard | None | IsAuthenticated |
| PUT | `api/programs/<int:program_id>/milestones/` | APIRootView | custom/standard | None | IsAuthenticated |
| PATCH | `api/programs/<int:program_id>/milestones/` | APIRootView | custom/standard | None | IsAuthenticated |
| DELETE | `api/programs/<int:program_id>/milestones/` | APIRootView | custom/standard | None | IsAuthenticated |
| TRACE | `api/programs/<int:program_id>/milestones/` | APIRootView | custom/standard | None | IsAuthenticated |
| GET | `api/milestones/<int:milestone_id>/requirements/research/` | MilestoneResearchRequirementView | custom/standard | ProgramMilestoneResearchRequirementSerializer | IsAuthenticated |
| POST | `api/milestones/<int:milestone_id>/requirements/research/` | MilestoneResearchRequirementView | custom/standard | ProgramMilestoneResearchRequirementSerializer | IsAuthenticated |
| PUT | `api/milestones/<int:milestone_id>/requirements/research/` | MilestoneResearchRequirementView | custom/standard | ProgramMilestoneResearchRequirementSerializer | IsAuthenticated |
| PATCH | `api/milestones/<int:milestone_id>/requirements/research/` | MilestoneResearchRequirementView | custom/standard | ProgramMilestoneResearchRequirementSerializer | IsAuthenticated |
| DELETE | `api/milestones/<int:milestone_id>/requirements/research/` | MilestoneResearchRequirementView | custom/standard | ProgramMilestoneResearchRequirementSerializer | IsAuthenticated |
| TRACE | `api/milestones/<int:milestone_id>/requirements/research/` | MilestoneResearchRequirementView | custom/standard | ProgramMilestoneResearchRequirementSerializer | IsAuthenticated |
| GET | `api/utrmc/approvals/rotations/` | RotationApprovalInboxView | custom/standard | RotationAssignmentSerializer | IsAuthenticated |
| POST | `api/utrmc/approvals/rotations/` | RotationApprovalInboxView | custom/standard | RotationAssignmentSerializer | IsAuthenticated |
| PUT | `api/utrmc/approvals/rotations/` | RotationApprovalInboxView | custom/standard | RotationAssignmentSerializer | IsAuthenticated |
| PATCH | `api/utrmc/approvals/rotations/` | RotationApprovalInboxView | custom/standard | RotationAssignmentSerializer | IsAuthenticated |
| DELETE | `api/utrmc/approvals/rotations/` | RotationApprovalInboxView | custom/standard | RotationAssignmentSerializer | IsAuthenticated |
| TRACE | `api/utrmc/approvals/rotations/` | RotationApprovalInboxView | custom/standard | RotationAssignmentSerializer | IsAuthenticated |
| GET | `api/utrmc/approvals/leaves/` | LeaveApprovalInboxView | custom/standard | LeaveRequestSerializer | IsAuthenticated |
| POST | `api/utrmc/approvals/leaves/` | LeaveApprovalInboxView | custom/standard | LeaveRequestSerializer | IsAuthenticated |
| PUT | `api/utrmc/approvals/leaves/` | LeaveApprovalInboxView | custom/standard | LeaveRequestSerializer | IsAuthenticated |
| PATCH | `api/utrmc/approvals/leaves/` | LeaveApprovalInboxView | custom/standard | LeaveRequestSerializer | IsAuthenticated |
| DELETE | `api/utrmc/approvals/leaves/` | LeaveApprovalInboxView | custom/standard | LeaveRequestSerializer | IsAuthenticated |
| TRACE | `api/utrmc/approvals/leaves/` | LeaveApprovalInboxView | custom/standard | LeaveRequestSerializer | IsAuthenticated |
| GET | `api/utrmc/eligibility/` | UTRMCEligibilityView | custom/standard | ResidentMilestoneEligibilitySerializer | IsAuthenticated |
| POST | `api/utrmc/eligibility/` | UTRMCEligibilityView | custom/standard | ResidentMilestoneEligibilitySerializer | IsAuthenticated |
| PUT | `api/utrmc/eligibility/` | UTRMCEligibilityView | custom/standard | ResidentMilestoneEligibilitySerializer | IsAuthenticated |
| PATCH | `api/utrmc/eligibility/` | UTRMCEligibilityView | custom/standard | ResidentMilestoneEligibilitySerializer | IsAuthenticated |
| DELETE | `api/utrmc/eligibility/` | UTRMCEligibilityView | custom/standard | ResidentMilestoneEligibilitySerializer | IsAuthenticated |
| TRACE | `api/utrmc/eligibility/` | UTRMCEligibilityView | custom/standard | ResidentMilestoneEligibilitySerializer | IsAuthenticated |
| GET | `api/my/rotations/` | MyRotationsView | custom/standard | RotationAssignmentSerializer | IsAuthenticated |
| POST | `api/my/rotations/` | MyRotationsView | custom/standard | RotationAssignmentSerializer | IsAuthenticated |
| PUT | `api/my/rotations/` | MyRotationsView | custom/standard | RotationAssignmentSerializer | IsAuthenticated |
| PATCH | `api/my/rotations/` | MyRotationsView | custom/standard | RotationAssignmentSerializer | IsAuthenticated |
| DELETE | `api/my/rotations/` | MyRotationsView | custom/standard | RotationAssignmentSerializer | IsAuthenticated |
| TRACE | `api/my/rotations/` | MyRotationsView | custom/standard | RotationAssignmentSerializer | IsAuthenticated |
| GET | `api/my/leaves/` | MyLeavesView | custom/standard | LeaveRequestSerializer | IsAuthenticated |
| POST | `api/my/leaves/` | MyLeavesView | custom/standard | LeaveRequestSerializer | IsAuthenticated |
| PUT | `api/my/leaves/` | MyLeavesView | custom/standard | LeaveRequestSerializer | IsAuthenticated |
| PATCH | `api/my/leaves/` | MyLeavesView | custom/standard | LeaveRequestSerializer | IsAuthenticated |
| DELETE | `api/my/leaves/` | MyLeavesView | custom/standard | LeaveRequestSerializer | IsAuthenticated |
| TRACE | `api/my/leaves/` | MyLeavesView | custom/standard | LeaveRequestSerializer | IsAuthenticated |
| GET | `api/my/research/` | ResidentResearchProjectView | custom/standard | ResidentResearchProjectSerializer | IsAuthenticated |
| POST | `api/my/research/` | ResidentResearchProjectView | custom/standard | ResidentResearchProjectSerializer | IsAuthenticated |
| PUT | `api/my/research/` | ResidentResearchProjectView | custom/standard | ResidentResearchProjectSerializer | IsAuthenticated |
| PATCH | `api/my/research/` | ResidentResearchProjectView | custom/standard | ResidentResearchProjectSerializer | IsAuthenticated |
| DELETE | `api/my/research/` | ResidentResearchProjectView | custom/standard | ResidentResearchProjectSerializer | IsAuthenticated |
| TRACE | `api/my/research/` | ResidentResearchProjectView | custom/standard | ResidentResearchProjectSerializer | IsAuthenticated |
| GET | `api/my/research/action/<str:action>/` | ResearchProjectActionView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| POST | `api/my/research/action/<str:action>/` | ResearchProjectActionView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| PUT | `api/my/research/action/<str:action>/` | ResearchProjectActionView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| PATCH | `api/my/research/action/<str:action>/` | ResearchProjectActionView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| DELETE | `api/my/research/action/<str:action>/` | ResearchProjectActionView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| TRACE | `api/my/research/action/<str:action>/` | ResearchProjectActionView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| GET | `api/my/thesis/` | ResidentThesisView | custom/standard | ResidentThesisSerializer | IsAuthenticated |
| POST | `api/my/thesis/` | ResidentThesisView | custom/standard | ResidentThesisSerializer | IsAuthenticated |
| PUT | `api/my/thesis/` | ResidentThesisView | custom/standard | ResidentThesisSerializer | IsAuthenticated |
| PATCH | `api/my/thesis/` | ResidentThesisView | custom/standard | ResidentThesisSerializer | IsAuthenticated |
| DELETE | `api/my/thesis/` | ResidentThesisView | custom/standard | ResidentThesisSerializer | IsAuthenticated |
| TRACE | `api/my/thesis/` | ResidentThesisView | custom/standard | ResidentThesisSerializer | IsAuthenticated |
| GET | `api/my/thesis/submit/` | ThesisSubmitView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| POST | `api/my/thesis/submit/` | ThesisSubmitView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| PUT | `api/my/thesis/submit/` | ThesisSubmitView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| PATCH | `api/my/thesis/submit/` | ThesisSubmitView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| DELETE | `api/my/thesis/submit/` | ThesisSubmitView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| TRACE | `api/my/thesis/submit/` | ThesisSubmitView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| GET | `api/my/workshops/` | MyWorkshopCompletionsView | custom/standard | ResidentWorkshopCompletionSerializer | IsAuthenticated |
| POST | `api/my/workshops/` | MyWorkshopCompletionsView | custom/standard | ResidentWorkshopCompletionSerializer | IsAuthenticated |
| PUT | `api/my/workshops/` | MyWorkshopCompletionsView | custom/standard | ResidentWorkshopCompletionSerializer | IsAuthenticated |
| PATCH | `api/my/workshops/` | MyWorkshopCompletionsView | custom/standard | ResidentWorkshopCompletionSerializer | IsAuthenticated |
| DELETE | `api/my/workshops/` | MyWorkshopCompletionsView | custom/standard | ResidentWorkshopCompletionSerializer | IsAuthenticated |
| TRACE | `api/my/workshops/` | MyWorkshopCompletionsView | custom/standard | ResidentWorkshopCompletionSerializer | IsAuthenticated |
| GET | `api/my/workshops/<int:pk>/` | MyWorkshopCompletionDetailView | custom/standard | ResidentWorkshopCompletionSerializer | IsAuthenticated |
| POST | `api/my/workshops/<int:pk>/` | MyWorkshopCompletionDetailView | custom/standard | ResidentWorkshopCompletionSerializer | IsAuthenticated |
| PUT | `api/my/workshops/<int:pk>/` | MyWorkshopCompletionDetailView | custom/standard | ResidentWorkshopCompletionSerializer | IsAuthenticated |
| PATCH | `api/my/workshops/<int:pk>/` | MyWorkshopCompletionDetailView | custom/standard | ResidentWorkshopCompletionSerializer | IsAuthenticated |
| DELETE | `api/my/workshops/<int:pk>/` | MyWorkshopCompletionDetailView | custom/standard | ResidentWorkshopCompletionSerializer | IsAuthenticated |
| TRACE | `api/my/workshops/<int:pk>/` | MyWorkshopCompletionDetailView | custom/standard | ResidentWorkshopCompletionSerializer | IsAuthenticated |
| GET | `api/my/eligibility/` | MyEligibilityView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| POST | `api/my/eligibility/` | MyEligibilityView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| PUT | `api/my/eligibility/` | MyEligibilityView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| PATCH | `api/my/eligibility/` | MyEligibilityView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| DELETE | `api/my/eligibility/` | MyEligibilityView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| TRACE | `api/my/eligibility/` | MyEligibilityView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| GET | `api/logbook/review-queue/` | LogbookReviewQueueView | custom/standard | LogbookEntrySerializer | IsAuthenticated |
| POST | `api/logbook/review-queue/` | LogbookReviewQueueView | custom/standard | LogbookEntrySerializer | IsAuthenticated |
| PUT | `api/logbook/review-queue/` | LogbookReviewQueueView | custom/standard | LogbookEntrySerializer | IsAuthenticated |
| PATCH | `api/logbook/review-queue/` | LogbookReviewQueueView | custom/standard | LogbookEntrySerializer | IsAuthenticated |
| DELETE | `api/logbook/review-queue/` | LogbookReviewQueueView | custom/standard | LogbookEntrySerializer | IsAuthenticated |
| TRACE | `api/logbook/review-queue/` | LogbookReviewQueueView | custom/standard | LogbookEntrySerializer | IsAuthenticated |
| GET | `api/logbook/my-threshold/` | LogbookMyThresholdView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| POST | `api/logbook/my-threshold/` | LogbookMyThresholdView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| PUT | `api/logbook/my-threshold/` | LogbookMyThresholdView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| PATCH | `api/logbook/my-threshold/` | LogbookMyThresholdView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| DELETE | `api/logbook/my-threshold/` | LogbookMyThresholdView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| TRACE | `api/logbook/my-threshold/` | LogbookMyThresholdView | custom/standard | TrainingEmptySchemaSerializer | IsAuthenticated |
| GET | `api/submissions/synopsis/` | SynopsisSubmissionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| POST | `api/submissions/synopsis/` | SynopsisSubmissionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| PUT | `api/submissions/synopsis/` | SynopsisSubmissionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| PATCH | `api/submissions/synopsis/` | SynopsisSubmissionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| DELETE | `api/submissions/synopsis/` | SynopsisSubmissionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| TRACE | `api/submissions/synopsis/` | SynopsisSubmissionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| GET | `api/submissions/synopsis/documents/` | SynopsisSubmissionDocumentsView | custom/standard | SubmissionDocumentSerializer | IsAuthenticated |
| POST | `api/submissions/synopsis/documents/` | SynopsisSubmissionDocumentsView | custom/standard | SubmissionDocumentSerializer | IsAuthenticated |
| PUT | `api/submissions/synopsis/documents/` | SynopsisSubmissionDocumentsView | custom/standard | SubmissionDocumentSerializer | IsAuthenticated |
| PATCH | `api/submissions/synopsis/documents/` | SynopsisSubmissionDocumentsView | custom/standard | SubmissionDocumentSerializer | IsAuthenticated |
| DELETE | `api/submissions/synopsis/documents/` | SynopsisSubmissionDocumentsView | custom/standard | SubmissionDocumentSerializer | IsAuthenticated |
| TRACE | `api/submissions/synopsis/documents/` | SynopsisSubmissionDocumentsView | custom/standard | SubmissionDocumentSerializer | IsAuthenticated |
| GET | `api/submissions/synopsis/submit/` | SynopsisSubmissionSubmitView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| POST | `api/submissions/synopsis/submit/` | SynopsisSubmissionSubmitView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| PUT | `api/submissions/synopsis/submit/` | SynopsisSubmissionSubmitView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| PATCH | `api/submissions/synopsis/submit/` | SynopsisSubmissionSubmitView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| DELETE | `api/submissions/synopsis/submit/` | SynopsisSubmissionSubmitView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| TRACE | `api/submissions/synopsis/submit/` | SynopsisSubmissionSubmitView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| GET | `api/submissions/synopsis/review-queue/` | SynopsisReviewQueueView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| POST | `api/submissions/synopsis/review-queue/` | SynopsisReviewQueueView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| PUT | `api/submissions/synopsis/review-queue/` | SynopsisReviewQueueView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| PATCH | `api/submissions/synopsis/review-queue/` | SynopsisReviewQueueView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| DELETE | `api/submissions/synopsis/review-queue/` | SynopsisReviewQueueView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| TRACE | `api/submissions/synopsis/review-queue/` | SynopsisReviewQueueView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| GET | `api/submissions/synopsis/<int:submission_id>/review/` | SynopsisReviewActionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| POST | `api/submissions/synopsis/<int:submission_id>/review/` | SynopsisReviewActionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| PUT | `api/submissions/synopsis/<int:submission_id>/review/` | SynopsisReviewActionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| PATCH | `api/submissions/synopsis/<int:submission_id>/review/` | SynopsisReviewActionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| DELETE | `api/submissions/synopsis/<int:submission_id>/review/` | SynopsisReviewActionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| TRACE | `api/submissions/synopsis/<int:submission_id>/review/` | SynopsisReviewActionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| GET | `api/submissions/thesis/` | ThesisSubmissionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| POST | `api/submissions/thesis/` | ThesisSubmissionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| PUT | `api/submissions/thesis/` | ThesisSubmissionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| PATCH | `api/submissions/thesis/` | ThesisSubmissionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| DELETE | `api/submissions/thesis/` | ThesisSubmissionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| TRACE | `api/submissions/thesis/` | ThesisSubmissionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| GET | `api/submissions/thesis/documents/` | ThesisSubmissionDocumentsView | custom/standard | SubmissionDocumentSerializer | IsAuthenticated |
| POST | `api/submissions/thesis/documents/` | ThesisSubmissionDocumentsView | custom/standard | SubmissionDocumentSerializer | IsAuthenticated |
| PUT | `api/submissions/thesis/documents/` | ThesisSubmissionDocumentsView | custom/standard | SubmissionDocumentSerializer | IsAuthenticated |
| PATCH | `api/submissions/thesis/documents/` | ThesisSubmissionDocumentsView | custom/standard | SubmissionDocumentSerializer | IsAuthenticated |
| DELETE | `api/submissions/thesis/documents/` | ThesisSubmissionDocumentsView | custom/standard | SubmissionDocumentSerializer | IsAuthenticated |
| TRACE | `api/submissions/thesis/documents/` | ThesisSubmissionDocumentsView | custom/standard | SubmissionDocumentSerializer | IsAuthenticated |
| GET | `api/submissions/thesis/submit/` | ThesisSubmissionSubmitView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| POST | `api/submissions/thesis/submit/` | ThesisSubmissionSubmitView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| PUT | `api/submissions/thesis/submit/` | ThesisSubmissionSubmitView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| PATCH | `api/submissions/thesis/submit/` | ThesisSubmissionSubmitView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| DELETE | `api/submissions/thesis/submit/` | ThesisSubmissionSubmitView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| TRACE | `api/submissions/thesis/submit/` | ThesisSubmissionSubmitView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| GET | `api/submissions/thesis/review-queue/` | ThesisReviewQueueView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| POST | `api/submissions/thesis/review-queue/` | ThesisReviewQueueView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| PUT | `api/submissions/thesis/review-queue/` | ThesisReviewQueueView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| PATCH | `api/submissions/thesis/review-queue/` | ThesisReviewQueueView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| DELETE | `api/submissions/thesis/review-queue/` | ThesisReviewQueueView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| TRACE | `api/submissions/thesis/review-queue/` | ThesisReviewQueueView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| GET | `api/submissions/thesis/<int:submission_id>/review/` | ThesisReviewActionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| POST | `api/submissions/thesis/<int:submission_id>/review/` | ThesisReviewActionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| PUT | `api/submissions/thesis/<int:submission_id>/review/` | ThesisReviewActionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| PATCH | `api/submissions/thesis/<int:submission_id>/review/` | ThesisReviewActionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| DELETE | `api/submissions/thesis/<int:submission_id>/review/` | ThesisReviewActionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| TRACE | `api/submissions/thesis/<int:submission_id>/review/` | ThesisReviewActionView | custom/standard | ResidentSubmissionSerializer | IsAuthenticated |
| GET | `api/submissions/certificates/` | SubmissionCertificatesView | custom/standard | SubmissionCertificateSerializer | IsAuthenticated |
| POST | `api/submissions/certificates/` | SubmissionCertificatesView | custom/standard | SubmissionCertificateSerializer | IsAuthenticated |
| PUT | `api/submissions/certificates/` | SubmissionCertificatesView | custom/standard | SubmissionCertificateSerializer | IsAuthenticated |
| PATCH | `api/submissions/certificates/` | SubmissionCertificatesView | custom/standard | SubmissionCertificateSerializer | IsAuthenticated |
| DELETE | `api/submissions/certificates/` | SubmissionCertificatesView | custom/standard | SubmissionCertificateSerializer | IsAuthenticated |
| TRACE | `api/submissions/certificates/` | SubmissionCertificatesView | custom/standard | SubmissionCertificateSerializer | IsAuthenticated |
| GET | `api/rotations/completions/` | RotationCompletionsView | custom/standard | RotationCompletionSerializer | IsAuthenticated |
| POST | `api/rotations/completions/` | RotationCompletionsView | custom/standard | RotationCompletionSerializer | IsAuthenticated |
| PUT | `api/rotations/completions/` | RotationCompletionsView | custom/standard | RotationCompletionSerializer | IsAuthenticated |
| PATCH | `api/rotations/completions/` | RotationCompletionsView | custom/standard | RotationCompletionSerializer | IsAuthenticated |
| DELETE | `api/rotations/completions/` | RotationCompletionsView | custom/standard | RotationCompletionSerializer | IsAuthenticated |
| TRACE | `api/rotations/completions/` | RotationCompletionsView | custom/standard | RotationCompletionSerializer | IsAuthenticated |
| GET | `api/rotations/completions/<int:completion_id>/verify/` | RotationCompletionVerifyView | custom/standard | RotationCompletionSerializer | IsAuthenticated |
| POST | `api/rotations/completions/<int:completion_id>/verify/` | RotationCompletionVerifyView | custom/standard | RotationCompletionSerializer | IsAuthenticated |
| PUT | `api/rotations/completions/<int:completion_id>/verify/` | RotationCompletionVerifyView | custom/standard | RotationCompletionSerializer | IsAuthenticated |
| PATCH | `api/rotations/completions/<int:completion_id>/verify/` | RotationCompletionVerifyView | custom/standard | RotationCompletionSerializer | IsAuthenticated |
| DELETE | `api/rotations/completions/<int:completion_id>/verify/` | RotationCompletionVerifyView | custom/standard | RotationCompletionSerializer | IsAuthenticated |
| TRACE | `api/rotations/completions/<int:completion_id>/verify/` | RotationCompletionVerifyView | custom/standard | RotationCompletionSerializer | IsAuthenticated |
| GET | `api/dashboard/resident/` | ResidentOperationalDashboardView | custom/standard | None | IsAuthenticated |
| POST | `api/dashboard/resident/` | ResidentOperationalDashboardView | custom/standard | None | IsAuthenticated |
| PUT | `api/dashboard/resident/` | ResidentOperationalDashboardView | custom/standard | None | IsAuthenticated |
| PATCH | `api/dashboard/resident/` | ResidentOperationalDashboardView | custom/standard | None | IsAuthenticated |
| DELETE | `api/dashboard/resident/` | ResidentOperationalDashboardView | custom/standard | None | IsAuthenticated |
| TRACE | `api/dashboard/resident/` | ResidentOperationalDashboardView | custom/standard | None | IsAuthenticated |
| GET | `api/dashboard/supervisor/` | SupervisorOperationalDashboardView | custom/standard | None | IsAuthenticated |
| POST | `api/dashboard/supervisor/` | SupervisorOperationalDashboardView | custom/standard | None | IsAuthenticated |
| PUT | `api/dashboard/supervisor/` | SupervisorOperationalDashboardView | custom/standard | None | IsAuthenticated |
| PATCH | `api/dashboard/supervisor/` | SupervisorOperationalDashboardView | custom/standard | None | IsAuthenticated |
| DELETE | `api/dashboard/supervisor/` | SupervisorOperationalDashboardView | custom/standard | None | IsAuthenticated |
| TRACE | `api/dashboard/supervisor/` | SupervisorOperationalDashboardView | custom/standard | None | IsAuthenticated |
| GET | `api/dashboard/hod/` | HODOperationalDashboardView | custom/standard | None | IsAuthenticated |
| POST | `api/dashboard/hod/` | HODOperationalDashboardView | custom/standard | None | IsAuthenticated |
| PUT | `api/dashboard/hod/` | HODOperationalDashboardView | custom/standard | None | IsAuthenticated |
| PATCH | `api/dashboard/hod/` | HODOperationalDashboardView | custom/standard | None | IsAuthenticated |
| DELETE | `api/dashboard/hod/` | HODOperationalDashboardView | custom/standard | None | IsAuthenticated |
| TRACE | `api/dashboard/hod/` | HODOperationalDashboardView | custom/standard | None | IsAuthenticated |
| GET | `api/dashboard/utrmc/` | UTRMCOperationalDashboardView | custom/standard | None | IsAuthenticated |
| POST | `api/dashboard/utrmc/` | UTRMCOperationalDashboardView | custom/standard | None | IsAuthenticated |
| PUT | `api/dashboard/utrmc/` | UTRMCOperationalDashboardView | custom/standard | None | IsAuthenticated |
| PATCH | `api/dashboard/utrmc/` | UTRMCOperationalDashboardView | custom/standard | None | IsAuthenticated |
| DELETE | `api/dashboard/utrmc/` | UTRMCOperationalDashboardView | custom/standard | None | IsAuthenticated |
| TRACE | `api/dashboard/utrmc/` | UTRMCOperationalDashboardView | custom/standard | None | IsAuthenticated |
| ANY | `api/^programs/$` | TrainingProgramViewSet | func | None | None |
| ANY | `api/^programs/(?P<pk>[^/.]+)/$` | TrainingProgramViewSet | func | None | None |
| ANY | `api/^program-templates/$` | ProgramRotationTemplateViewSet | func | None | None |
| ANY | `api/^program-templates/(?P<pk>[^/.]+)/$` | ProgramRotationTemplateViewSet | func | None | None |
| ANY | `api/^resident-training/$` | ResidentTrainingRecordViewSet | func | None | None |
| ANY | `api/^resident-training/(?P<pk>[^/.]+)/$` | ResidentTrainingRecordViewSet | func | None | None |
| ANY | `api/^rotations/$` | RotationAssignmentViewSet | func | None | None |
| ANY | `api/^rotations/(?P<pk>[^/.]+)/$` | RotationAssignmentViewSet | func | None | None |
| ANY | `api/^rotations/(?P<pk>[^/.]+)/activate/$` | RotationAssignmentViewSet | func | None | None |
| ANY | `api/^rotations/(?P<pk>[^/.]+)/complete/$` | RotationAssignmentViewSet | func | None | None |
| ANY | `api/^rotations/(?P<pk>[^/.]+)/confirm-completion/$` | RotationAssignmentViewSet | func | None | None |
| ANY | `api/^rotations/(?P<pk>[^/.]+)/hod-approve/$` | RotationAssignmentViewSet | func | None | None |
| ANY | `api/^rotations/(?P<pk>[^/.]+)/reject/$` | RotationAssignmentViewSet | func | None | None |
| ANY | `api/^rotations/(?P<pk>[^/.]+)/returned/$` | RotationAssignmentViewSet | func | None | None |
| ANY | `api/^rotations/(?P<pk>[^/.]+)/review-application/$` | RotationAssignmentViewSet | func | None | None |
| ANY | `api/^rotations/(?P<pk>[^/.]+)/submit/$` | RotationAssignmentViewSet | func | None | None |
| ANY | `api/^rotations/(?P<pk>[^/.]+)/utrmc-approve/$` | RotationAssignmentViewSet | func | None | None |
| ANY | `api/^rotations/(?P<pk>[^/.]+)/verify-completion/$` | RotationAssignmentViewSet | func | None | None |
| ANY | `api/^leaves/$` | LeaveRequestViewSet | func | None | None |
| ANY | `api/^leaves/(?P<pk>[^/.]+)/$` | LeaveRequestViewSet | func | None | None |
| ANY | `api/^leaves/(?P<pk>[^/.]+)/approve/$` | LeaveRequestViewSet | func | None | None |
| ANY | `api/^leaves/(?P<pk>[^/.]+)/reject/$` | LeaveRequestViewSet | func | None | None |
| ANY | `api/^leaves/(?P<pk>[^/.]+)/submit/$` | LeaveRequestViewSet | func | None | None |
| ANY | `api/^postings/$` | DeputationPostingViewSet | func | None | None |
| ANY | `api/^postings/(?P<pk>[^/.]+)/$` | DeputationPostingViewSet | func | None | None |
| ANY | `api/^postings/(?P<pk>[^/.]+)/approve/$` | DeputationPostingViewSet | func | None | None |
| ANY | `api/^postings/(?P<pk>[^/.]+)/complete/$` | DeputationPostingViewSet | func | None | None |
| ANY | `api/^postings/(?P<pk>[^/.]+)/reject/$` | DeputationPostingViewSet | func | None | None |
| ANY | `api/^workshops/$` | WorkshopViewSet | func | None | None |
| ANY | `api/^workshops/(?P<pk>[^/.]+)/$` | WorkshopViewSet | func | None | None |
| ANY | `api/^logbook/config/$` | LogbookThresholdConfigViewSet | func | None | None |
| ANY | `api/^logbook/config/(?P<pk>[^/.]+)/$` | LogbookThresholdConfigViewSet | func | None | None |
| ANY | `api/^logbook/$` | LogbookEntryViewSet | func | None | None |
| ANY | `api/^logbook/(?P<pk>[^/.]+)/$` | LogbookEntryViewSet | func | None | None |
| ANY | `api/^logbook/(?P<pk>[^/.]+)/review/$` | LogbookEntryViewSet | func | None | None |
| ANY | `api/^logbook/(?P<pk>[^/.]+)/submit/$` | LogbookEntryViewSet | func | None | None |
| ANY | `api/^logbook/(?P<pk>[^/.]+)/verify/$` | LogbookEntryViewSet | func | None | None |
| ANY | `api/^submissions/requirements/$` | SubmissionRequirementTemplateViewSet | func | None | None |
| ANY | `api/^submissions/requirements/(?P<pk>[^/.]+)/$` | SubmissionRequirementTemplateViewSet | func | None | None |
| ANY | `api/^rotations/requirements/$` | ProgramRotationRequirementViewSet | func | None | None |
| ANY | `api/^rotations/requirements/(?P<pk>[^/.]+)/$` | ProgramRotationRequirementViewSet | func | None | None |
| GET | `api/` | APIRootView | custom/standard | None | IsAuthenticated |
| POST | `api/` | APIRootView | custom/standard | None | IsAuthenticated |
| PUT | `api/` | APIRootView | custom/standard | None | IsAuthenticated |
| PATCH | `api/` | APIRootView | custom/standard | None | IsAuthenticated |
| DELETE | `api/` | APIRootView | custom/standard | None | IsAuthenticated |
| TRACE | `api/` | APIRootView | custom/standard | None | IsAuthenticated |
| GET | `api/supervisor/rotations/pending/` | SupervisorPendingRotationsView | custom/standard | RotationAssignmentSerializer | IsAuthenticated |
| POST | `api/supervisor/rotations/pending/` | SupervisorPendingRotationsView | custom/standard | RotationAssignmentSerializer | IsAuthenticated |
| PUT | `api/supervisor/rotations/pending/` | SupervisorPendingRotationsView | custom/standard | RotationAssignmentSerializer | IsAuthenticated |
| PATCH | `api/supervisor/rotations/pending/` | SupervisorPendingRotationsView | custom/standard | RotationAssignmentSerializer | IsAuthenticated |
| DELETE | `api/supervisor/rotations/pending/` | SupervisorPendingRotationsView | custom/standard | RotationAssignmentSerializer | IsAuthenticated |
| TRACE | `api/supervisor/rotations/pending/` | SupervisorPendingRotationsView | custom/standard | RotationAssignmentSerializer | IsAuthenticated |
| GET | `api/supervisor/research-approvals/` | SupervisorResearchApprovalsView | custom/standard | None | IsAuthenticated |
| POST | `api/supervisor/research-approvals/` | SupervisorResearchApprovalsView | custom/standard | None | IsAuthenticated |
| PUT | `api/supervisor/research-approvals/` | SupervisorResearchApprovalsView | custom/standard | None | IsAuthenticated |
| PATCH | `api/supervisor/research-approvals/` | SupervisorResearchApprovalsView | custom/standard | None | IsAuthenticated |
| DELETE | `api/supervisor/research-approvals/` | SupervisorResearchApprovalsView | custom/standard | None | IsAuthenticated |
| TRACE | `api/supervisor/research-approvals/` | SupervisorResearchApprovalsView | custom/standard | None | IsAuthenticated |
| GET | `api/residents/me/summary/` | ResidentSummaryView | custom/standard | None | IsAuthenticated |
| POST | `api/residents/me/summary/` | ResidentSummaryView | custom/standard | None | IsAuthenticated |
| PUT | `api/residents/me/summary/` | ResidentSummaryView | custom/standard | None | IsAuthenticated |
| PATCH | `api/residents/me/summary/` | ResidentSummaryView | custom/standard | None | IsAuthenticated |
| DELETE | `api/residents/me/summary/` | ResidentSummaryView | custom/standard | None | IsAuthenticated |
| TRACE | `api/residents/me/summary/` | ResidentSummaryView | custom/standard | None | IsAuthenticated |
| GET | `api/supervisors/me/summary/` | SupervisorSummaryView | custom/standard | None | IsAuthenticated |
| POST | `api/supervisors/me/summary/` | SupervisorSummaryView | custom/standard | None | IsAuthenticated |
| PUT | `api/supervisors/me/summary/` | SupervisorSummaryView | custom/standard | None | IsAuthenticated |
| PATCH | `api/supervisors/me/summary/` | SupervisorSummaryView | custom/standard | None | IsAuthenticated |
| DELETE | `api/supervisors/me/summary/` | SupervisorSummaryView | custom/standard | None | IsAuthenticated |
| TRACE | `api/supervisors/me/summary/` | SupervisorSummaryView | custom/standard | None | IsAuthenticated |
| GET | `api/supervisors/residents/<int:resident_id>/progress/` | SupervisorResidentProgressView | custom/standard | None | IsAuthenticated |
| POST | `api/supervisors/residents/<int:resident_id>/progress/` | SupervisorResidentProgressView | custom/standard | None | IsAuthenticated |
| PUT | `api/supervisors/residents/<int:resident_id>/progress/` | SupervisorResidentProgressView | custom/standard | None | IsAuthenticated |
| PATCH | `api/supervisors/residents/<int:resident_id>/progress/` | SupervisorResidentProgressView | custom/standard | None | IsAuthenticated |
| DELETE | `api/supervisors/residents/<int:resident_id>/progress/` | SupervisorResidentProgressView | custom/standard | None | IsAuthenticated |
| TRACE | `api/supervisors/residents/<int:resident_id>/progress/` | SupervisorResidentProgressView | custom/standard | None | IsAuthenticated |
| GET | `api/system/settings/` | SystemSettingsView | custom/standard | None | IsAuthenticated |
| POST | `api/system/settings/` | SystemSettingsView | custom/standard | None | IsAuthenticated |
| PUT | `api/system/settings/` | SystemSettingsView | custom/standard | None | IsAuthenticated |
| PATCH | `api/system/settings/` | SystemSettingsView | custom/standard | None | IsAuthenticated |
| DELETE | `api/system/settings/` | SystemSettingsView | custom/standard | None | IsAuthenticated |
| TRACE | `api/system/settings/` | SystemSettingsView | custom/standard | None | IsAuthenticated |
| ANY | `academics/api/^departments/$` | DepartmentViewSet | func | None | None |
| ANY | `academics/api/^departments/(?P<pk>[^/.]+)/$` | DepartmentViewSet | func | None | None |
| GET | `academics/api/` | APIRootView | custom/standard | None | IsAuthenticated |
| POST | `academics/api/` | APIRootView | custom/standard | None | IsAuthenticated |
| PUT | `academics/api/` | APIRootView | custom/standard | None | IsAuthenticated |
| PATCH | `academics/api/` | APIRootView | custom/standard | None | IsAuthenticated |
| DELETE | `academics/api/` | APIRootView | custom/standard | None | IsAuthenticated |
| TRACE | `academics/api/` | APIRootView | custom/standard | None | IsAuthenticated |
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
| GET | `api/auth/me/` | AuthMeView | custom/standard | UserManagementSerializer | IsAuthenticated |
| POST | `api/auth/me/` | AuthMeView | custom/standard | UserManagementSerializer | IsAuthenticated |
| PUT | `api/auth/me/` | AuthMeView | custom/standard | UserManagementSerializer | IsAuthenticated |
| PATCH | `api/auth/me/` | AuthMeView | custom/standard | UserManagementSerializer | IsAuthenticated |
| DELETE | `api/auth/me/` | AuthMeView | custom/standard | UserManagementSerializer | IsAuthenticated |
| TRACE | `api/auth/me/` | AuthMeView | custom/standard | UserManagementSerializer | IsAuthenticated |
| GET | `api/auth/profile/` | user_profile_view | custom/standard | None | IsAuthenticated |
| PATCH | `api/auth/profile/update/` | update_profile_view | custom/standard | None | IsAuthenticated |
| PUT | `api/auth/profile/update/` | update_profile_view | custom/standard | None | IsAuthenticated |
| POST | `api/auth/password-reset/` | password_reset_request_view | custom/standard | None | AllowAny |
| POST | `api/auth/password-reset/confirm/` | password_reset_confirm_view | custom/standard | None | AllowAny |
| POST | `api/auth/change-password/` | change_password_view | custom/standard | None | IsAuthenticated |
| GET | `api/backup_center/backups/` | BackupJobListView | custom/standard | BackupJobSerializer | IsAuthenticated, IsSuperAdmin |
| POST | `api/backup_center/backups/` | BackupJobListView | custom/standard | BackupJobSerializer | IsAuthenticated, IsSuperAdmin |
| PUT | `api/backup_center/backups/` | BackupJobListView | custom/standard | BackupJobSerializer | IsAuthenticated, IsSuperAdmin |
| PATCH | `api/backup_center/backups/` | BackupJobListView | custom/standard | BackupJobSerializer | IsAuthenticated, IsSuperAdmin |
| DELETE | `api/backup_center/backups/` | BackupJobListView | custom/standard | BackupJobSerializer | IsAuthenticated, IsSuperAdmin |
| TRACE | `api/backup_center/backups/` | BackupJobListView | custom/standard | BackupJobSerializer | IsAuthenticated, IsSuperAdmin |
| GET | `api/backup_center/backups/<int:pk>/` | BackupJobDetailView | custom/standard | BackupJobSerializer | IsAuthenticated, IsSuperAdmin |
| POST | `api/backup_center/backups/<int:pk>/` | BackupJobDetailView | custom/standard | BackupJobSerializer | IsAuthenticated, IsSuperAdmin |
| PUT | `api/backup_center/backups/<int:pk>/` | BackupJobDetailView | custom/standard | BackupJobSerializer | IsAuthenticated, IsSuperAdmin |
| PATCH | `api/backup_center/backups/<int:pk>/` | BackupJobDetailView | custom/standard | BackupJobSerializer | IsAuthenticated, IsSuperAdmin |
| DELETE | `api/backup_center/backups/<int:pk>/` | BackupJobDetailView | custom/standard | BackupJobSerializer | IsAuthenticated, IsSuperAdmin |
| TRACE | `api/backup_center/backups/<int:pk>/` | BackupJobDetailView | custom/standard | BackupJobSerializer | IsAuthenticated, IsSuperAdmin |
| GET | `api/backup_center/backups/create-routine/` | CreateRoutineBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| POST | `api/backup_center/backups/create-routine/` | CreateRoutineBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PUT | `api/backup_center/backups/create-routine/` | CreateRoutineBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PATCH | `api/backup_center/backups/create-routine/` | CreateRoutineBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| DELETE | `api/backup_center/backups/create-routine/` | CreateRoutineBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| TRACE | `api/backup_center/backups/create-routine/` | CreateRoutineBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| GET | `api/backup_center/backups/create-disaster/` | CreateDisasterBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| POST | `api/backup_center/backups/create-disaster/` | CreateDisasterBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PUT | `api/backup_center/backups/create-disaster/` | CreateDisasterBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PATCH | `api/backup_center/backups/create-disaster/` | CreateDisasterBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| DELETE | `api/backup_center/backups/create-disaster/` | CreateDisasterBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| TRACE | `api/backup_center/backups/create-disaster/` | CreateDisasterBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| GET | `api/backup_center/backups/<int:pk>/download/` | DownloadBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| POST | `api/backup_center/backups/<int:pk>/download/` | DownloadBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PUT | `api/backup_center/backups/<int:pk>/download/` | DownloadBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PATCH | `api/backup_center/backups/<int:pk>/download/` | DownloadBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| DELETE | `api/backup_center/backups/<int:pk>/download/` | DownloadBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| TRACE | `api/backup_center/backups/<int:pk>/download/` | DownloadBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| GET | `api/backup_center/backups/<int:pk>/delete/` | DeleteBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| POST | `api/backup_center/backups/<int:pk>/delete/` | DeleteBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PUT | `api/backup_center/backups/<int:pk>/delete/` | DeleteBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PATCH | `api/backup_center/backups/<int:pk>/delete/` | DeleteBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| DELETE | `api/backup_center/backups/<int:pk>/delete/` | DeleteBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| TRACE | `api/backup_center/backups/<int:pk>/delete/` | DeleteBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| GET | `api/backup_center/backups/<int:pk>/validate/` | ValidateBackupJobView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| POST | `api/backup_center/backups/<int:pk>/validate/` | ValidateBackupJobView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PUT | `api/backup_center/backups/<int:pk>/validate/` | ValidateBackupJobView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PATCH | `api/backup_center/backups/<int:pk>/validate/` | ValidateBackupJobView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| DELETE | `api/backup_center/backups/<int:pk>/validate/` | ValidateBackupJobView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| TRACE | `api/backup_center/backups/<int:pk>/validate/` | ValidateBackupJobView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| GET | `api/backup_center/restores/` | RestoreJobListView | custom/standard | RestoreJobSerializer | IsAuthenticated, IsSuperAdmin |
| POST | `api/backup_center/restores/` | RestoreJobListView | custom/standard | RestoreJobSerializer | IsAuthenticated, IsSuperAdmin |
| PUT | `api/backup_center/restores/` | RestoreJobListView | custom/standard | RestoreJobSerializer | IsAuthenticated, IsSuperAdmin |
| PATCH | `api/backup_center/restores/` | RestoreJobListView | custom/standard | RestoreJobSerializer | IsAuthenticated, IsSuperAdmin |
| DELETE | `api/backup_center/restores/` | RestoreJobListView | custom/standard | RestoreJobSerializer | IsAuthenticated, IsSuperAdmin |
| TRACE | `api/backup_center/restores/` | RestoreJobListView | custom/standard | RestoreJobSerializer | IsAuthenticated, IsSuperAdmin |
| GET | `api/backup_center/restores/upload/` | UploadRestoreFileView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| POST | `api/backup_center/restores/upload/` | UploadRestoreFileView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PUT | `api/backup_center/restores/upload/` | UploadRestoreFileView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PATCH | `api/backup_center/restores/upload/` | UploadRestoreFileView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| DELETE | `api/backup_center/restores/upload/` | UploadRestoreFileView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| TRACE | `api/backup_center/restores/upload/` | UploadRestoreFileView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| GET | `api/backup_center/restores/<int:pk>/validate/` | ValidateRestoreJobView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| POST | `api/backup_center/restores/<int:pk>/validate/` | ValidateRestoreJobView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PUT | `api/backup_center/restores/<int:pk>/validate/` | ValidateRestoreJobView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PATCH | `api/backup_center/restores/<int:pk>/validate/` | ValidateRestoreJobView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| DELETE | `api/backup_center/restores/<int:pk>/validate/` | ValidateRestoreJobView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| TRACE | `api/backup_center/restores/<int:pk>/validate/` | ValidateRestoreJobView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| GET | `api/backup_center/restores/<int:pk>/dry-run/` | DryRunRestoreView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| POST | `api/backup_center/restores/<int:pk>/dry-run/` | DryRunRestoreView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PUT | `api/backup_center/restores/<int:pk>/dry-run/` | DryRunRestoreView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PATCH | `api/backup_center/restores/<int:pk>/dry-run/` | DryRunRestoreView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| DELETE | `api/backup_center/restores/<int:pk>/dry-run/` | DryRunRestoreView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| TRACE | `api/backup_center/restores/<int:pk>/dry-run/` | DryRunRestoreView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| GET | `api/backup_center/restores/<int:pk>/confirm/` | ConfirmRestoreView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| POST | `api/backup_center/restores/<int:pk>/confirm/` | ConfirmRestoreView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PUT | `api/backup_center/restores/<int:pk>/confirm/` | ConfirmRestoreView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PATCH | `api/backup_center/restores/<int:pk>/confirm/` | ConfirmRestoreView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| DELETE | `api/backup_center/restores/<int:pk>/confirm/` | ConfirmRestoreView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| TRACE | `api/backup_center/restores/<int:pk>/confirm/` | ConfirmRestoreView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| GET | `api/backup_center/audit-logs/` | BackupAuditLogListView | custom/standard | BackupAuditLogSerializer | IsAuthenticated, IsSuperAdmin |
| POST | `api/backup_center/audit-logs/` | BackupAuditLogListView | custom/standard | BackupAuditLogSerializer | IsAuthenticated, IsSuperAdmin |
| PUT | `api/backup_center/audit-logs/` | BackupAuditLogListView | custom/standard | BackupAuditLogSerializer | IsAuthenticated, IsSuperAdmin |
| PATCH | `api/backup_center/audit-logs/` | BackupAuditLogListView | custom/standard | BackupAuditLogSerializer | IsAuthenticated, IsSuperAdmin |
| DELETE | `api/backup_center/audit-logs/` | BackupAuditLogListView | custom/standard | BackupAuditLogSerializer | IsAuthenticated, IsSuperAdmin |
| TRACE | `api/backup_center/audit-logs/` | BackupAuditLogListView | custom/standard | BackupAuditLogSerializer | IsAuthenticated, IsSuperAdmin |
| GET | `api/backup_center/google-drive/status/` | GoogleDriveStatusView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| POST | `api/backup_center/google-drive/status/` | GoogleDriveStatusView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PUT | `api/backup_center/google-drive/status/` | GoogleDriveStatusView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PATCH | `api/backup_center/google-drive/status/` | GoogleDriveStatusView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| DELETE | `api/backup_center/google-drive/status/` | GoogleDriveStatusView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| TRACE | `api/backup_center/google-drive/status/` | GoogleDriveStatusView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| GET | `api/backup_center/google-drive/connect/` | GoogleDriveConnectView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| POST | `api/backup_center/google-drive/connect/` | GoogleDriveConnectView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PUT | `api/backup_center/google-drive/connect/` | GoogleDriveConnectView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PATCH | `api/backup_center/google-drive/connect/` | GoogleDriveConnectView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| DELETE | `api/backup_center/google-drive/connect/` | GoogleDriveConnectView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| TRACE | `api/backup_center/google-drive/connect/` | GoogleDriveConnectView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| GET | `api/backup_center/google-drive/oauth/callback/` | GoogleDriveOAuthCallbackView | custom/standard | None | AllowAny |
| POST | `api/backup_center/google-drive/oauth/callback/` | GoogleDriveOAuthCallbackView | custom/standard | None | AllowAny |
| PUT | `api/backup_center/google-drive/oauth/callback/` | GoogleDriveOAuthCallbackView | custom/standard | None | AllowAny |
| PATCH | `api/backup_center/google-drive/oauth/callback/` | GoogleDriveOAuthCallbackView | custom/standard | None | AllowAny |
| DELETE | `api/backup_center/google-drive/oauth/callback/` | GoogleDriveOAuthCallbackView | custom/standard | None | AllowAny |
| TRACE | `api/backup_center/google-drive/oauth/callback/` | GoogleDriveOAuthCallbackView | custom/standard | None | AllowAny |
| GET | `api/backup_center/google-drive/disconnect/` | GoogleDriveDisconnectView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| POST | `api/backup_center/google-drive/disconnect/` | GoogleDriveDisconnectView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PUT | `api/backup_center/google-drive/disconnect/` | GoogleDriveDisconnectView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PATCH | `api/backup_center/google-drive/disconnect/` | GoogleDriveDisconnectView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| DELETE | `api/backup_center/google-drive/disconnect/` | GoogleDriveDisconnectView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| TRACE | `api/backup_center/google-drive/disconnect/` | GoogleDriveDisconnectView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| GET | `api/backup_center/google-drive/health-check/` | GoogleDriveHealthCheckView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| POST | `api/backup_center/google-drive/health-check/` | GoogleDriveHealthCheckView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PUT | `api/backup_center/google-drive/health-check/` | GoogleDriveHealthCheckView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PATCH | `api/backup_center/google-drive/health-check/` | GoogleDriveHealthCheckView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| DELETE | `api/backup_center/google-drive/health-check/` | GoogleDriveHealthCheckView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| TRACE | `api/backup_center/google-drive/health-check/` | GoogleDriveHealthCheckView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| GET | `api/backup_center/google-drive/create-folder/` | GoogleDriveCreateFolderView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| POST | `api/backup_center/google-drive/create-folder/` | GoogleDriveCreateFolderView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PUT | `api/backup_center/google-drive/create-folder/` | GoogleDriveCreateFolderView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PATCH | `api/backup_center/google-drive/create-folder/` | GoogleDriveCreateFolderView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| DELETE | `api/backup_center/google-drive/create-folder/` | GoogleDriveCreateFolderView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| TRACE | `api/backup_center/google-drive/create-folder/` | GoogleDriveCreateFolderView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| GET | `api/backup_center/backups/<int:pk>/google-drive/upload/` | GoogleDriveUploadBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| POST | `api/backup_center/backups/<int:pk>/google-drive/upload/` | GoogleDriveUploadBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PUT | `api/backup_center/backups/<int:pk>/google-drive/upload/` | GoogleDriveUploadBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PATCH | `api/backup_center/backups/<int:pk>/google-drive/upload/` | GoogleDriveUploadBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| DELETE | `api/backup_center/backups/<int:pk>/google-drive/upload/` | GoogleDriveUploadBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| TRACE | `api/backup_center/backups/<int:pk>/google-drive/upload/` | GoogleDriveUploadBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| GET | `api/backup_center/backups/<int:pk>/google-drive/verify/` | GoogleDriveVerifyBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| POST | `api/backup_center/backups/<int:pk>/google-drive/verify/` | GoogleDriveVerifyBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PUT | `api/backup_center/backups/<int:pk>/google-drive/verify/` | GoogleDriveVerifyBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PATCH | `api/backup_center/backups/<int:pk>/google-drive/verify/` | GoogleDriveVerifyBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| DELETE | `api/backup_center/backups/<int:pk>/google-drive/verify/` | GoogleDriveVerifyBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| TRACE | `api/backup_center/backups/<int:pk>/google-drive/verify/` | GoogleDriveVerifyBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| GET | `api/backup_center/backups/<int:pk>/google-drive/download/` | GoogleDriveDownloadBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| POST | `api/backup_center/backups/<int:pk>/google-drive/download/` | GoogleDriveDownloadBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PUT | `api/backup_center/backups/<int:pk>/google-drive/download/` | GoogleDriveDownloadBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PATCH | `api/backup_center/backups/<int:pk>/google-drive/download/` | GoogleDriveDownloadBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| DELETE | `api/backup_center/backups/<int:pk>/google-drive/download/` | GoogleDriveDownloadBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| TRACE | `api/backup_center/backups/<int:pk>/google-drive/download/` | GoogleDriveDownloadBackupView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| GET | `api/backup_center/google-drive/list/` | GoogleDriveListView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| POST | `api/backup_center/google-drive/list/` | GoogleDriveListView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PUT | `api/backup_center/google-drive/list/` | GoogleDriveListView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| PATCH | `api/backup_center/google-drive/list/` | GoogleDriveListView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| DELETE | `api/backup_center/google-drive/list/` | GoogleDriveListView | custom/standard | None | IsAuthenticated, IsSuperAdmin |
| TRACE | `api/backup_center/google-drive/list/` | GoogleDriveListView | custom/standard | None | IsAuthenticated, IsSuperAdmin |

## B) Frontend Inventory
| Method | URL | Caller File | Line | Adapter / Notes |
|---|---|---|---|---|
| GET | `/api/hospitals/` | lib/api/hospitals.ts | 4 | |
| POST | `/api/hospitals/` | lib/api/hospitals.ts | 5 | |
| PATCH | `/api/hospitals/${id}/` | lib/api/hospitals.ts | 6 | |
| DELETE | `/api/hospitals/${id}/` | lib/api/hospitals.ts | 7 | |
| GET | `/api/audit/activity/` | lib/api/audit.ts | 31 | |
| GET | `/api/audit/reports/` | lib/api/audit.ts | 39 | |
| POST | `/api/audit/reports/` | lib/api/audit.ts | 47 | |
| GET | `/api/bulk/templates/${resource}/` | lib/api/bulk.ts | 56 | |
| GET | `/api/bulk/exports/${resource}/` | lib/api/bulk.ts | 66 | |
| POST | `/api/hospitals/` | lib/api/userbase.ts | 117 | |
| PATCH | `/api/hospitals/${id}/` | lib/api/userbase.ts | 121 | |
| GET | `/api/hospitals/${id}/departments/` | lib/api/userbase.ts | 125 | |
| DELETE | `/api/hospitals/${id}/` | lib/api/userbase.ts | 129 | |
| POST | `/api/departments/` | lib/api/userbase.ts | 140 | |
| PATCH | `/api/departments/${id}/` | lib/api/userbase.ts | 144 | |
| DELETE | `/api/departments/${id}/` | lib/api/userbase.ts | 148 | |
| GET | `/api/departments/${id}/roster/` | lib/api/userbase.ts | 151 | |
| POST | `/api/hospital-departments/` | lib/api/userbase.ts | 163 | |
| PATCH | `/api/hospital-departments/${id}/` | lib/api/userbase.ts | 167 | |
| POST | `/api/users/` | lib/api/userbase.ts | 180 | |
| GET | `/api/users/${id}/` | lib/api/userbase.ts | 184 | |
| PATCH | `/api/users/${id}/` | lib/api/userbase.ts | 188 | |
| PATCH | `/api/residents/${userId}/` | lib/api/userbase.ts | 197 | |
| PATCH | `/api/staff/${userId}/` | lib/api/userbase.ts | 212 | |
| GET | `/api/admin/data-quality/summary` | lib/api/userbase.ts | 218 | |
| GET | `/api/admin/data-quality/users` | lib/api/userbase.ts | 222 | |
| POST | `/api/admin/data-quality/recompute` | lib/api/userbase.ts | 228 | |
| GET | `/api/admin/data-quality/audit` | lib/api/userbase.ts | 232 | |
| POST | `/api/department-memberships/` | lib/api/userbase.ts | 238 | |
| PATCH | `/api/department-memberships/${id}/` | lib/api/userbase.ts | 242 | |
| DELETE | `/api/department-memberships/${id}/` | lib/api/userbase.ts | 246 | |
| POST | `/api/hospital-assignments/` | lib/api/userbase.ts | 251 | |
| PATCH | `/api/hospital-assignments/${id}/` | lib/api/userbase.ts | 255 | |
| DELETE | `/api/hospital-assignments/${id}/` | lib/api/userbase.ts | 259 | |
| GET | `/api/supervision-links/` | lib/api/userbase.ts | 264 | |
| POST | `/api/supervision-links/` | lib/api/userbase.ts | 268 | |
| PATCH | `/api/supervision-links/${id}/` | lib/api/userbase.ts | 272 | |
| GET | `/api/hod-assignments/` | lib/api/userbase.ts | 278 | |
| POST | `/api/hod-assignments/` | lib/api/userbase.ts | 282 | |
| PATCH | `/api/hod-assignments/${id}/` | lib/api/userbase.ts | 286 | |
| GET | `/api/programs/` | lib/api/training.ts | 466 | |
| GET | `/api/programs/${id}/` | lib/api/training.ts | 471 | |
| POST | `/api/programs/` | lib/api/training.ts | 476 | |
| PUT | `/api/programs/${id}/` | lib/api/training.ts | 481 | |
| GET | `/api/programs/${programId}/policy/` | lib/api/training.ts | 487 | |
| PUT | `/api/programs/${programId}/policy/` | lib/api/training.ts | 492 | |
| GET | `/api/programs/${programId}/milestones/` | lib/api/training.ts | 498 | |
| POST | `/api/programs/${programId}/milestones/` | lib/api/training.ts | 503 | |
| GET | `/api/my/research/` | lib/api/training.ts | 509 | |
| POST | `/api/my/research/` | lib/api/training.ts | 514 | |
| PATCH | `/api/my/research/` | lib/api/training.ts | 519 | |
| PATCH | `/api/my/research/` | lib/api/training.ts | 526 | |
| POST | `/api/my/research/action/${action}/` | lib/api/training.ts | 533 | |
| GET | `/api/supervisor/research-approvals/` | lib/api/training.ts | 539 | |
| POST | `/api/my/research/action/supervisor-approve/` | lib/api/training.ts | 544 | |
| POST | `/api/my/research/action/supervisor-return/` | lib/api/training.ts | 552 | |
| GET | `/api/my/thesis/` | lib/api/training.ts | 561 | |
| POST | `/api/my/thesis/` | lib/api/training.ts | 566 | |
| POST | `/api/my/thesis/submit/` | lib/api/training.ts | 571 | |
| GET | `/api/workshops/` | lib/api/training.ts | 577 | |
| GET | `/api/my/workshops/` | lib/api/training.ts | 582 | |
| POST | `/api/my/workshops/` | lib/api/training.ts | 591 | |
| DELETE | `/api/my/workshops/${id}/` | lib/api/training.ts | 596 | |
| GET | `/api/my/eligibility/` | lib/api/training.ts | 601 | |
| GET | `/api/residents/me/summary/` | lib/api/training.ts | 630 | |
| GET | `/api/supervisors/me/summary/` | lib/api/training.ts | 635 | |
| GET | `/api/supervisors/residents/${residentId}/progress/` | lib/api/training.ts | 640 | |
| GET | `/api/resident-training/` | lib/api/training.ts | 647 | |
| GET | `/api/my/rotations/` | lib/api/training.ts | 652 | |
| GET | `/api/rotations/` | lib/api/training.ts | 660 | |
| GET | `/api/supervisor/rotations/pending/` | lib/api/training.ts | 670 | |
| GET | `/api/utrmc/approvals/rotations/` | lib/api/training.ts | 675 | |
| POST | `/api/rotations/` | lib/api/training.ts | 686 | |
| POST | `/api/rotations/${id}/${action}/` | lib/api/training.ts | 705 | |
| GET | `/api/logbook/` | lib/api/training.ts | 712 | |
| POST | `/api/logbook/` | lib/api/training.ts | 720 | |
| PATCH | `/api/logbook/${id}/` | lib/api/training.ts | 725 | |
| POST | `/api/logbook/${id}/submit/` | lib/api/training.ts | 730 | |
| POST | `/api/logbook/${id}/review/` | lib/api/training.ts | 739 | |
| GET | `/api/logbook/review-queue/` | lib/api/training.ts | 747 | |
| GET | `/api/logbook/my-threshold/` | lib/api/training.ts | 756 | |
| GET | `/api/submissions/requirements/` | lib/api/training.ts | 769 | |
| GET | `/api/submissions/synopsis/` | lib/api/training.ts | 776 | |
| POST | `/api/submissions/synopsis/` | lib/api/training.ts | 781 | |
| PATCH | `/api/submissions/synopsis/` | lib/api/training.ts | 786 | |
| POST | `/api/submissions/synopsis/submit/` | lib/api/training.ts | 803 | |
| GET | `/api/submissions/thesis/` | lib/api/training.ts | 808 | |
| POST | `/api/submissions/thesis/` | lib/api/training.ts | 813 | |
| PATCH | `/api/submissions/thesis/` | lib/api/training.ts | 818 | |
| POST | `/api/submissions/thesis/submit/` | lib/api/training.ts | 835 | |
| GET | `/api/submissions/synopsis/review-queue/` | lib/api/training.ts | 840 | |
| GET | `/api/submissions/thesis/review-queue/` | lib/api/training.ts | 845 | |
| GET | `/api/submissions/certificates/` | lib/api/training.ts | 876 | |
| GET | `/api/rotations/completions/` | lib/api/training.ts | 885 | |
| GET | `/api/dashboard/resident/` | lib/api/training.ts | 902 | |
| GET | `/api/dashboard/supervisor/` | lib/api/training.ts | 907 | |
| GET | `/api/dashboard/hod/` | lib/api/training.ts | 912 | |
| GET | `/api/dashboard/utrmc/` | lib/api/training.ts | 917 | |
| GET | `/api/my/leaves/` | lib/api/training.ts | 924 | |
| POST | `/api/leaves/` | lib/api/training.ts | 935 | |
| POST | `/api/leaves/${id}/submit/` | lib/api/training.ts | 940 | |
| GET | `/api/utrmc/approvals/leaves/` | lib/api/training.ts | 945 | |
| POST | `/api/leaves/${id}/approve/` | lib/api/training.ts | 950 | |
| POST | `/api/leaves/${id}/reject/` | lib/api/training.ts | 955 | |
| GET | `/api/system/settings/` | lib/api/training.ts | 961 | |
| GET | `/api/program-templates/?program=${programId}` | lib/api/training.ts | 968 | |
| POST | `/api/program-templates/` | lib/api/training.ts | 973 | |
| PATCH | `/api/program-templates/${id}/` | lib/api/training.ts | 978 | |
| DELETE | `/api/program-templates/${id}/` | lib/api/training.ts | 983 | |
| GET | `/api/postings/${qs}` | lib/api/training.ts | 990 | |
| POST | `/api/postings/` | lib/api/training.ts | 995 | |
| POST | `/api/postings/${id}/${action}/` | lib/api/training.ts | 1000 | |
| DELETE | `/api/postings/${id}/` | lib/api/training.ts | 1005 | |
| GET | `/api/notifications/` | lib/api/notifications.ts | 30 | |
| GET | `/api/notifications/` | lib/api/notifications.ts | 39 | |
| GET | `/api/notifications/unread-count/` | lib/api/notifications.ts | 50 | |
| POST | `/api/notifications/mark-read/` | lib/api/notifications.ts | 59 | |
| GET | `/api/notifications/preferences/` | lib/api/notifications.ts | 69 | |
| PATCH | `/api/notifications/preferences/` | lib/api/notifications.ts | 77 | |
| POST | `/api/auth/login/` | lib/api/auth.ts | 59 | |
| POST | `/api/auth/register/` | lib/api/auth.ts | 67 | |
| POST | `/api/auth/logout/` | lib/api/auth.ts | 78 | |
| GET | `/api/auth/profile/` | lib/api/auth.ts | 97 | |
| POST | `/api/auth/refresh/` | lib/api/auth.ts | 106 | |
| PATCH | `/api/auth/profile/update/` | lib/api/auth.ts | 117 | |
| POST | `/api/auth/password-reset/` | lib/api/auth.ts | 126 | |
| POST | `/api/auth/password-reset/confirm/` | lib/api/auth.ts | 140 | |
| POST | `/api/auth/change-password/` | lib/api/auth.ts | 153 | |
| GET | `/api/users/assigned-pgs/` | lib/api/users.ts | 22 | |
| GET | `/api/users/?role=supervisor` | lib/api/users.ts | 27 | |
| GET | `/api/departments/` | lib/api/departments.ts | 18 | |
| POST | `/api/departments/` | lib/api/departments.ts | 19 | |
| PATCH | `/api/departments/${id}/` | lib/api/departments.ts | 20 | |
| DELETE | `/api/departments/${id}/` | lib/api/departments.ts | 21 | |
| GET | `/api/hospital-departments/` | lib/api/departments.ts | 22 | |
| POST | `/api/hospital-departments/` | lib/api/departments.ts | 23 | |
| DELETE | `/api/hospital-departments/${id}/` | lib/api/departments.ts | 24 | |
| GET | `/api/supervision-links/` | lib/api/departments.ts | 26 | |
| POST | `/api/supervision-links/` | lib/api/departments.ts | 27 | |
| DELETE | `/api/supervision-links/${id}/` | lib/api/departments.ts | 28 | |
| GET | `/api/hod-assignments/` | lib/api/departments.ts | 29 | |
| POST | `/api/hod-assignments/` | lib/api/departments.ts | 30 | |

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
- **GET users/api/users/search/** -> lib/api/users.ts (GET)
- **POST users/api/users/search/** -> lib/api/userbase.ts (POST)
- **PUT users/api/users/search/** -> [backend-only/future]
- **PATCH users/api/users/search/** -> [backend-only/future]
- **DELETE users/api/users/search/** -> [backend-only/future]
- **TRACE users/api/users/search/** -> [backend-only/future]
- **GET users/api/supervisors/specialty/<str:specialty>/** -> lib/api/users.ts (GET)
- **POST users/api/supervisors/specialty/<str:specialty>/** -> lib/api/userbase.ts (POST)
- **PUT users/api/supervisors/specialty/<str:specialty>/** -> [backend-only/future]
- **PATCH users/api/supervisors/specialty/<str:specialty>/** -> [backend-only/future]
- **DELETE users/api/supervisors/specialty/<str:specialty>/** -> [backend-only/future]
- **TRACE users/api/supervisors/specialty/<str:specialty>/** -> [backend-only/future]
- **GET users/api/user/<int:pk>/stats/** -> lib/api/users.ts (GET)
- **POST users/api/user/<int:pk>/stats/** -> lib/api/userbase.ts (POST)
- **PUT users/api/user/<int:pk>/stats/** -> [backend-only/future]
- **PATCH users/api/user/<int:pk>/stats/** -> [backend-only/future]
- **DELETE users/api/user/<int:pk>/stats/** -> [backend-only/future]
- **TRACE users/api/user/<int:pk>/stats/** -> [backend-only/future]
- **GET users/api/stats/** -> lib/api/users.ts (GET)
- **POST users/api/stats/** -> lib/api/userbase.ts (POST)
- **PUT users/api/stats/** -> [backend-only/future]
- **PATCH users/api/stats/** -> [backend-only/future]
- **DELETE users/api/stats/** -> [backend-only/future]
- **TRACE users/api/stats/** -> [backend-only/future]
- **ANY users/api/admin/stats/** -> lib/api/userbase.ts (POST), lib/api/users.ts (GET)
- **GET users/api/user-statistics/** -> lib/api/users.ts (GET)
- **POST users/api/user-statistics/** -> lib/api/userbase.ts (POST)
- **PUT users/api/user-statistics/** -> [backend-only/future]
- **PATCH users/api/user-statistics/** -> [backend-only/future]
- **DELETE users/api/user-statistics/** -> [backend-only/future]
- **TRACE users/api/user-statistics/** -> [backend-only/future]
- **GET users/api/user-performance/** -> lib/api/users.ts (GET)
- **POST users/api/user-performance/** -> lib/api/userbase.ts (POST)
- **PUT users/api/user-performance/** -> [backend-only/future]
- **PATCH users/api/user-performance/** -> [backend-only/future]
- **DELETE users/api/user-performance/** -> [backend-only/future]
- **TRACE users/api/user-performance/** -> [backend-only/future]
- **ANY logbook/api/stats/** -> lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY logbook/api/template/<int:template_id>/preview/** -> lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY logbook/api/entry/<int:entry_id>/complexity/** -> lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY logbook/api/update-statistics/** -> lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY rotations/api/departments/<int:hospital_id>/** -> lib/api/departments.ts (PATCH), lib/api/userbase.ts (DELETE), lib/api/userbase.ts (POST), lib/api/training.ts (POST), lib/api/training.ts (GET), lib/api/departments.ts (DELETE), lib/api/departments.ts (POST), lib/api/userbase.ts (PATCH), lib/api/departments.ts (GET)
- **ANY rotations/api/quick-stats/** -> lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/audit/^activity/$** -> lib/api/audit.ts (GET)
- **ANY api/audit/^activity/export/$** -> lib/api/audit.ts (GET)
- **ANY api/audit/^activity/(?P<pk>[^/.]+)/$** -> lib/api/audit.ts (GET)
- **ANY api/audit/^reports/$** -> lib/api/audit.ts (GET), lib/api/audit.ts (POST)
- **ANY api/audit/^reports/latest/$** -> lib/api/audit.ts (GET), lib/api/audit.ts (POST)
- **GET api/audit/** -> lib/api/userbase.ts (GET), lib/api/audit.ts (GET)
- **POST api/audit/** -> lib/api/audit.ts (POST)
- **PUT api/audit/** -> [system-only]
- **PATCH api/audit/** -> [system-only]
- **DELETE api/audit/** -> [system-only]
- **TRACE api/audit/** -> [system-only]
- **GET api/bulk/review/** -> [backend-only/future]
- **POST api/bulk/review/** -> [backend-only/future]
- **PUT api/bulk/review/** -> [backend-only/future]
- **PATCH api/bulk/review/** -> [backend-only/future]
- **DELETE api/bulk/review/** -> [backend-only/future]
- **TRACE api/bulk/review/** -> [backend-only/future]
- **GET api/bulk/assignment/** -> [backend-only/future]
- **POST api/bulk/assignment/** -> [backend-only/future]
- **PUT api/bulk/assignment/** -> [backend-only/future]
- **PATCH api/bulk/assignment/** -> [backend-only/future]
- **DELETE api/bulk/assignment/** -> [backend-only/future]
- **TRACE api/bulk/assignment/** -> [backend-only/future]
- **GET api/bulk/import/** -> [backend-only/future]
- **POST api/bulk/import/** -> [backend-only/future]
- **PUT api/bulk/import/** -> [backend-only/future]
- **PATCH api/bulk/import/** -> [backend-only/future]
- **DELETE api/bulk/import/** -> [backend-only/future]
- **TRACE api/bulk/import/** -> [backend-only/future]
- **GET api/bulk/import-trainees/** -> [backend-only/future]
- **POST api/bulk/import-trainees/** -> [backend-only/future]
- **PUT api/bulk/import-trainees/** -> [backend-only/future]
- **PATCH api/bulk/import-trainees/** -> [backend-only/future]
- **DELETE api/bulk/import-trainees/** -> [backend-only/future]
- **TRACE api/bulk/import-trainees/** -> [backend-only/future]
- **GET api/bulk/import-supervisors/** -> [backend-only/future]
- **POST api/bulk/import-supervisors/** -> [backend-only/future]
- **PUT api/bulk/import-supervisors/** -> [backend-only/future]
- **PATCH api/bulk/import-supervisors/** -> [backend-only/future]
- **DELETE api/bulk/import-supervisors/** -> [backend-only/future]
- **TRACE api/bulk/import-supervisors/** -> [backend-only/future]
- **GET api/bulk/import-residents/** -> [backend-only/future]
- **POST api/bulk/import-residents/** -> [backend-only/future]
- **PUT api/bulk/import-residents/** -> [backend-only/future]
- **PATCH api/bulk/import-residents/** -> [backend-only/future]
- **DELETE api/bulk/import-residents/** -> [backend-only/future]
- **TRACE api/bulk/import-residents/** -> [backend-only/future]
- **GET api/bulk/import-departments/** -> lib/api/departments.ts (GET)
- **POST api/bulk/import-departments/** -> lib/api/departments.ts (POST), lib/api/userbase.ts (POST)
- **PUT api/bulk/import-departments/** -> [backend-only/future]
- **PATCH api/bulk/import-departments/** -> [backend-only/future]
- **DELETE api/bulk/import-departments/** -> [backend-only/future]
- **TRACE api/bulk/import-departments/** -> [backend-only/future]
- **GET api/bulk/exports/<str:resource>/** -> lib/api/bulk.ts (GET)
- **POST api/bulk/exports/<str:resource>/** -> [backend-only/future]
- **PUT api/bulk/exports/<str:resource>/** -> [backend-only/future]
- **PATCH api/bulk/exports/<str:resource>/** -> [backend-only/future]
- **DELETE api/bulk/exports/<str:resource>/** -> [backend-only/future]
- **TRACE api/bulk/exports/<str:resource>/** -> [backend-only/future]
- **GET api/bulk/templates/<str:resource>/** -> lib/api/bulk.ts (GET)
- **POST api/bulk/templates/<str:resource>/** -> [backend-only/future]
- **PUT api/bulk/templates/<str:resource>/** -> [backend-only/future]
- **PATCH api/bulk/templates/<str:resource>/** -> [backend-only/future]
- **DELETE api/bulk/templates/<str:resource>/** -> [backend-only/future]
- **TRACE api/bulk/templates/<str:resource>/** -> [backend-only/future]
- **GET api/bulk/import/<str:entity>/<str:action>/** -> [backend-only/future]
- **POST api/bulk/import/<str:entity>/<str:action>/** -> [backend-only/future]
- **PUT api/bulk/import/<str:entity>/<str:action>/** -> [backend-only/future]
- **PATCH api/bulk/import/<str:entity>/<str:action>/** -> [backend-only/future]
- **DELETE api/bulk/import/<str:entity>/<str:action>/** -> [backend-only/future]
- **TRACE api/bulk/import/<str:entity>/<str:action>/** -> [backend-only/future]
- **GET api/bulk/flexible/schemas/** -> [backend-only/future]
- **POST api/bulk/flexible/schemas/** -> [backend-only/future]
- **PUT api/bulk/flexible/schemas/** -> [backend-only/future]
- **PATCH api/bulk/flexible/schemas/** -> [backend-only/future]
- **DELETE api/bulk/flexible/schemas/** -> [backend-only/future]
- **TRACE api/bulk/flexible/schemas/** -> [backend-only/future]
- **GET api/bulk/flexible/detect-headers/** -> [backend-only/future]
- **POST api/bulk/flexible/detect-headers/** -> [backend-only/future]
- **PUT api/bulk/flexible/detect-headers/** -> [backend-only/future]
- **PATCH api/bulk/flexible/detect-headers/** -> [backend-only/future]
- **DELETE api/bulk/flexible/detect-headers/** -> [backend-only/future]
- **TRACE api/bulk/flexible/detect-headers/** -> [backend-only/future]
- **GET api/bulk/flexible/validate-mapping/** -> [backend-only/future]
- **POST api/bulk/flexible/validate-mapping/** -> [backend-only/future]
- **PUT api/bulk/flexible/validate-mapping/** -> [backend-only/future]
- **PATCH api/bulk/flexible/validate-mapping/** -> [backend-only/future]
- **DELETE api/bulk/flexible/validate-mapping/** -> [backend-only/future]
- **TRACE api/bulk/flexible/validate-mapping/** -> [backend-only/future]
- **GET api/bulk/flexible/dry-run/** -> [backend-only/future]
- **POST api/bulk/flexible/dry-run/** -> [backend-only/future]
- **PUT api/bulk/flexible/dry-run/** -> [backend-only/future]
- **PATCH api/bulk/flexible/dry-run/** -> [backend-only/future]
- **DELETE api/bulk/flexible/dry-run/** -> [backend-only/future]
- **TRACE api/bulk/flexible/dry-run/** -> [backend-only/future]
- **GET api/bulk/flexible/apply/** -> [backend-only/future]
- **POST api/bulk/flexible/apply/** -> [backend-only/future]
- **PUT api/bulk/flexible/apply/** -> [backend-only/future]
- **PATCH api/bulk/flexible/apply/** -> [backend-only/future]
- **DELETE api/bulk/flexible/apply/** -> [backend-only/future]
- **TRACE api/bulk/flexible/apply/** -> [backend-only/future]
- **ANY api/bulk/flexible/presets/** -> [backend-only/future]
- **ANY api/bulk/flexible/presets/<int:pk>/** -> [backend-only/future]
- **GET api/notifications/** -> lib/api/notifications.ts (GET)
- **POST api/notifications/** -> lib/api/notifications.ts (POST)
- **PUT api/notifications/** -> [backend-only/future]
- **PATCH api/notifications/** -> lib/api/notifications.ts (PATCH)
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
- **GET api/schema/** -> [backend-only/future]
- **POST api/schema/** -> [backend-only/future]
- **PUT api/schema/** -> [backend-only/future]
- **PATCH api/schema/** -> [backend-only/future]
- **DELETE api/schema/** -> [backend-only/future]
- **TRACE api/schema/** -> [backend-only/future]
- **ANY api/^hospitals/$** -> lib/api/userbase.ts (DELETE), lib/api/userbase.ts (GET), lib/api/hospitals.ts (GET), lib/api/userbase.ts (POST), lib/api/hospitals.ts (PATCH), lib/api/hospitals.ts (POST), lib/api/hospitals.ts (DELETE), lib/api/userbase.ts (PATCH)
- **ANY api/^hospitals/(?P<pk>[^/.]+)/$** -> lib/api/userbase.ts (DELETE), lib/api/userbase.ts (GET), lib/api/hospitals.ts (GET), lib/api/userbase.ts (POST), lib/api/hospitals.ts (PATCH), lib/api/hospitals.ts (POST), lib/api/hospitals.ts (DELETE), lib/api/userbase.ts (PATCH)
- **ANY api/^hospitals/(?P<pk>[^/.]+)/departments/$** -> lib/api/departments.ts (POST), lib/api/userbase.ts (DELETE), lib/api/userbase.ts (GET), lib/api/hospitals.ts (GET), lib/api/userbase.ts (POST), lib/api/hospitals.ts (PATCH), lib/api/hospitals.ts (POST), lib/api/hospitals.ts (DELETE), lib/api/userbase.ts (PATCH), lib/api/departments.ts (GET)
- **ANY api/^departments/$** -> lib/api/departments.ts (PATCH), lib/api/userbase.ts (DELETE), lib/api/userbase.ts (GET), lib/api/userbase.ts (POST), lib/api/departments.ts (DELETE), lib/api/departments.ts (POST), lib/api/userbase.ts (PATCH), lib/api/departments.ts (GET)
- **ANY api/^departments/(?P<pk>[^/.]+)/$** -> lib/api/departments.ts (PATCH), lib/api/userbase.ts (DELETE), lib/api/userbase.ts (GET), lib/api/userbase.ts (POST), lib/api/departments.ts (DELETE), lib/api/departments.ts (POST), lib/api/userbase.ts (PATCH), lib/api/departments.ts (GET)
- **ANY api/^departments/(?P<pk>[^/.]+)/roster/$** -> lib/api/departments.ts (PATCH), lib/api/userbase.ts (DELETE), lib/api/userbase.ts (GET), lib/api/userbase.ts (POST), lib/api/departments.ts (DELETE), lib/api/departments.ts (POST), lib/api/userbase.ts (PATCH), lib/api/departments.ts (GET)
- **ANY api/^hospital-departments/$** -> lib/api/userbase.ts (POST), lib/api/departments.ts (DELETE), lib/api/departments.ts (POST), lib/api/userbase.ts (PATCH), lib/api/departments.ts (GET)
- **ANY api/^hospital-departments/(?P<pk>[^/.]+)/$** -> lib/api/departments.ts (PATCH), lib/api/userbase.ts (DELETE), lib/api/userbase.ts (POST), lib/api/departments.ts (DELETE), lib/api/departments.ts (POST), lib/api/userbase.ts (PATCH), lib/api/departments.ts (GET)
- **ANY api/^residents/$** -> lib/api/userbase.ts (PATCH), lib/api/training.ts (GET)
- **ANY api/^residents/(?P<user_id>[^/.]+)/$** -> lib/api/userbase.ts (PATCH), lib/api/training.ts (GET)
- **ANY api/^staff/$** -> lib/api/userbase.ts (PATCH)
- **ANY api/^staff/(?P<user_id>[^/.]+)/$** -> lib/api/userbase.ts (PATCH)
- **ANY api/^department-memberships/$** -> lib/api/userbase.ts (PATCH), lib/api/userbase.ts (POST), lib/api/userbase.ts (DELETE)
- **ANY api/^department-memberships/(?P<pk>[^/.]+)/$** -> lib/api/userbase.ts (PATCH), lib/api/userbase.ts (POST), lib/api/userbase.ts (DELETE)
- **ANY api/^hospital-assignments/$** -> lib/api/userbase.ts (PATCH), lib/api/userbase.ts (POST), lib/api/userbase.ts (DELETE)
- **ANY api/^hospital-assignments/(?P<pk>[^/.]+)/$** -> lib/api/userbase.ts (PATCH), lib/api/userbase.ts (POST), lib/api/userbase.ts (DELETE)
- **ANY api/^supervision-links/$** -> lib/api/userbase.ts (GET), lib/api/userbase.ts (POST), lib/api/departments.ts (DELETE), lib/api/departments.ts (POST), lib/api/userbase.ts (PATCH), lib/api/departments.ts (GET)
- **ANY api/^supervision-links/(?P<pk>[^/.]+)/$** -> lib/api/userbase.ts (GET), lib/api/userbase.ts (POST), lib/api/departments.ts (DELETE), lib/api/departments.ts (POST), lib/api/userbase.ts (PATCH), lib/api/departments.ts (GET)
- **ANY api/^hod-assignments/$** -> lib/api/userbase.ts (GET), lib/api/userbase.ts (POST), lib/api/departments.ts (POST), lib/api/userbase.ts (PATCH), lib/api/departments.ts (GET)
- **ANY api/^hod-assignments/(?P<pk>[^/.]+)/$** -> lib/api/userbase.ts (GET), lib/api/userbase.ts (POST), lib/api/departments.ts (POST), lib/api/userbase.ts (PATCH), lib/api/departments.ts (GET)
- **GET api/** -> lib/api/audit.ts (GET), lib/api/userbase.ts (GET), lib/api/hospitals.ts (GET), lib/api/auth.ts (GET), lib/api/bulk.ts (GET), lib/api/notifications.ts (GET), lib/api/training.ts (GET), lib/api/departments.ts (GET), lib/api/users.ts (GET)
- **POST api/** -> lib/api/notifications.ts (POST), lib/api/audit.ts (POST), lib/api/departments.ts (POST), lib/api/userbase.ts (POST), lib/api/training.ts (POST), lib/api/hospitals.ts (POST), lib/api/auth.ts (POST)
- **PUT api/** -> lib/api/training.ts (PUT)
- **PATCH api/** -> lib/api/departments.ts (PATCH), lib/api/notifications.ts (PATCH), lib/api/hospitals.ts (PATCH), lib/api/training.ts (PATCH), lib/api/auth.ts (PATCH), lib/api/userbase.ts (PATCH)
- **DELETE api/** -> lib/api/hospitals.ts (DELETE), lib/api/training.ts (DELETE), lib/api/departments.ts (DELETE), lib/api/userbase.ts (DELETE)
- **TRACE api/** -> [system-only]
- **GET api/admin/data-quality/summary** -> lib/api/userbase.ts (GET)
- **POST api/admin/data-quality/summary** -> [Django-admin-only]
- **PUT api/admin/data-quality/summary** -> [Django-admin-only]
- **PATCH api/admin/data-quality/summary** -> [Django-admin-only]
- **DELETE api/admin/data-quality/summary** -> [Django-admin-only]
- **TRACE api/admin/data-quality/summary** -> [Django-admin-only]
- **GET api/admin/data-quality/users** -> lib/api/userbase.ts (GET), lib/api/users.ts (GET)
- **POST api/admin/data-quality/users** -> lib/api/userbase.ts (POST)
- **PUT api/admin/data-quality/users** -> [Django-admin-only]
- **PATCH api/admin/data-quality/users** -> [Django-admin-only]
- **DELETE api/admin/data-quality/users** -> [Django-admin-only]
- **TRACE api/admin/data-quality/users** -> [Django-admin-only]
- **GET api/admin/data-quality/recompute** -> [Django-admin-only]
- **POST api/admin/data-quality/recompute** -> lib/api/userbase.ts (POST)
- **PUT api/admin/data-quality/recompute** -> [Django-admin-only]
- **PATCH api/admin/data-quality/recompute** -> [Django-admin-only]
- **DELETE api/admin/data-quality/recompute** -> [Django-admin-only]
- **TRACE api/admin/data-quality/recompute** -> [Django-admin-only]
- **GET api/admin/data-quality/audit** -> lib/api/userbase.ts (GET)
- **POST api/admin/data-quality/audit** -> [Django-admin-only]
- **PUT api/admin/data-quality/audit** -> [Django-admin-only]
- **PATCH api/admin/data-quality/audit** -> [Django-admin-only]
- **DELETE api/admin/data-quality/audit** -> [Django-admin-only]
- **TRACE api/admin/data-quality/audit** -> [Django-admin-only]
- **GET api/users/assigned-pgs/** -> lib/api/userbase.ts (GET), lib/api/users.ts (GET)
- **POST api/users/assigned-pgs/** -> lib/api/userbase.ts (POST)
- **PUT api/users/assigned-pgs/** -> [backend-only/future]
- **PATCH api/users/assigned-pgs/** -> lib/api/userbase.ts (PATCH)
- **DELETE api/users/assigned-pgs/** -> [backend-only/future]
- **TRACE api/users/assigned-pgs/** -> [backend-only/future]
- **ANY api/users/^$** -> lib/api/userbase.ts (GET), lib/api/userbase.ts (PATCH), lib/api/userbase.ts (POST), lib/api/users.ts (GET)
- **ANY api/users/^(?P<pk>[^/.]+)/$** -> lib/api/userbase.ts (GET), lib/api/userbase.ts (PATCH), lib/api/userbase.ts (POST), lib/api/users.ts (GET)
- **GET api/users/** -> lib/api/userbase.ts (GET), lib/api/users.ts (GET)
- **POST api/users/** -> lib/api/userbase.ts (POST)
- **PUT api/users/** -> [system-only]
- **PATCH api/users/** -> lib/api/userbase.ts (PATCH)
- **DELETE api/users/** -> [system-only]
- **TRACE api/users/** -> [system-only]
- **GET api/programs/<int:program_id>/policy/** -> lib/api/training.ts (GET)
- **POST api/programs/<int:program_id>/policy/** -> lib/api/training.ts (POST)
- **PUT api/programs/<int:program_id>/policy/** -> lib/api/training.ts (PUT)
- **PATCH api/programs/<int:program_id>/policy/** -> [backend-only/future]
- **DELETE api/programs/<int:program_id>/policy/** -> [backend-only/future]
- **TRACE api/programs/<int:program_id>/policy/** -> [backend-only/future]
- **ANY api/programs/<int:program_id>/milestones/^$** -> lib/api/training.ts (PUT), lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/programs/<int:program_id>/milestones/^(?P<pk>[^/.]+)/$** -> lib/api/training.ts (PUT), lib/api/training.ts (POST), lib/api/training.ts (GET)
- **GET api/programs/<int:program_id>/milestones/** -> lib/api/training.ts (GET)
- **POST api/programs/<int:program_id>/milestones/** -> lib/api/training.ts (POST)
- **PUT api/programs/<int:program_id>/milestones/** -> lib/api/training.ts (PUT)
- **PATCH api/programs/<int:program_id>/milestones/** -> [system-only]
- **DELETE api/programs/<int:program_id>/milestones/** -> [system-only]
- **TRACE api/programs/<int:program_id>/milestones/** -> [system-only]
- **GET api/milestones/<int:milestone_id>/requirements/research/** -> [backend-only/future]
- **POST api/milestones/<int:milestone_id>/requirements/research/** -> [backend-only/future]
- **PUT api/milestones/<int:milestone_id>/requirements/research/** -> [backend-only/future]
- **PATCH api/milestones/<int:milestone_id>/requirements/research/** -> [backend-only/future]
- **DELETE api/milestones/<int:milestone_id>/requirements/research/** -> [backend-only/future]
- **TRACE api/milestones/<int:milestone_id>/requirements/research/** -> [backend-only/future]
- **GET api/utrmc/approvals/rotations/** -> lib/api/training.ts (GET)
- **POST api/utrmc/approvals/rotations/** -> lib/api/training.ts (POST)
- **PUT api/utrmc/approvals/rotations/** -> [backend-only/future]
- **PATCH api/utrmc/approvals/rotations/** -> [backend-only/future]
- **DELETE api/utrmc/approvals/rotations/** -> [backend-only/future]
- **TRACE api/utrmc/approvals/rotations/** -> [backend-only/future]
- **GET api/utrmc/approvals/leaves/** -> lib/api/training.ts (GET)
- **POST api/utrmc/approvals/leaves/** -> lib/api/training.ts (POST)
- **PUT api/utrmc/approvals/leaves/** -> [backend-only/future]
- **PATCH api/utrmc/approvals/leaves/** -> [backend-only/future]
- **DELETE api/utrmc/approvals/leaves/** -> [backend-only/future]
- **TRACE api/utrmc/approvals/leaves/** -> [backend-only/future]
- **GET api/utrmc/eligibility/** -> [backend-only/future]
- **POST api/utrmc/eligibility/** -> [backend-only/future]
- **PUT api/utrmc/eligibility/** -> [backend-only/future]
- **PATCH api/utrmc/eligibility/** -> [backend-only/future]
- **DELETE api/utrmc/eligibility/** -> [backend-only/future]
- **TRACE api/utrmc/eligibility/** -> [backend-only/future]
- **GET api/my/rotations/** -> lib/api/training.ts (GET)
- **POST api/my/rotations/** -> lib/api/training.ts (POST)
- **PUT api/my/rotations/** -> [backend-only/future]
- **PATCH api/my/rotations/** -> [backend-only/future]
- **DELETE api/my/rotations/** -> [backend-only/future]
- **TRACE api/my/rotations/** -> [backend-only/future]
- **GET api/my/leaves/** -> lib/api/training.ts (GET)
- **POST api/my/leaves/** -> lib/api/training.ts (POST)
- **PUT api/my/leaves/** -> [backend-only/future]
- **PATCH api/my/leaves/** -> [backend-only/future]
- **DELETE api/my/leaves/** -> [backend-only/future]
- **TRACE api/my/leaves/** -> [backend-only/future]
- **GET api/my/research/** -> lib/api/training.ts (GET)
- **POST api/my/research/** -> lib/api/training.ts (POST)
- **PUT api/my/research/** -> [backend-only/future]
- **PATCH api/my/research/** -> lib/api/training.ts (PATCH)
- **DELETE api/my/research/** -> [backend-only/future]
- **TRACE api/my/research/** -> [backend-only/future]
- **GET api/my/research/action/<str:action>/** -> lib/api/training.ts (GET)
- **POST api/my/research/action/<str:action>/** -> lib/api/training.ts (POST)
- **PUT api/my/research/action/<str:action>/** -> [backend-only/future]
- **PATCH api/my/research/action/<str:action>/** -> lib/api/training.ts (PATCH)
- **DELETE api/my/research/action/<str:action>/** -> [backend-only/future]
- **TRACE api/my/research/action/<str:action>/** -> [backend-only/future]
- **GET api/my/thesis/** -> lib/api/training.ts (GET)
- **POST api/my/thesis/** -> lib/api/training.ts (POST)
- **PUT api/my/thesis/** -> [backend-only/future]
- **PATCH api/my/thesis/** -> [backend-only/future]
- **DELETE api/my/thesis/** -> [backend-only/future]
- **TRACE api/my/thesis/** -> [backend-only/future]
- **GET api/my/thesis/submit/** -> lib/api/training.ts (GET)
- **POST api/my/thesis/submit/** -> lib/api/training.ts (POST)
- **PUT api/my/thesis/submit/** -> [backend-only/future]
- **PATCH api/my/thesis/submit/** -> [backend-only/future]
- **DELETE api/my/thesis/submit/** -> [backend-only/future]
- **TRACE api/my/thesis/submit/** -> [backend-only/future]
- **GET api/my/workshops/** -> lib/api/training.ts (GET)
- **POST api/my/workshops/** -> lib/api/training.ts (POST)
- **PUT api/my/workshops/** -> [backend-only/future]
- **PATCH api/my/workshops/** -> [backend-only/future]
- **DELETE api/my/workshops/** -> lib/api/training.ts (DELETE)
- **TRACE api/my/workshops/** -> [backend-only/future]
- **GET api/my/workshops/<int:pk>/** -> lib/api/training.ts (GET)
- **POST api/my/workshops/<int:pk>/** -> lib/api/training.ts (POST)
- **PUT api/my/workshops/<int:pk>/** -> [backend-only/future]
- **PATCH api/my/workshops/<int:pk>/** -> [backend-only/future]
- **DELETE api/my/workshops/<int:pk>/** -> lib/api/training.ts (DELETE)
- **TRACE api/my/workshops/<int:pk>/** -> [backend-only/future]
- **GET api/my/eligibility/** -> lib/api/training.ts (GET)
- **POST api/my/eligibility/** -> [backend-only/future]
- **PUT api/my/eligibility/** -> [backend-only/future]
- **PATCH api/my/eligibility/** -> [backend-only/future]
- **DELETE api/my/eligibility/** -> [backend-only/future]
- **TRACE api/my/eligibility/** -> [backend-only/future]
- **GET api/logbook/review-queue/** -> lib/api/training.ts (GET)
- **POST api/logbook/review-queue/** -> lib/api/training.ts (POST)
- **PUT api/logbook/review-queue/** -> [backend-only/future]
- **PATCH api/logbook/review-queue/** -> lib/api/training.ts (PATCH)
- **DELETE api/logbook/review-queue/** -> [backend-only/future]
- **TRACE api/logbook/review-queue/** -> [backend-only/future]
- **GET api/logbook/my-threshold/** -> lib/api/training.ts (GET)
- **POST api/logbook/my-threshold/** -> lib/api/training.ts (POST)
- **PUT api/logbook/my-threshold/** -> [backend-only/future]
- **PATCH api/logbook/my-threshold/** -> lib/api/training.ts (PATCH)
- **DELETE api/logbook/my-threshold/** -> [backend-only/future]
- **TRACE api/logbook/my-threshold/** -> [backend-only/future]
- **GET api/submissions/synopsis/** -> lib/api/training.ts (GET)
- **POST api/submissions/synopsis/** -> lib/api/training.ts (POST)
- **PUT api/submissions/synopsis/** -> [backend-only/future]
- **PATCH api/submissions/synopsis/** -> lib/api/training.ts (PATCH)
- **DELETE api/submissions/synopsis/** -> [backend-only/future]
- **TRACE api/submissions/synopsis/** -> [backend-only/future]
- **GET api/submissions/synopsis/documents/** -> lib/api/training.ts (GET)
- **POST api/submissions/synopsis/documents/** -> lib/api/training.ts (POST)
- **PUT api/submissions/synopsis/documents/** -> [backend-only/future]
- **PATCH api/submissions/synopsis/documents/** -> lib/api/training.ts (PATCH)
- **DELETE api/submissions/synopsis/documents/** -> [backend-only/future]
- **TRACE api/submissions/synopsis/documents/** -> [backend-only/future]
- **GET api/submissions/synopsis/submit/** -> lib/api/training.ts (GET)
- **POST api/submissions/synopsis/submit/** -> lib/api/training.ts (POST)
- **PUT api/submissions/synopsis/submit/** -> [backend-only/future]
- **PATCH api/submissions/synopsis/submit/** -> lib/api/training.ts (PATCH)
- **DELETE api/submissions/synopsis/submit/** -> [backend-only/future]
- **TRACE api/submissions/synopsis/submit/** -> [backend-only/future]
- **GET api/submissions/synopsis/review-queue/** -> lib/api/training.ts (GET)
- **POST api/submissions/synopsis/review-queue/** -> lib/api/training.ts (POST)
- **PUT api/submissions/synopsis/review-queue/** -> [backend-only/future]
- **PATCH api/submissions/synopsis/review-queue/** -> lib/api/training.ts (PATCH)
- **DELETE api/submissions/synopsis/review-queue/** -> [backend-only/future]
- **TRACE api/submissions/synopsis/review-queue/** -> [backend-only/future]
- **GET api/submissions/synopsis/<int:submission_id>/review/** -> lib/api/training.ts (GET)
- **POST api/submissions/synopsis/<int:submission_id>/review/** -> lib/api/training.ts (POST)
- **PUT api/submissions/synopsis/<int:submission_id>/review/** -> [backend-only/future]
- **PATCH api/submissions/synopsis/<int:submission_id>/review/** -> lib/api/training.ts (PATCH)
- **DELETE api/submissions/synopsis/<int:submission_id>/review/** -> [backend-only/future]
- **TRACE api/submissions/synopsis/<int:submission_id>/review/** -> [backend-only/future]
- **GET api/submissions/thesis/** -> lib/api/training.ts (GET)
- **POST api/submissions/thesis/** -> lib/api/training.ts (POST)
- **PUT api/submissions/thesis/** -> [backend-only/future]
- **PATCH api/submissions/thesis/** -> lib/api/training.ts (PATCH)
- **DELETE api/submissions/thesis/** -> [backend-only/future]
- **TRACE api/submissions/thesis/** -> [backend-only/future]
- **GET api/submissions/thesis/documents/** -> lib/api/training.ts (GET)
- **POST api/submissions/thesis/documents/** -> lib/api/training.ts (POST)
- **PUT api/submissions/thesis/documents/** -> [backend-only/future]
- **PATCH api/submissions/thesis/documents/** -> lib/api/training.ts (PATCH)
- **DELETE api/submissions/thesis/documents/** -> [backend-only/future]
- **TRACE api/submissions/thesis/documents/** -> [backend-only/future]
- **GET api/submissions/thesis/submit/** -> lib/api/training.ts (GET)
- **POST api/submissions/thesis/submit/** -> lib/api/training.ts (POST)
- **PUT api/submissions/thesis/submit/** -> [backend-only/future]
- **PATCH api/submissions/thesis/submit/** -> lib/api/training.ts (PATCH)
- **DELETE api/submissions/thesis/submit/** -> [backend-only/future]
- **TRACE api/submissions/thesis/submit/** -> [backend-only/future]
- **GET api/submissions/thesis/review-queue/** -> lib/api/training.ts (GET)
- **POST api/submissions/thesis/review-queue/** -> lib/api/training.ts (POST)
- **PUT api/submissions/thesis/review-queue/** -> [backend-only/future]
- **PATCH api/submissions/thesis/review-queue/** -> lib/api/training.ts (PATCH)
- **DELETE api/submissions/thesis/review-queue/** -> [backend-only/future]
- **TRACE api/submissions/thesis/review-queue/** -> [backend-only/future]
- **GET api/submissions/thesis/<int:submission_id>/review/** -> lib/api/training.ts (GET)
- **POST api/submissions/thesis/<int:submission_id>/review/** -> lib/api/training.ts (POST)
- **PUT api/submissions/thesis/<int:submission_id>/review/** -> [backend-only/future]
- **PATCH api/submissions/thesis/<int:submission_id>/review/** -> lib/api/training.ts (PATCH)
- **DELETE api/submissions/thesis/<int:submission_id>/review/** -> [backend-only/future]
- **TRACE api/submissions/thesis/<int:submission_id>/review/** -> [backend-only/future]
- **GET api/submissions/certificates/** -> lib/api/training.ts (GET)
- **POST api/submissions/certificates/** -> [backend-only/future]
- **PUT api/submissions/certificates/** -> [backend-only/future]
- **PATCH api/submissions/certificates/** -> [backend-only/future]
- **DELETE api/submissions/certificates/** -> [backend-only/future]
- **TRACE api/submissions/certificates/** -> [backend-only/future]
- **GET api/rotations/completions/** -> lib/api/training.ts (GET)
- **POST api/rotations/completions/** -> lib/api/training.ts (POST)
- **PUT api/rotations/completions/** -> [backend-only/future]
- **PATCH api/rotations/completions/** -> [backend-only/future]
- **DELETE api/rotations/completions/** -> [backend-only/future]
- **TRACE api/rotations/completions/** -> [backend-only/future]
- **GET api/rotations/completions/<int:completion_id>/verify/** -> lib/api/training.ts (GET)
- **POST api/rotations/completions/<int:completion_id>/verify/** -> lib/api/training.ts (POST)
- **PUT api/rotations/completions/<int:completion_id>/verify/** -> [backend-only/future]
- **PATCH api/rotations/completions/<int:completion_id>/verify/** -> [backend-only/future]
- **DELETE api/rotations/completions/<int:completion_id>/verify/** -> [backend-only/future]
- **TRACE api/rotations/completions/<int:completion_id>/verify/** -> [backend-only/future]
- **GET api/dashboard/resident/** -> lib/api/training.ts (GET)
- **POST api/dashboard/resident/** -> [backend-only/future]
- **PUT api/dashboard/resident/** -> [backend-only/future]
- **PATCH api/dashboard/resident/** -> [backend-only/future]
- **DELETE api/dashboard/resident/** -> [backend-only/future]
- **TRACE api/dashboard/resident/** -> [backend-only/future]
- **GET api/dashboard/supervisor/** -> lib/api/training.ts (GET)
- **POST api/dashboard/supervisor/** -> [backend-only/future]
- **PUT api/dashboard/supervisor/** -> [backend-only/future]
- **PATCH api/dashboard/supervisor/** -> [backend-only/future]
- **DELETE api/dashboard/supervisor/** -> [backend-only/future]
- **TRACE api/dashboard/supervisor/** -> [backend-only/future]
- **GET api/dashboard/hod/** -> lib/api/training.ts (GET)
- **POST api/dashboard/hod/** -> [backend-only/future]
- **PUT api/dashboard/hod/** -> [backend-only/future]
- **PATCH api/dashboard/hod/** -> [backend-only/future]
- **DELETE api/dashboard/hod/** -> [backend-only/future]
- **TRACE api/dashboard/hod/** -> [backend-only/future]
- **GET api/dashboard/utrmc/** -> lib/api/training.ts (GET)
- **POST api/dashboard/utrmc/** -> [backend-only/future]
- **PUT api/dashboard/utrmc/** -> [backend-only/future]
- **PATCH api/dashboard/utrmc/** -> [backend-only/future]
- **DELETE api/dashboard/utrmc/** -> [backend-only/future]
- **TRACE api/dashboard/utrmc/** -> [backend-only/future]
- **ANY api/^programs/$** -> lib/api/training.ts (PUT), lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^programs/(?P<pk>[^/.]+)/$** -> lib/api/training.ts (PUT), lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^program-templates/$** -> lib/api/training.ts (PATCH), lib/api/training.ts (POST), lib/api/training.ts (DELETE), lib/api/training.ts (GET)
- **ANY api/^program-templates/(?P<pk>[^/.]+)/$** -> lib/api/training.ts (PATCH), lib/api/training.ts (POST), lib/api/training.ts (DELETE), lib/api/training.ts (GET)
- **ANY api/^resident-training/$** -> lib/api/training.ts (GET)
- **ANY api/^resident-training/(?P<pk>[^/.]+)/$** -> lib/api/training.ts (GET)
- **ANY api/^rotations/$** -> lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^rotations/(?P<pk>[^/.]+)/$** -> lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^rotations/(?P<pk>[^/.]+)/activate/$** -> lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^rotations/(?P<pk>[^/.]+)/complete/$** -> lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^rotations/(?P<pk>[^/.]+)/confirm-completion/$** -> lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^rotations/(?P<pk>[^/.]+)/hod-approve/$** -> lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^rotations/(?P<pk>[^/.]+)/reject/$** -> lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^rotations/(?P<pk>[^/.]+)/returned/$** -> lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^rotations/(?P<pk>[^/.]+)/review-application/$** -> lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^rotations/(?P<pk>[^/.]+)/submit/$** -> lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^rotations/(?P<pk>[^/.]+)/utrmc-approve/$** -> lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^rotations/(?P<pk>[^/.]+)/verify-completion/$** -> lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^leaves/$** -> lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^leaves/(?P<pk>[^/.]+)/$** -> lib/api/training.ts (POST)
- **ANY api/^leaves/(?P<pk>[^/.]+)/approve/$** -> lib/api/training.ts (POST)
- **ANY api/^leaves/(?P<pk>[^/.]+)/reject/$** -> lib/api/training.ts (POST)
- **ANY api/^leaves/(?P<pk>[^/.]+)/submit/$** -> lib/api/training.ts (POST)
- **ANY api/^postings/$** -> lib/api/training.ts (POST), lib/api/training.ts (DELETE), lib/api/training.ts (GET)
- **ANY api/^postings/(?P<pk>[^/.]+)/$** -> lib/api/training.ts (POST), lib/api/training.ts (DELETE), lib/api/training.ts (GET)
- **ANY api/^postings/(?P<pk>[^/.]+)/approve/$** -> lib/api/training.ts (POST), lib/api/training.ts (DELETE), lib/api/training.ts (GET)
- **ANY api/^postings/(?P<pk>[^/.]+)/complete/$** -> lib/api/training.ts (POST), lib/api/training.ts (DELETE), lib/api/training.ts (GET)
- **ANY api/^postings/(?P<pk>[^/.]+)/reject/$** -> lib/api/training.ts (POST), lib/api/training.ts (DELETE), lib/api/training.ts (GET)
- **ANY api/^workshops/$** -> lib/api/training.ts (POST), lib/api/training.ts (DELETE), lib/api/training.ts (GET)
- **ANY api/^workshops/(?P<pk>[^/.]+)/$** -> lib/api/training.ts (DELETE), lib/api/training.ts (GET)
- **ANY api/^logbook/config/$** -> lib/api/training.ts (PATCH), lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^logbook/config/(?P<pk>[^/.]+)/$** -> lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^logbook/$** -> lib/api/training.ts (PATCH), lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^logbook/(?P<pk>[^/.]+)/$** -> lib/api/training.ts (PATCH), lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^logbook/(?P<pk>[^/.]+)/review/$** -> lib/api/training.ts (PATCH), lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^logbook/(?P<pk>[^/.]+)/submit/$** -> lib/api/training.ts (PATCH), lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^logbook/(?P<pk>[^/.]+)/verify/$** -> lib/api/training.ts (PATCH), lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^submissions/requirements/$** -> lib/api/training.ts (GET)
- **ANY api/^submissions/requirements/(?P<pk>[^/.]+)/$** -> lib/api/training.ts (GET)
- **ANY api/^rotations/requirements/$** -> lib/api/training.ts (POST), lib/api/training.ts (GET)
- **ANY api/^rotations/requirements/(?P<pk>[^/.]+)/$** -> lib/api/training.ts (POST), lib/api/training.ts (GET)
- **GET api/** -> lib/api/audit.ts (GET), lib/api/userbase.ts (GET), lib/api/hospitals.ts (GET), lib/api/auth.ts (GET), lib/api/bulk.ts (GET), lib/api/notifications.ts (GET), lib/api/training.ts (GET), lib/api/departments.ts (GET), lib/api/users.ts (GET)
- **POST api/** -> lib/api/notifications.ts (POST), lib/api/audit.ts (POST), lib/api/departments.ts (POST), lib/api/userbase.ts (POST), lib/api/training.ts (POST), lib/api/hospitals.ts (POST), lib/api/auth.ts (POST)
- **PUT api/** -> lib/api/training.ts (PUT)
- **PATCH api/** -> lib/api/departments.ts (PATCH), lib/api/notifications.ts (PATCH), lib/api/hospitals.ts (PATCH), lib/api/training.ts (PATCH), lib/api/auth.ts (PATCH), lib/api/userbase.ts (PATCH)
- **DELETE api/** -> lib/api/hospitals.ts (DELETE), lib/api/training.ts (DELETE), lib/api/departments.ts (DELETE), lib/api/userbase.ts (DELETE)
- **TRACE api/** -> [system-only]
- **GET api/supervisor/rotations/pending/** -> lib/api/training.ts (GET)
- **POST api/supervisor/rotations/pending/** -> lib/api/training.ts (POST)
- **PUT api/supervisor/rotations/pending/** -> [backend-only/future]
- **PATCH api/supervisor/rotations/pending/** -> [backend-only/future]
- **DELETE api/supervisor/rotations/pending/** -> [backend-only/future]
- **TRACE api/supervisor/rotations/pending/** -> [backend-only/future]
- **GET api/supervisor/research-approvals/** -> lib/api/training.ts (GET)
- **POST api/supervisor/research-approvals/** -> [backend-only/future]
- **PUT api/supervisor/research-approvals/** -> [backend-only/future]
- **PATCH api/supervisor/research-approvals/** -> [backend-only/future]
- **DELETE api/supervisor/research-approvals/** -> [backend-only/future]
- **TRACE api/supervisor/research-approvals/** -> [backend-only/future]
- **GET api/residents/me/summary/** -> lib/api/training.ts (GET)
- **POST api/residents/me/summary/** -> [backend-only/future]
- **PUT api/residents/me/summary/** -> [backend-only/future]
- **PATCH api/residents/me/summary/** -> [backend-only/future]
- **DELETE api/residents/me/summary/** -> [backend-only/future]
- **TRACE api/residents/me/summary/** -> [backend-only/future]
- **GET api/supervisors/me/summary/** -> lib/api/training.ts (GET)
- **POST api/supervisors/me/summary/** -> [backend-only/future]
- **PUT api/supervisors/me/summary/** -> [backend-only/future]
- **PATCH api/supervisors/me/summary/** -> [backend-only/future]
- **DELETE api/supervisors/me/summary/** -> [backend-only/future]
- **TRACE api/supervisors/me/summary/** -> [backend-only/future]
- **GET api/supervisors/residents/<int:resident_id>/progress/** -> lib/api/training.ts (GET)
- **POST api/supervisors/residents/<int:resident_id>/progress/** -> [backend-only/future]
- **PUT api/supervisors/residents/<int:resident_id>/progress/** -> [backend-only/future]
- **PATCH api/supervisors/residents/<int:resident_id>/progress/** -> lib/api/userbase.ts (PATCH)
- **DELETE api/supervisors/residents/<int:resident_id>/progress/** -> [backend-only/future]
- **TRACE api/supervisors/residents/<int:resident_id>/progress/** -> [backend-only/future]
- **GET api/system/settings/** -> lib/api/training.ts (GET)
- **POST api/system/settings/** -> [backend-only/future]
- **PUT api/system/settings/** -> [backend-only/future]
- **PATCH api/system/settings/** -> [backend-only/future]
- **DELETE api/system/settings/** -> [backend-only/future]
- **TRACE api/system/settings/** -> [backend-only/future]
- **ANY academics/api/^departments/$** -> lib/api/departments.ts (POST), lib/api/userbase.ts (POST), lib/api/departments.ts (GET)
- **ANY academics/api/^departments/(?P<pk>[^/.]+)/$** -> lib/api/departments.ts (PATCH), lib/api/userbase.ts (DELETE), lib/api/userbase.ts (POST), lib/api/departments.ts (DELETE), lib/api/departments.ts (POST), lib/api/userbase.ts (PATCH), lib/api/departments.ts (GET)
- **GET academics/api/** -> [system-only]
- **POST academics/api/** -> [system-only]
- **PUT academics/api/** -> [system-only]
- **PATCH academics/api/** -> [system-only]
- **DELETE academics/api/** -> [system-only]
- **TRACE academics/api/** -> [system-only]
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
- **GET api/auth/me/** -> [backend-only/future]
- **POST api/auth/me/** -> [backend-only/future]
- **PUT api/auth/me/** -> [backend-only/future]
- **PATCH api/auth/me/** -> [backend-only/future]
- **DELETE api/auth/me/** -> [backend-only/future]
- **TRACE api/auth/me/** -> [backend-only/future]
- **GET api/auth/profile/** -> lib/api/auth.ts (GET)
- **PATCH api/auth/profile/update/** -> lib/api/auth.ts (PATCH)
- **PUT api/auth/profile/update/** -> [backend-only/future]
- **POST api/auth/password-reset/** -> lib/api/auth.ts (POST)
- **POST api/auth/password-reset/confirm/** -> lib/api/auth.ts (POST)
- **POST api/auth/change-password/** -> lib/api/auth.ts (POST)
- **GET api/backup_center/backups/** -> [backend-only/future]
- **POST api/backup_center/backups/** -> [backend-only/future]
- **PUT api/backup_center/backups/** -> [backend-only/future]
- **PATCH api/backup_center/backups/** -> [backend-only/future]
- **DELETE api/backup_center/backups/** -> [backend-only/future]
- **TRACE api/backup_center/backups/** -> [backend-only/future]
- **GET api/backup_center/backups/<int:pk>/** -> [backend-only/future]
- **POST api/backup_center/backups/<int:pk>/** -> [backend-only/future]
- **PUT api/backup_center/backups/<int:pk>/** -> [backend-only/future]
- **PATCH api/backup_center/backups/<int:pk>/** -> [backend-only/future]
- **DELETE api/backup_center/backups/<int:pk>/** -> [backend-only/future]
- **TRACE api/backup_center/backups/<int:pk>/** -> [backend-only/future]
- **GET api/backup_center/backups/create-routine/** -> [backend-only/future]
- **POST api/backup_center/backups/create-routine/** -> [backend-only/future]
- **PUT api/backup_center/backups/create-routine/** -> [backend-only/future]
- **PATCH api/backup_center/backups/create-routine/** -> [backend-only/future]
- **DELETE api/backup_center/backups/create-routine/** -> [backend-only/future]
- **TRACE api/backup_center/backups/create-routine/** -> [backend-only/future]
- **GET api/backup_center/backups/create-disaster/** -> [backend-only/future]
- **POST api/backup_center/backups/create-disaster/** -> [backend-only/future]
- **PUT api/backup_center/backups/create-disaster/** -> [backend-only/future]
- **PATCH api/backup_center/backups/create-disaster/** -> [backend-only/future]
- **DELETE api/backup_center/backups/create-disaster/** -> [backend-only/future]
- **TRACE api/backup_center/backups/create-disaster/** -> [backend-only/future]
- **GET api/backup_center/backups/<int:pk>/download/** -> [backend-only/future]
- **POST api/backup_center/backups/<int:pk>/download/** -> [backend-only/future]
- **PUT api/backup_center/backups/<int:pk>/download/** -> [backend-only/future]
- **PATCH api/backup_center/backups/<int:pk>/download/** -> [backend-only/future]
- **DELETE api/backup_center/backups/<int:pk>/download/** -> [backend-only/future]
- **TRACE api/backup_center/backups/<int:pk>/download/** -> [backend-only/future]
- **GET api/backup_center/backups/<int:pk>/delete/** -> [backend-only/future]
- **POST api/backup_center/backups/<int:pk>/delete/** -> [backend-only/future]
- **PUT api/backup_center/backups/<int:pk>/delete/** -> [backend-only/future]
- **PATCH api/backup_center/backups/<int:pk>/delete/** -> [backend-only/future]
- **DELETE api/backup_center/backups/<int:pk>/delete/** -> [backend-only/future]
- **TRACE api/backup_center/backups/<int:pk>/delete/** -> [backend-only/future]
- **GET api/backup_center/backups/<int:pk>/validate/** -> [backend-only/future]
- **POST api/backup_center/backups/<int:pk>/validate/** -> [backend-only/future]
- **PUT api/backup_center/backups/<int:pk>/validate/** -> [backend-only/future]
- **PATCH api/backup_center/backups/<int:pk>/validate/** -> [backend-only/future]
- **DELETE api/backup_center/backups/<int:pk>/validate/** -> [backend-only/future]
- **TRACE api/backup_center/backups/<int:pk>/validate/** -> [backend-only/future]
- **GET api/backup_center/restores/** -> [backend-only/future]
- **POST api/backup_center/restores/** -> [backend-only/future]
- **PUT api/backup_center/restores/** -> [backend-only/future]
- **PATCH api/backup_center/restores/** -> [backend-only/future]
- **DELETE api/backup_center/restores/** -> [backend-only/future]
- **TRACE api/backup_center/restores/** -> [backend-only/future]
- **GET api/backup_center/restores/upload/** -> [backend-only/future]
- **POST api/backup_center/restores/upload/** -> [backend-only/future]
- **PUT api/backup_center/restores/upload/** -> [backend-only/future]
- **PATCH api/backup_center/restores/upload/** -> [backend-only/future]
- **DELETE api/backup_center/restores/upload/** -> [backend-only/future]
- **TRACE api/backup_center/restores/upload/** -> [backend-only/future]
- **GET api/backup_center/restores/<int:pk>/validate/** -> [backend-only/future]
- **POST api/backup_center/restores/<int:pk>/validate/** -> [backend-only/future]
- **PUT api/backup_center/restores/<int:pk>/validate/** -> [backend-only/future]
- **PATCH api/backup_center/restores/<int:pk>/validate/** -> [backend-only/future]
- **DELETE api/backup_center/restores/<int:pk>/validate/** -> [backend-only/future]
- **TRACE api/backup_center/restores/<int:pk>/validate/** -> [backend-only/future]
- **GET api/backup_center/restores/<int:pk>/dry-run/** -> [backend-only/future]
- **POST api/backup_center/restores/<int:pk>/dry-run/** -> [backend-only/future]
- **PUT api/backup_center/restores/<int:pk>/dry-run/** -> [backend-only/future]
- **PATCH api/backup_center/restores/<int:pk>/dry-run/** -> [backend-only/future]
- **DELETE api/backup_center/restores/<int:pk>/dry-run/** -> [backend-only/future]
- **TRACE api/backup_center/restores/<int:pk>/dry-run/** -> [backend-only/future]
- **GET api/backup_center/restores/<int:pk>/confirm/** -> [backend-only/future]
- **POST api/backup_center/restores/<int:pk>/confirm/** -> [backend-only/future]
- **PUT api/backup_center/restores/<int:pk>/confirm/** -> [backend-only/future]
- **PATCH api/backup_center/restores/<int:pk>/confirm/** -> [backend-only/future]
- **DELETE api/backup_center/restores/<int:pk>/confirm/** -> [backend-only/future]
- **TRACE api/backup_center/restores/<int:pk>/confirm/** -> [backend-only/future]
- **GET api/backup_center/audit-logs/** -> [backend-only/future]
- **POST api/backup_center/audit-logs/** -> [backend-only/future]
- **PUT api/backup_center/audit-logs/** -> [backend-only/future]
- **PATCH api/backup_center/audit-logs/** -> [backend-only/future]
- **DELETE api/backup_center/audit-logs/** -> [backend-only/future]
- **TRACE api/backup_center/audit-logs/** -> [backend-only/future]
- **GET api/backup_center/google-drive/status/** -> [backend-only/future]
- **POST api/backup_center/google-drive/status/** -> [backend-only/future]
- **PUT api/backup_center/google-drive/status/** -> [backend-only/future]
- **PATCH api/backup_center/google-drive/status/** -> [backend-only/future]
- **DELETE api/backup_center/google-drive/status/** -> [backend-only/future]
- **TRACE api/backup_center/google-drive/status/** -> [backend-only/future]
- **GET api/backup_center/google-drive/connect/** -> [backend-only/future]
- **POST api/backup_center/google-drive/connect/** -> [backend-only/future]
- **PUT api/backup_center/google-drive/connect/** -> [backend-only/future]
- **PATCH api/backup_center/google-drive/connect/** -> [backend-only/future]
- **DELETE api/backup_center/google-drive/connect/** -> [backend-only/future]
- **TRACE api/backup_center/google-drive/connect/** -> [backend-only/future]
- **GET api/backup_center/google-drive/oauth/callback/** -> [backend-only/future]
- **POST api/backup_center/google-drive/oauth/callback/** -> [backend-only/future]
- **PUT api/backup_center/google-drive/oauth/callback/** -> [backend-only/future]
- **PATCH api/backup_center/google-drive/oauth/callback/** -> [backend-only/future]
- **DELETE api/backup_center/google-drive/oauth/callback/** -> [backend-only/future]
- **TRACE api/backup_center/google-drive/oauth/callback/** -> [backend-only/future]
- **GET api/backup_center/google-drive/disconnect/** -> [backend-only/future]
- **POST api/backup_center/google-drive/disconnect/** -> [backend-only/future]
- **PUT api/backup_center/google-drive/disconnect/** -> [backend-only/future]
- **PATCH api/backup_center/google-drive/disconnect/** -> [backend-only/future]
- **DELETE api/backup_center/google-drive/disconnect/** -> [backend-only/future]
- **TRACE api/backup_center/google-drive/disconnect/** -> [backend-only/future]
- **GET api/backup_center/google-drive/health-check/** -> [backend-only/future]
- **POST api/backup_center/google-drive/health-check/** -> [backend-only/future]
- **PUT api/backup_center/google-drive/health-check/** -> [backend-only/future]
- **PATCH api/backup_center/google-drive/health-check/** -> [backend-only/future]
- **DELETE api/backup_center/google-drive/health-check/** -> [backend-only/future]
- **TRACE api/backup_center/google-drive/health-check/** -> [backend-only/future]
- **GET api/backup_center/google-drive/create-folder/** -> [backend-only/future]
- **POST api/backup_center/google-drive/create-folder/** -> [backend-only/future]
- **PUT api/backup_center/google-drive/create-folder/** -> [backend-only/future]
- **PATCH api/backup_center/google-drive/create-folder/** -> [backend-only/future]
- **DELETE api/backup_center/google-drive/create-folder/** -> [backend-only/future]
- **TRACE api/backup_center/google-drive/create-folder/** -> [backend-only/future]
- **GET api/backup_center/backups/<int:pk>/google-drive/upload/** -> [backend-only/future]
- **POST api/backup_center/backups/<int:pk>/google-drive/upload/** -> [backend-only/future]
- **PUT api/backup_center/backups/<int:pk>/google-drive/upload/** -> [backend-only/future]
- **PATCH api/backup_center/backups/<int:pk>/google-drive/upload/** -> [backend-only/future]
- **DELETE api/backup_center/backups/<int:pk>/google-drive/upload/** -> [backend-only/future]
- **TRACE api/backup_center/backups/<int:pk>/google-drive/upload/** -> [backend-only/future]
- **GET api/backup_center/backups/<int:pk>/google-drive/verify/** -> [backend-only/future]
- **POST api/backup_center/backups/<int:pk>/google-drive/verify/** -> [backend-only/future]
- **PUT api/backup_center/backups/<int:pk>/google-drive/verify/** -> [backend-only/future]
- **PATCH api/backup_center/backups/<int:pk>/google-drive/verify/** -> [backend-only/future]
- **DELETE api/backup_center/backups/<int:pk>/google-drive/verify/** -> [backend-only/future]
- **TRACE api/backup_center/backups/<int:pk>/google-drive/verify/** -> [backend-only/future]
- **GET api/backup_center/backups/<int:pk>/google-drive/download/** -> [backend-only/future]
- **POST api/backup_center/backups/<int:pk>/google-drive/download/** -> [backend-only/future]
- **PUT api/backup_center/backups/<int:pk>/google-drive/download/** -> [backend-only/future]
- **PATCH api/backup_center/backups/<int:pk>/google-drive/download/** -> [backend-only/future]
- **DELETE api/backup_center/backups/<int:pk>/google-drive/download/** -> [backend-only/future]
- **TRACE api/backup_center/backups/<int:pk>/google-drive/download/** -> [backend-only/future]
- **GET api/backup_center/google-drive/list/** -> [backend-only/future]
- **POST api/backup_center/google-drive/list/** -> [backend-only/future]
- **PUT api/backup_center/google-drive/list/** -> [backend-only/future]
- **PATCH api/backup_center/google-drive/list/** -> [backend-only/future]
- **DELETE api/backup_center/google-drive/list/** -> [backend-only/future]
- **TRACE api/backup_center/google-drive/list/** -> [backend-only/future]

### Frontend to Backend
- **GET /api/hospitals/** in `lib/api/hospitals.ts` -> `api/^hospitals/$`, `api/^hospitals\.(?P<format>[a-z0-9]+)/?$`, `api/^hospitals/(?P<pk>[^/.]+)/$`, `api/^hospitals/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^hospitals/(?P<pk>[^/.]+)/departments/$`, `api/^hospitals/(?P<pk>[^/.]+)/departments\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **POST /api/hospitals/** in `lib/api/hospitals.ts` -> `api/^hospitals/$`, `api/^hospitals\.(?P<format>[a-z0-9]+)/?$`, `api/^hospitals/(?P<pk>[^/.]+)/$`, `api/^hospitals/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^hospitals/(?P<pk>[^/.]+)/departments/$`, `api/^hospitals/(?P<pk>[^/.]+)/departments\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **PATCH /api/hospitals/${id}/** in `lib/api/hospitals.ts` -> `api/^hospitals/$`, `api/^hospitals/(?P<pk>[^/.]+)/$`, `api/^hospitals/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^hospitals/(?P<pk>[^/.]+)/departments/$`, `api/^hospitals/(?P<pk>[^/.]+)/departments\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **DELETE /api/hospitals/${id}/** in `lib/api/hospitals.ts` -> `api/^hospitals/$`, `api/^hospitals/(?P<pk>[^/.]+)/$`, `api/^hospitals/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^hospitals/(?P<pk>[^/.]+)/departments/$`, `api/^hospitals/(?P<pk>[^/.]+)/departments\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/audit/activity/** in `lib/api/audit.ts` -> `api/audit/^activity/$`, `api/audit/^activity\.(?P<format>[a-z0-9]+)/?$`, `api/audit/^activity/export/$`, `api/audit/^activity/export\.(?P<format>[a-z0-9]+)/?$`, `api/audit/^activity/(?P<pk>[^/.]+)/$`, `api/audit/^activity/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/audit/`, `api/audit/<drf_format_suffix:format>`, `api/`, `api/`
- **GET /api/audit/reports/** in `lib/api/audit.ts` -> `api/audit/^reports/$`, `api/audit/^reports\.(?P<format>[a-z0-9]+)/?$`, `api/audit/^reports/latest/$`, `api/audit/^reports/latest\.(?P<format>[a-z0-9]+)/?$`, `api/audit/`, `api/audit/<drf_format_suffix:format>`, `api/`, `api/`
- **POST /api/audit/reports/** in `lib/api/audit.ts` -> `api/audit/^reports/$`, `api/audit/^reports\.(?P<format>[a-z0-9]+)/?$`, `api/audit/^reports/latest/$`, `api/audit/^reports/latest\.(?P<format>[a-z0-9]+)/?$`, `api/audit/`, `api/audit/<drf_format_suffix:format>`, `api/`, `api/`
- **GET /api/bulk/templates/${resource}/** in `lib/api/bulk.ts` -> `api/bulk/templates/<str:resource>/`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/bulk/exports/${resource}/** in `lib/api/bulk.ts` -> `api/bulk/exports/<str:resource>/`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **POST /api/hospitals/** in `lib/api/userbase.ts` -> `api/^hospitals/$`, `api/^hospitals\.(?P<format>[a-z0-9]+)/?$`, `api/^hospitals/(?P<pk>[^/.]+)/$`, `api/^hospitals/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^hospitals/(?P<pk>[^/.]+)/departments/$`, `api/^hospitals/(?P<pk>[^/.]+)/departments\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **PATCH /api/hospitals/${id}/** in `lib/api/userbase.ts` -> `api/^hospitals/$`, `api/^hospitals/(?P<pk>[^/.]+)/$`, `api/^hospitals/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^hospitals/(?P<pk>[^/.]+)/departments/$`, `api/^hospitals/(?P<pk>[^/.]+)/departments\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/hospitals/${id}/departments/** in `lib/api/userbase.ts` -> `api/^hospitals/$`, `api/^hospitals/(?P<pk>[^/.]+)/$`, `api/^hospitals/(?P<pk>[^/.]+)/departments/$`, `api/^hospitals/(?P<pk>[^/.]+)/departments\.(?P<format>[a-z0-9]+)/?$`, `api/^departments/$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **DELETE /api/hospitals/${id}/** in `lib/api/userbase.ts` -> `api/^hospitals/$`, `api/^hospitals/(?P<pk>[^/.]+)/$`, `api/^hospitals/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^hospitals/(?P<pk>[^/.]+)/departments/$`, `api/^hospitals/(?P<pk>[^/.]+)/departments\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **POST /api/departments/** in `lib/api/userbase.ts` -> `rotations/api/departments/<int:hospital_id>/`, `api/bulk/import-departments/`, `api/^hospitals/(?P<pk>[^/.]+)/departments/$`, `api/^hospitals/(?P<pk>[^/.]+)/departments\.(?P<format>[a-z0-9]+)/?$`, `api/^departments/$`, `api/^departments\.(?P<format>[a-z0-9]+)/?$`, `api/^departments/(?P<pk>[^/.]+)/$`, `api/^departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^departments/(?P<pk>[^/.]+)/roster/$`, `api/^departments/(?P<pk>[^/.]+)/roster\.(?P<format>[a-z0-9]+)/?$`, `api/^hospital-departments/$`, `api/^hospital-departments\.(?P<format>[a-z0-9]+)/?$`, `api/^hospital-departments/(?P<pk>[^/.]+)/$`, `api/^hospital-departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`, `academics/api/^departments/$`, `academics/api/^departments\.(?P<format>[a-z0-9]+)/?$`, `academics/api/^departments/(?P<pk>[^/.]+)/$`, `academics/api/^departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`
- **PATCH /api/departments/${id}/** in `lib/api/userbase.ts` -> `rotations/api/departments/<int:hospital_id>/`, `api/^departments/$`, `api/^departments/(?P<pk>[^/.]+)/$`, `api/^departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^departments/(?P<pk>[^/.]+)/roster/$`, `api/^departments/(?P<pk>[^/.]+)/roster\.(?P<format>[a-z0-9]+)/?$`, `api/^hospital-departments/(?P<pk>[^/.]+)/$`, `api/^hospital-departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`, `academics/api/^departments/(?P<pk>[^/.]+)/$`, `academics/api/^departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`
- **DELETE /api/departments/${id}/** in `lib/api/userbase.ts` -> `rotations/api/departments/<int:hospital_id>/`, `api/^departments/$`, `api/^departments/(?P<pk>[^/.]+)/$`, `api/^departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^departments/(?P<pk>[^/.]+)/roster/$`, `api/^departments/(?P<pk>[^/.]+)/roster\.(?P<format>[a-z0-9]+)/?$`, `api/^hospital-departments/(?P<pk>[^/.]+)/$`, `api/^hospital-departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`, `academics/api/^departments/(?P<pk>[^/.]+)/$`, `academics/api/^departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`
- **GET /api/departments/${id}/roster/** in `lib/api/userbase.ts` -> `api/^departments/$`, `api/^departments/(?P<pk>[^/.]+)/$`, `api/^departments/(?P<pk>[^/.]+)/roster/$`, `api/^departments/(?P<pk>[^/.]+)/roster\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **POST /api/hospital-departments/** in `lib/api/userbase.ts` -> `api/^departments/$`, `api/^hospital-departments/$`, `api/^hospital-departments\.(?P<format>[a-z0-9]+)/?$`, `api/^hospital-departments/(?P<pk>[^/.]+)/$`, `api/^hospital-departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **PATCH /api/hospital-departments/${id}/** in `lib/api/userbase.ts` -> `api/^departments/$`, `api/^departments/(?P<pk>[^/.]+)/$`, `api/^hospital-departments/$`, `api/^hospital-departments/(?P<pk>[^/.]+)/$`, `api/^hospital-departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **POST /api/users/** in `lib/api/userbase.ts` -> `users/api/users/search/`, `users/api/supervisors/specialty/<str:specialty>/`, `users/api/user/<int:pk>/stats/`, `users/api/stats/`, `users/api/admin/stats/`, `users/api/user-statistics/`, `users/api/user-performance/`, `api/`, `api/<drf_format_suffix:format>`, `api/admin/data-quality/users`, `api/users/assigned-pgs/`, `api/users/^$`, `api/users/^\.(?P<format>[a-z0-9]+)/?$`, `api/users/^(?P<pk>[^/.]+)/$`, `api/users/^(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/users/`, `api/users/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/users/${id}/** in `lib/api/userbase.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/users/assigned-pgs/`, `api/users/^$`, `api/users/^\.(?P<format>[a-z0-9]+)/?$`, `api/users/^(?P<pk>[^/.]+)/$`, `api/users/^(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/users/`, `api/users/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **PATCH /api/users/${id}/** in `lib/api/userbase.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/users/assigned-pgs/`, `api/users/^$`, `api/users/^\.(?P<format>[a-z0-9]+)/?$`, `api/users/^(?P<pk>[^/.]+)/$`, `api/users/^(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/users/`, `api/users/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **PATCH /api/residents/${userId}/** in `lib/api/userbase.ts` -> `api/^residents/$`, `api/^residents/(?P<user_id>[^/.]+)/$`, `api/^residents/(?P<user_id>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`, `api/supervisors/residents/<int:resident_id>/progress/`
- **PATCH /api/staff/${userId}/** in `lib/api/userbase.ts` -> `api/^staff/$`, `api/^staff/(?P<user_id>[^/.]+)/$`, `api/^staff/(?P<user_id>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/admin/data-quality/summary** in `lib/api/userbase.ts` -> `api/`, `api/admin/data-quality/summary`, `api/`
- **GET /api/admin/data-quality/users** in `lib/api/userbase.ts` -> `api/`, `api/admin/data-quality/users`, `api/users/^$`, `api/users/`, `api/`
- **POST /api/admin/data-quality/recompute** in `lib/api/userbase.ts` -> `api/`, `api/admin/data-quality/recompute`, `api/`
- **GET /api/admin/data-quality/audit** in `lib/api/userbase.ts` -> `api/audit/`, `api/`, `api/admin/data-quality/audit`, `api/`
- **POST /api/department-memberships/** in `lib/api/userbase.ts` -> `api/^department-memberships/$`, `api/^department-memberships\.(?P<format>[a-z0-9]+)/?$`, `api/^department-memberships/(?P<pk>[^/.]+)/$`, `api/^department-memberships/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **PATCH /api/department-memberships/${id}/** in `lib/api/userbase.ts` -> `api/^department-memberships/$`, `api/^department-memberships/(?P<pk>[^/.]+)/$`, `api/^department-memberships/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **DELETE /api/department-memberships/${id}/** in `lib/api/userbase.ts` -> `api/^department-memberships/$`, `api/^department-memberships/(?P<pk>[^/.]+)/$`, `api/^department-memberships/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **POST /api/hospital-assignments/** in `lib/api/userbase.ts` -> `api/^hospital-assignments/$`, `api/^hospital-assignments\.(?P<format>[a-z0-9]+)/?$`, `api/^hospital-assignments/(?P<pk>[^/.]+)/$`, `api/^hospital-assignments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **PATCH /api/hospital-assignments/${id}/** in `lib/api/userbase.ts` -> `api/^hospital-assignments/$`, `api/^hospital-assignments/(?P<pk>[^/.]+)/$`, `api/^hospital-assignments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **DELETE /api/hospital-assignments/${id}/** in `lib/api/userbase.ts` -> `api/^hospital-assignments/$`, `api/^hospital-assignments/(?P<pk>[^/.]+)/$`, `api/^hospital-assignments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/supervision-links/** in `lib/api/userbase.ts` -> `api/^supervision-links/$`, `api/^supervision-links\.(?P<format>[a-z0-9]+)/?$`, `api/^supervision-links/(?P<pk>[^/.]+)/$`, `api/^supervision-links/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **POST /api/supervision-links/** in `lib/api/userbase.ts` -> `api/^supervision-links/$`, `api/^supervision-links\.(?P<format>[a-z0-9]+)/?$`, `api/^supervision-links/(?P<pk>[^/.]+)/$`, `api/^supervision-links/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **PATCH /api/supervision-links/${id}/** in `lib/api/userbase.ts` -> `api/^supervision-links/$`, `api/^supervision-links/(?P<pk>[^/.]+)/$`, `api/^supervision-links/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/hod-assignments/** in `lib/api/userbase.ts` -> `api/^hod-assignments/$`, `api/^hod-assignments\.(?P<format>[a-z0-9]+)/?$`, `api/^hod-assignments/(?P<pk>[^/.]+)/$`, `api/^hod-assignments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **POST /api/hod-assignments/** in `lib/api/userbase.ts` -> `api/^hod-assignments/$`, `api/^hod-assignments\.(?P<format>[a-z0-9]+)/?$`, `api/^hod-assignments/(?P<pk>[^/.]+)/$`, `api/^hod-assignments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **PATCH /api/hod-assignments/${id}/** in `lib/api/userbase.ts` -> `api/^hod-assignments/$`, `api/^hod-assignments/(?P<pk>[^/.]+)/$`, `api/^hod-assignments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/programs/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/programs/<int:program_id>/policy/`, `api/programs/<int:program_id>/milestones/^$`, `api/programs/<int:program_id>/milestones/^\.(?P<format>[a-z0-9]+)/?$`, `api/programs/<int:program_id>/milestones/^(?P<pk>[^/.]+)/$`, `api/programs/<int:program_id>/milestones/^(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/programs/<int:program_id>/milestones/`, `api/programs/<int:program_id>/milestones/<drf_format_suffix:format>`, `api/^programs/$`, `api/^programs\.(?P<format>[a-z0-9]+)/?$`, `api/^programs/(?P<pk>[^/.]+)/$`, `api/^programs/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/programs/${id}/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/programs/<int:program_id>/policy/`, `api/programs/<int:program_id>/milestones/^$`, `api/programs/<int:program_id>/milestones/^\.(?P<format>[a-z0-9]+)/?$`, `api/programs/<int:program_id>/milestones/^(?P<pk>[^/.]+)/$`, `api/programs/<int:program_id>/milestones/^(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/programs/<int:program_id>/milestones/`, `api/programs/<int:program_id>/milestones/<drf_format_suffix:format>`, `api/^programs/$`, `api/^programs/(?P<pk>[^/.]+)/$`, `api/^programs/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **POST /api/programs/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/programs/<int:program_id>/policy/`, `api/programs/<int:program_id>/milestones/^$`, `api/programs/<int:program_id>/milestones/^\.(?P<format>[a-z0-9]+)/?$`, `api/programs/<int:program_id>/milestones/^(?P<pk>[^/.]+)/$`, `api/programs/<int:program_id>/milestones/^(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/programs/<int:program_id>/milestones/`, `api/programs/<int:program_id>/milestones/<drf_format_suffix:format>`, `api/^programs/$`, `api/^programs\.(?P<format>[a-z0-9]+)/?$`, `api/^programs/(?P<pk>[^/.]+)/$`, `api/^programs/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **PUT /api/programs/${id}/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/programs/<int:program_id>/policy/`, `api/programs/<int:program_id>/milestones/^$`, `api/programs/<int:program_id>/milestones/^\.(?P<format>[a-z0-9]+)/?$`, `api/programs/<int:program_id>/milestones/^(?P<pk>[^/.]+)/$`, `api/programs/<int:program_id>/milestones/^(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/programs/<int:program_id>/milestones/`, `api/programs/<int:program_id>/milestones/<drf_format_suffix:format>`, `api/^programs/$`, `api/^programs/(?P<pk>[^/.]+)/$`, `api/^programs/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/programs/${programId}/policy/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/programs/<int:program_id>/policy/`, `api/^programs/$`, `api/^programs/(?P<pk>[^/.]+)/$`, `api/`, `api/<drf_format_suffix:format>`
- **PUT /api/programs/${programId}/policy/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/programs/<int:program_id>/policy/`, `api/^programs/$`, `api/^programs/(?P<pk>[^/.]+)/$`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/programs/${programId}/milestones/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/programs/<int:program_id>/milestones/^$`, `api/programs/<int:program_id>/milestones/^\.(?P<format>[a-z0-9]+)/?$`, `api/programs/<int:program_id>/milestones/^(?P<pk>[^/.]+)/$`, `api/programs/<int:program_id>/milestones/^(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/programs/<int:program_id>/milestones/`, `api/programs/<int:program_id>/milestones/<drf_format_suffix:format>`, `api/^programs/$`, `api/^programs/(?P<pk>[^/.]+)/$`, `api/`, `api/<drf_format_suffix:format>`
- **POST /api/programs/${programId}/milestones/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/programs/<int:program_id>/milestones/^$`, `api/programs/<int:program_id>/milestones/^\.(?P<format>[a-z0-9]+)/?$`, `api/programs/<int:program_id>/milestones/^(?P<pk>[^/.]+)/$`, `api/programs/<int:program_id>/milestones/^(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/programs/<int:program_id>/milestones/`, `api/programs/<int:program_id>/milestones/<drf_format_suffix:format>`, `api/^programs/$`, `api/^programs/(?P<pk>[^/.]+)/$`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/my/research/** in `lib/api/training.ts` -> `api/`, `api/my/research/`, `api/my/research/action/<str:action>/`, `api/`
- **POST /api/my/research/** in `lib/api/training.ts` -> `api/`, `api/my/research/`, `api/my/research/action/<str:action>/`, `api/`
- **PATCH /api/my/research/** in `lib/api/training.ts` -> `api/`, `api/my/research/`, `api/my/research/action/<str:action>/`, `api/`
- **PATCH /api/my/research/** in `lib/api/training.ts` -> `api/`, `api/my/research/`, `api/my/research/action/<str:action>/`, `api/`
- **POST /api/my/research/action/${action}/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/my/research/`, `api/my/research/action/<str:action>/`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/supervisor/research-approvals/** in `lib/api/training.ts` -> `api/`, `api/`, `api/supervisor/research-approvals/`
- **POST /api/my/research/action/supervisor-approve/** in `lib/api/training.ts` -> `api/`, `api/my/research/`, `api/my/research/action/<str:action>/`, `api/`
- **POST /api/my/research/action/supervisor-return/** in `lib/api/training.ts` -> `api/`, `api/my/research/`, `api/my/research/action/<str:action>/`, `api/`
- **GET /api/my/thesis/** in `lib/api/training.ts` -> `api/`, `api/my/thesis/`, `api/my/thesis/submit/`, `api/`
- **POST /api/my/thesis/** in `lib/api/training.ts` -> `api/`, `api/my/thesis/`, `api/my/thesis/submit/`, `api/`
- **POST /api/my/thesis/submit/** in `lib/api/training.ts` -> `api/`, `api/my/thesis/`, `api/my/thesis/submit/`, `api/`
- **GET /api/workshops/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/my/workshops/`, `api/my/workshops/<int:pk>/`, `api/^workshops/$`, `api/^workshops\.(?P<format>[a-z0-9]+)/?$`, `api/^workshops/(?P<pk>[^/.]+)/$`, `api/^workshops/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/my/workshops/** in `lib/api/training.ts` -> `api/`, `api/my/workshops/`, `api/my/workshops/<int:pk>/`, `api/^workshops/$`, `api/`
- **POST /api/my/workshops/** in `lib/api/training.ts` -> `api/`, `api/my/workshops/`, `api/my/workshops/<int:pk>/`, `api/^workshops/$`, `api/`
- **DELETE /api/my/workshops/${id}/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/my/workshops/`, `api/my/workshops/<int:pk>/`, `api/^workshops/$`, `api/^workshops/(?P<pk>[^/.]+)/$`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/my/eligibility/** in `lib/api/training.ts` -> `api/`, `api/my/eligibility/`, `api/`
- **GET /api/residents/me/summary/** in `lib/api/training.ts` -> `api/^residents/$`, `api/`, `api/`, `api/residents/me/summary/`
- **GET /api/supervisors/me/summary/** in `lib/api/training.ts` -> `api/`, `api/`, `api/supervisors/me/summary/`
- **GET /api/supervisors/residents/${residentId}/progress/** in `lib/api/training.ts` -> `api/^residents/$`, `api/^residents/(?P<user_id>[^/.]+)/$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`, `api/supervisors/residents/<int:resident_id>/progress/`
- **GET /api/resident-training/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/^resident-training/$`, `api/^resident-training\.(?P<format>[a-z0-9]+)/?$`, `api/^resident-training/(?P<pk>[^/.]+)/$`, `api/^resident-training/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/my/rotations/** in `lib/api/training.ts` -> `api/`, `api/my/rotations/`, `api/^rotations/$`, `api/`
- **GET /api/rotations/** in `lib/api/training.ts` -> `rotations/api/departments/<int:hospital_id>/`, `rotations/api/quick-stats/`, `api/`, `api/<drf_format_suffix:format>`, `api/utrmc/approvals/rotations/`, `api/my/rotations/`, `api/rotations/completions/`, `api/rotations/completions/<int:completion_id>/verify/`, `api/^rotations/$`, `api/^rotations\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/$`, `api/^rotations/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/activate/$`, `api/^rotations/(?P<pk>[^/.]+)/activate\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/complete/$`, `api/^rotations/(?P<pk>[^/.]+)/complete\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/confirm-completion/$`, `api/^rotations/(?P<pk>[^/.]+)/confirm-completion\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/hod-approve/$`, `api/^rotations/(?P<pk>[^/.]+)/hod-approve\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/reject/$`, `api/^rotations/(?P<pk>[^/.]+)/reject\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/returned/$`, `api/^rotations/(?P<pk>[^/.]+)/returned\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/review-application/$`, `api/^rotations/(?P<pk>[^/.]+)/review-application\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/submit/$`, `api/^rotations/(?P<pk>[^/.]+)/submit\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/utrmc-approve/$`, `api/^rotations/(?P<pk>[^/.]+)/utrmc-approve\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/verify-completion/$`, `api/^rotations/(?P<pk>[^/.]+)/verify-completion\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/requirements/$`, `api/^rotations/requirements\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/requirements/(?P<pk>[^/.]+)/$`, `api/^rotations/requirements/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/supervisor/rotations/pending/`
- **GET /api/supervisor/rotations/pending/** in `lib/api/training.ts` -> `api/`, `api/^rotations/$`, `api/`, `api/supervisor/rotations/pending/`
- **GET /api/utrmc/approvals/rotations/** in `lib/api/training.ts` -> `api/`, `api/utrmc/approvals/rotations/`, `api/^rotations/$`, `api/`
- **POST /api/rotations/** in `lib/api/training.ts` -> `rotations/api/departments/<int:hospital_id>/`, `rotations/api/quick-stats/`, `api/`, `api/<drf_format_suffix:format>`, `api/utrmc/approvals/rotations/`, `api/my/rotations/`, `api/rotations/completions/`, `api/rotations/completions/<int:completion_id>/verify/`, `api/^rotations/$`, `api/^rotations\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/$`, `api/^rotations/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/activate/$`, `api/^rotations/(?P<pk>[^/.]+)/activate\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/complete/$`, `api/^rotations/(?P<pk>[^/.]+)/complete\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/confirm-completion/$`, `api/^rotations/(?P<pk>[^/.]+)/confirm-completion\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/hod-approve/$`, `api/^rotations/(?P<pk>[^/.]+)/hod-approve\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/reject/$`, `api/^rotations/(?P<pk>[^/.]+)/reject\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/returned/$`, `api/^rotations/(?P<pk>[^/.]+)/returned\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/review-application/$`, `api/^rotations/(?P<pk>[^/.]+)/review-application\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/submit/$`, `api/^rotations/(?P<pk>[^/.]+)/submit\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/utrmc-approve/$`, `api/^rotations/(?P<pk>[^/.]+)/utrmc-approve\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/verify-completion/$`, `api/^rotations/(?P<pk>[^/.]+)/verify-completion\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/requirements/$`, `api/^rotations/requirements\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/requirements/(?P<pk>[^/.]+)/$`, `api/^rotations/requirements/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/supervisor/rotations/pending/`
- **POST /api/rotations/${id}/${action}/** in `lib/api/training.ts` -> `rotations/api/quick-stats/`, `api/`, `api/<drf_format_suffix:format>`, `api/^rotations/$`, `api/^rotations/(?P<pk>[^/.]+)/$`, `api/^rotations/(?P<pk>[^/.]+)/activate/$`, `api/^rotations/(?P<pk>[^/.]+)/activate\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/complete/$`, `api/^rotations/(?P<pk>[^/.]+)/complete\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/confirm-completion/$`, `api/^rotations/(?P<pk>[^/.]+)/confirm-completion\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/hod-approve/$`, `api/^rotations/(?P<pk>[^/.]+)/hod-approve\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/reject/$`, `api/^rotations/(?P<pk>[^/.]+)/reject\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/returned/$`, `api/^rotations/(?P<pk>[^/.]+)/returned\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/review-application/$`, `api/^rotations/(?P<pk>[^/.]+)/review-application\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/submit/$`, `api/^rotations/(?P<pk>[^/.]+)/submit\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/utrmc-approve/$`, `api/^rotations/(?P<pk>[^/.]+)/utrmc-approve\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/(?P<pk>[^/.]+)/verify-completion/$`, `api/^rotations/(?P<pk>[^/.]+)/verify-completion\.(?P<format>[a-z0-9]+)/?$`, `api/^rotations/requirements/(?P<pk>[^/.]+)/$`, `api/^rotations/requirements/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/logbook/** in `lib/api/training.ts` -> `logbook/api/stats/`, `logbook/api/template/<int:template_id>/preview/`, `logbook/api/entry/<int:entry_id>/complexity/`, `logbook/api/update-statistics/`, `api/`, `api/<drf_format_suffix:format>`, `api/logbook/review-queue/`, `api/logbook/my-threshold/`, `api/^logbook/config/$`, `api/^logbook/config\.(?P<format>[a-z0-9]+)/?$`, `api/^logbook/config/(?P<pk>[^/.]+)/$`, `api/^logbook/config/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^logbook/$`, `api/^logbook\.(?P<format>[a-z0-9]+)/?$`, `api/^logbook/(?P<pk>[^/.]+)/$`, `api/^logbook/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^logbook/(?P<pk>[^/.]+)/review/$`, `api/^logbook/(?P<pk>[^/.]+)/review\.(?P<format>[a-z0-9]+)/?$`, `api/^logbook/(?P<pk>[^/.]+)/submit/$`, `api/^logbook/(?P<pk>[^/.]+)/submit\.(?P<format>[a-z0-9]+)/?$`, `api/^logbook/(?P<pk>[^/.]+)/verify/$`, `api/^logbook/(?P<pk>[^/.]+)/verify\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **POST /api/logbook/** in `lib/api/training.ts` -> `logbook/api/stats/`, `logbook/api/template/<int:template_id>/preview/`, `logbook/api/entry/<int:entry_id>/complexity/`, `logbook/api/update-statistics/`, `api/`, `api/<drf_format_suffix:format>`, `api/logbook/review-queue/`, `api/logbook/my-threshold/`, `api/^logbook/config/$`, `api/^logbook/config\.(?P<format>[a-z0-9]+)/?$`, `api/^logbook/config/(?P<pk>[^/.]+)/$`, `api/^logbook/config/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^logbook/$`, `api/^logbook\.(?P<format>[a-z0-9]+)/?$`, `api/^logbook/(?P<pk>[^/.]+)/$`, `api/^logbook/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^logbook/(?P<pk>[^/.]+)/review/$`, `api/^logbook/(?P<pk>[^/.]+)/review\.(?P<format>[a-z0-9]+)/?$`, `api/^logbook/(?P<pk>[^/.]+)/submit/$`, `api/^logbook/(?P<pk>[^/.]+)/submit\.(?P<format>[a-z0-9]+)/?$`, `api/^logbook/(?P<pk>[^/.]+)/verify/$`, `api/^logbook/(?P<pk>[^/.]+)/verify\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **PATCH /api/logbook/${id}/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/logbook/review-queue/`, `api/logbook/my-threshold/`, `api/^logbook/config/$`, `api/^logbook/config\.(?P<format>[a-z0-9]+)/?$`, `api/^logbook/$`, `api/^logbook/(?P<pk>[^/.]+)/$`, `api/^logbook/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^logbook/(?P<pk>[^/.]+)/review/$`, `api/^logbook/(?P<pk>[^/.]+)/review\.(?P<format>[a-z0-9]+)/?$`, `api/^logbook/(?P<pk>[^/.]+)/submit/$`, `api/^logbook/(?P<pk>[^/.]+)/submit\.(?P<format>[a-z0-9]+)/?$`, `api/^logbook/(?P<pk>[^/.]+)/verify/$`, `api/^logbook/(?P<pk>[^/.]+)/verify\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **POST /api/logbook/${id}/submit/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/^logbook/$`, `api/^logbook/(?P<pk>[^/.]+)/$`, `api/^logbook/(?P<pk>[^/.]+)/submit/$`, `api/^logbook/(?P<pk>[^/.]+)/submit\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **POST /api/logbook/${id}/review/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/^logbook/$`, `api/^logbook/(?P<pk>[^/.]+)/$`, `api/^logbook/(?P<pk>[^/.]+)/review/$`, `api/^logbook/(?P<pk>[^/.]+)/review\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/logbook/review-queue/** in `lib/api/training.ts` -> `api/`, `api/logbook/review-queue/`, `api/^logbook/$`, `api/^logbook/(?P<pk>[^/.]+)/$`, `api/`
- **GET /api/logbook/my-threshold/** in `lib/api/training.ts` -> `api/`, `api/logbook/my-threshold/`, `api/^logbook/$`, `api/^logbook/(?P<pk>[^/.]+)/$`, `api/`
- **GET /api/submissions/requirements/** in `lib/api/training.ts` -> `api/`, `api/^submissions/requirements/$`, `api/^submissions/requirements\.(?P<format>[a-z0-9]+)/?$`, `api/^submissions/requirements/(?P<pk>[^/.]+)/$`, `api/^submissions/requirements/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`
- **GET /api/submissions/synopsis/** in `lib/api/training.ts` -> `api/`, `api/submissions/synopsis/`, `api/submissions/synopsis/documents/`, `api/submissions/synopsis/submit/`, `api/submissions/synopsis/review-queue/`, `api/submissions/synopsis/<int:submission_id>/review/`, `api/`
- **POST /api/submissions/synopsis/** in `lib/api/training.ts` -> `api/`, `api/submissions/synopsis/`, `api/submissions/synopsis/documents/`, `api/submissions/synopsis/submit/`, `api/submissions/synopsis/review-queue/`, `api/submissions/synopsis/<int:submission_id>/review/`, `api/`
- **PATCH /api/submissions/synopsis/** in `lib/api/training.ts` -> `api/`, `api/submissions/synopsis/`, `api/submissions/synopsis/documents/`, `api/submissions/synopsis/submit/`, `api/submissions/synopsis/review-queue/`, `api/submissions/synopsis/<int:submission_id>/review/`, `api/`
- **POST /api/submissions/synopsis/submit/** in `lib/api/training.ts` -> `api/`, `api/submissions/synopsis/`, `api/submissions/synopsis/submit/`, `api/`
- **GET /api/submissions/thesis/** in `lib/api/training.ts` -> `api/`, `api/submissions/thesis/`, `api/submissions/thesis/documents/`, `api/submissions/thesis/submit/`, `api/submissions/thesis/review-queue/`, `api/submissions/thesis/<int:submission_id>/review/`, `api/`
- **POST /api/submissions/thesis/** in `lib/api/training.ts` -> `api/`, `api/submissions/thesis/`, `api/submissions/thesis/documents/`, `api/submissions/thesis/submit/`, `api/submissions/thesis/review-queue/`, `api/submissions/thesis/<int:submission_id>/review/`, `api/`
- **PATCH /api/submissions/thesis/** in `lib/api/training.ts` -> `api/`, `api/submissions/thesis/`, `api/submissions/thesis/documents/`, `api/submissions/thesis/submit/`, `api/submissions/thesis/review-queue/`, `api/submissions/thesis/<int:submission_id>/review/`, `api/`
- **POST /api/submissions/thesis/submit/** in `lib/api/training.ts` -> `api/`, `api/submissions/thesis/`, `api/submissions/thesis/submit/`, `api/`
- **GET /api/submissions/synopsis/review-queue/** in `lib/api/training.ts` -> `api/`, `api/submissions/synopsis/`, `api/submissions/synopsis/review-queue/`, `api/`
- **GET /api/submissions/thesis/review-queue/** in `lib/api/training.ts` -> `api/`, `api/submissions/thesis/`, `api/submissions/thesis/review-queue/`, `api/`
- **GET /api/submissions/certificates/** in `lib/api/training.ts` -> `api/`, `api/submissions/certificates/`, `api/`
- **GET /api/rotations/completions/** in `lib/api/training.ts` -> `api/`, `api/rotations/completions/`, `api/rotations/completions/<int:completion_id>/verify/`, `api/^rotations/$`, `api/^rotations/(?P<pk>[^/.]+)/$`, `api/`
- **GET /api/dashboard/resident/** in `lib/api/training.ts` -> `api/`, `api/dashboard/resident/`, `api/`
- **GET /api/dashboard/supervisor/** in `lib/api/training.ts` -> `api/`, `api/dashboard/supervisor/`, `api/`
- **GET /api/dashboard/hod/** in `lib/api/training.ts` -> `api/`, `api/dashboard/hod/`, `api/`
- **GET /api/dashboard/utrmc/** in `lib/api/training.ts` -> `api/`, `api/dashboard/utrmc/`, `api/`
- **GET /api/my/leaves/** in `lib/api/training.ts` -> `api/`, `api/my/leaves/`, `api/^leaves/$`, `api/`
- **POST /api/leaves/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/utrmc/approvals/leaves/`, `api/my/leaves/`, `api/^leaves/$`, `api/^leaves\.(?P<format>[a-z0-9]+)/?$`, `api/^leaves/(?P<pk>[^/.]+)/$`, `api/^leaves/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^leaves/(?P<pk>[^/.]+)/approve/$`, `api/^leaves/(?P<pk>[^/.]+)/approve\.(?P<format>[a-z0-9]+)/?$`, `api/^leaves/(?P<pk>[^/.]+)/reject/$`, `api/^leaves/(?P<pk>[^/.]+)/reject\.(?P<format>[a-z0-9]+)/?$`, `api/^leaves/(?P<pk>[^/.]+)/submit/$`, `api/^leaves/(?P<pk>[^/.]+)/submit\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **POST /api/leaves/${id}/submit/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/^leaves/$`, `api/^leaves/(?P<pk>[^/.]+)/$`, `api/^leaves/(?P<pk>[^/.]+)/submit/$`, `api/^leaves/(?P<pk>[^/.]+)/submit\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/utrmc/approvals/leaves/** in `lib/api/training.ts` -> `api/`, `api/utrmc/approvals/leaves/`, `api/^leaves/$`, `api/`
- **POST /api/leaves/${id}/approve/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/^leaves/$`, `api/^leaves/(?P<pk>[^/.]+)/$`, `api/^leaves/(?P<pk>[^/.]+)/approve/$`, `api/^leaves/(?P<pk>[^/.]+)/approve\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **POST /api/leaves/${id}/reject/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/^leaves/$`, `api/^leaves/(?P<pk>[^/.]+)/$`, `api/^leaves/(?P<pk>[^/.]+)/reject/$`, `api/^leaves/(?P<pk>[^/.]+)/reject\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/system/settings/** in `lib/api/training.ts` -> `api/`, `api/`, `api/system/settings/`
- **GET /api/program-templates/?program=${programId}** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/^program-templates/$`, `api/^program-templates\.(?P<format>[a-z0-9]+)/?$`, `api/^program-templates/(?P<pk>[^/.]+)/$`, `api/^program-templates/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **POST /api/program-templates/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/^program-templates/$`, `api/^program-templates\.(?P<format>[a-z0-9]+)/?$`, `api/^program-templates/(?P<pk>[^/.]+)/$`, `api/^program-templates/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **PATCH /api/program-templates/${id}/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/^program-templates/$`, `api/^program-templates/(?P<pk>[^/.]+)/$`, `api/^program-templates/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **DELETE /api/program-templates/${id}/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/^program-templates/$`, `api/^program-templates/(?P<pk>[^/.]+)/$`, `api/^program-templates/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/postings/${qs}** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/^postings/$`, `api/^postings/(?P<pk>[^/.]+)/$`, `api/^postings/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^postings/(?P<pk>[^/.]+)/approve/$`, `api/^postings/(?P<pk>[^/.]+)/approve\.(?P<format>[a-z0-9]+)/?$`, `api/^postings/(?P<pk>[^/.]+)/complete/$`, `api/^postings/(?P<pk>[^/.]+)/complete\.(?P<format>[a-z0-9]+)/?$`, `api/^postings/(?P<pk>[^/.]+)/reject/$`, `api/^postings/(?P<pk>[^/.]+)/reject\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **POST /api/postings/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/^postings/$`, `api/^postings\.(?P<format>[a-z0-9]+)/?$`, `api/^postings/(?P<pk>[^/.]+)/$`, `api/^postings/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^postings/(?P<pk>[^/.]+)/approve/$`, `api/^postings/(?P<pk>[^/.]+)/approve\.(?P<format>[a-z0-9]+)/?$`, `api/^postings/(?P<pk>[^/.]+)/complete/$`, `api/^postings/(?P<pk>[^/.]+)/complete\.(?P<format>[a-z0-9]+)/?$`, `api/^postings/(?P<pk>[^/.]+)/reject/$`, `api/^postings/(?P<pk>[^/.]+)/reject\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **POST /api/postings/${id}/${action}/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/^postings/$`, `api/^postings/(?P<pk>[^/.]+)/$`, `api/^postings/(?P<pk>[^/.]+)/approve/$`, `api/^postings/(?P<pk>[^/.]+)/approve\.(?P<format>[a-z0-9]+)/?$`, `api/^postings/(?P<pk>[^/.]+)/complete/$`, `api/^postings/(?P<pk>[^/.]+)/complete\.(?P<format>[a-z0-9]+)/?$`, `api/^postings/(?P<pk>[^/.]+)/reject/$`, `api/^postings/(?P<pk>[^/.]+)/reject\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **DELETE /api/postings/${id}/** in `lib/api/training.ts` -> `api/`, `api/<drf_format_suffix:format>`, `api/^postings/$`, `api/^postings/(?P<pk>[^/.]+)/$`, `api/^postings/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^postings/(?P<pk>[^/.]+)/approve/$`, `api/^postings/(?P<pk>[^/.]+)/approve\.(?P<format>[a-z0-9]+)/?$`, `api/^postings/(?P<pk>[^/.]+)/complete/$`, `api/^postings/(?P<pk>[^/.]+)/complete\.(?P<format>[a-z0-9]+)/?$`, `api/^postings/(?P<pk>[^/.]+)/reject/$`, `api/^postings/(?P<pk>[^/.]+)/reject\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/notifications/** in `lib/api/notifications.ts` -> `api/notifications/`, `api/notifications/mark-read/`, `api/notifications/preferences/`, `api/notifications/unread-count/`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/notifications/** in `lib/api/notifications.ts` -> `api/notifications/`, `api/notifications/mark-read/`, `api/notifications/preferences/`, `api/notifications/unread-count/`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/notifications/unread-count/** in `lib/api/notifications.ts` -> `api/notifications/`, `api/notifications/unread-count/`, `api/`, `api/`
- **POST /api/notifications/mark-read/** in `lib/api/notifications.ts` -> `api/notifications/`, `api/notifications/mark-read/`, `api/`, `api/`
- **GET /api/notifications/preferences/** in `lib/api/notifications.ts` -> `api/notifications/`, `api/notifications/preferences/`, `api/`, `api/`
- **PATCH /api/notifications/preferences/** in `lib/api/notifications.ts` -> `api/notifications/`, `api/notifications/preferences/`, `api/`, `api/`
- **POST /api/auth/login/** in `lib/api/auth.ts` -> `api/`, `api/`, `api/auth/login/`
- **POST /api/auth/register/** in `lib/api/auth.ts` -> `api/`, `api/`, `api/auth/register/`
- **POST /api/auth/logout/** in `lib/api/auth.ts` -> `api/`, `api/`, `api/auth/logout/`
- **GET /api/auth/profile/** in `lib/api/auth.ts` -> `api/`, `api/`, `api/auth/profile/`
- **POST /api/auth/refresh/** in `lib/api/auth.ts` -> `api/`, `api/`, `api/auth/refresh/`
- **PATCH /api/auth/profile/update/** in `lib/api/auth.ts` -> `api/`, `api/`, `api/auth/profile/update/`
- **POST /api/auth/password-reset/** in `lib/api/auth.ts` -> `api/`, `api/`, `api/auth/password-reset/`, `api/auth/password-reset/confirm/`
- **POST /api/auth/password-reset/confirm/** in `lib/api/auth.ts` -> `api/`, `api/`, `api/auth/password-reset/`, `api/auth/password-reset/confirm/`
- **POST /api/auth/change-password/** in `lib/api/auth.ts` -> `api/`, `api/`, `api/auth/change-password/`
- **GET /api/users/assigned-pgs/** in `lib/api/users.ts` -> `api/`, `api/users/assigned-pgs/`, `api/users/^$`, `api/users/^(?P<pk>[^/.]+)/$`, `api/users/`, `api/users/<drf_format_suffix:format>`, `api/`
- **GET /api/users/?role=supervisor** in `lib/api/users.ts` -> `users/api/users/search/`, `users/api/supervisors/specialty/<str:specialty>/`, `users/api/user/<int:pk>/stats/`, `users/api/stats/`, `users/api/admin/stats/`, `users/api/user-statistics/`, `users/api/user-performance/`, `api/`, `api/<drf_format_suffix:format>`, `api/admin/data-quality/users`, `api/users/assigned-pgs/`, `api/users/^$`, `api/users/^\.(?P<format>[a-z0-9]+)/?$`, `api/users/^(?P<pk>[^/.]+)/$`, `api/users/^(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/users/`, `api/users/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/departments/** in `lib/api/departments.ts` -> `rotations/api/departments/<int:hospital_id>/`, `api/bulk/import-departments/`, `api/^hospitals/(?P<pk>[^/.]+)/departments/$`, `api/^hospitals/(?P<pk>[^/.]+)/departments\.(?P<format>[a-z0-9]+)/?$`, `api/^departments/$`, `api/^departments\.(?P<format>[a-z0-9]+)/?$`, `api/^departments/(?P<pk>[^/.]+)/$`, `api/^departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^departments/(?P<pk>[^/.]+)/roster/$`, `api/^departments/(?P<pk>[^/.]+)/roster\.(?P<format>[a-z0-9]+)/?$`, `api/^hospital-departments/$`, `api/^hospital-departments\.(?P<format>[a-z0-9]+)/?$`, `api/^hospital-departments/(?P<pk>[^/.]+)/$`, `api/^hospital-departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`, `academics/api/^departments/$`, `academics/api/^departments\.(?P<format>[a-z0-9]+)/?$`, `academics/api/^departments/(?P<pk>[^/.]+)/$`, `academics/api/^departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`
- **POST /api/departments/** in `lib/api/departments.ts` -> `rotations/api/departments/<int:hospital_id>/`, `api/bulk/import-departments/`, `api/^hospitals/(?P<pk>[^/.]+)/departments/$`, `api/^hospitals/(?P<pk>[^/.]+)/departments\.(?P<format>[a-z0-9]+)/?$`, `api/^departments/$`, `api/^departments\.(?P<format>[a-z0-9]+)/?$`, `api/^departments/(?P<pk>[^/.]+)/$`, `api/^departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^departments/(?P<pk>[^/.]+)/roster/$`, `api/^departments/(?P<pk>[^/.]+)/roster\.(?P<format>[a-z0-9]+)/?$`, `api/^hospital-departments/$`, `api/^hospital-departments\.(?P<format>[a-z0-9]+)/?$`, `api/^hospital-departments/(?P<pk>[^/.]+)/$`, `api/^hospital-departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`, `academics/api/^departments/$`, `academics/api/^departments\.(?P<format>[a-z0-9]+)/?$`, `academics/api/^departments/(?P<pk>[^/.]+)/$`, `academics/api/^departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`
- **PATCH /api/departments/${id}/** in `lib/api/departments.ts` -> `rotations/api/departments/<int:hospital_id>/`, `api/^departments/$`, `api/^departments/(?P<pk>[^/.]+)/$`, `api/^departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^departments/(?P<pk>[^/.]+)/roster/$`, `api/^departments/(?P<pk>[^/.]+)/roster\.(?P<format>[a-z0-9]+)/?$`, `api/^hospital-departments/(?P<pk>[^/.]+)/$`, `api/^hospital-departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`, `academics/api/^departments/(?P<pk>[^/.]+)/$`, `academics/api/^departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`
- **DELETE /api/departments/${id}/** in `lib/api/departments.ts` -> `rotations/api/departments/<int:hospital_id>/`, `api/^departments/$`, `api/^departments/(?P<pk>[^/.]+)/$`, `api/^departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/^departments/(?P<pk>[^/.]+)/roster/$`, `api/^departments/(?P<pk>[^/.]+)/roster\.(?P<format>[a-z0-9]+)/?$`, `api/^hospital-departments/(?P<pk>[^/.]+)/$`, `api/^hospital-departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`, `academics/api/^departments/(?P<pk>[^/.]+)/$`, `academics/api/^departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`
- **GET /api/hospital-departments/** in `lib/api/departments.ts` -> `api/^departments/$`, `api/^hospital-departments/$`, `api/^hospital-departments\.(?P<format>[a-z0-9]+)/?$`, `api/^hospital-departments/(?P<pk>[^/.]+)/$`, `api/^hospital-departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **POST /api/hospital-departments/** in `lib/api/departments.ts` -> `api/^departments/$`, `api/^hospital-departments/$`, `api/^hospital-departments\.(?P<format>[a-z0-9]+)/?$`, `api/^hospital-departments/(?P<pk>[^/.]+)/$`, `api/^hospital-departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **DELETE /api/hospital-departments/${id}/** in `lib/api/departments.ts` -> `api/^departments/$`, `api/^departments/(?P<pk>[^/.]+)/$`, `api/^hospital-departments/$`, `api/^hospital-departments/(?P<pk>[^/.]+)/$`, `api/^hospital-departments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/supervision-links/** in `lib/api/departments.ts` -> `api/^supervision-links/$`, `api/^supervision-links\.(?P<format>[a-z0-9]+)/?$`, `api/^supervision-links/(?P<pk>[^/.]+)/$`, `api/^supervision-links/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **POST /api/supervision-links/** in `lib/api/departments.ts` -> `api/^supervision-links/$`, `api/^supervision-links\.(?P<format>[a-z0-9]+)/?$`, `api/^supervision-links/(?P<pk>[^/.]+)/$`, `api/^supervision-links/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **DELETE /api/supervision-links/${id}/** in `lib/api/departments.ts` -> `api/^supervision-links/$`, `api/^supervision-links/(?P<pk>[^/.]+)/$`, `api/^supervision-links/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **GET /api/hod-assignments/** in `lib/api/departments.ts` -> `api/^hod-assignments/$`, `api/^hod-assignments\.(?P<format>[a-z0-9]+)/?$`, `api/^hod-assignments/(?P<pk>[^/.]+)/$`, `api/^hod-assignments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`
- **POST /api/hod-assignments/** in `lib/api/departments.ts` -> `api/^hod-assignments/$`, `api/^hod-assignments\.(?P<format>[a-z0-9]+)/?$`, `api/^hod-assignments/(?P<pk>[^/.]+)/$`, `api/^hod-assignments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$`, `api/`, `api/<drf_format_suffix:format>`, `api/`, `api/<drf_format_suffix:format>`

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
- `PUT users/api/users/search/` - Reason: [backend-only/future]
- `PATCH users/api/users/search/` - Reason: [backend-only/future]
- `DELETE users/api/users/search/` - Reason: [backend-only/future]
- `TRACE users/api/users/search/` - Reason: [backend-only/future]
- `PUT users/api/supervisors/specialty/<str:specialty>/` - Reason: [backend-only/future]
- `PATCH users/api/supervisors/specialty/<str:specialty>/` - Reason: [backend-only/future]
- `DELETE users/api/supervisors/specialty/<str:specialty>/` - Reason: [backend-only/future]
- `TRACE users/api/supervisors/specialty/<str:specialty>/` - Reason: [backend-only/future]
- `PUT users/api/user/<int:pk>/stats/` - Reason: [backend-only/future]
- `PATCH users/api/user/<int:pk>/stats/` - Reason: [backend-only/future]
- `DELETE users/api/user/<int:pk>/stats/` - Reason: [backend-only/future]
- `TRACE users/api/user/<int:pk>/stats/` - Reason: [backend-only/future]
- `PUT users/api/stats/` - Reason: [backend-only/future]
- `PATCH users/api/stats/` - Reason: [backend-only/future]
- `DELETE users/api/stats/` - Reason: [backend-only/future]
- `TRACE users/api/stats/` - Reason: [backend-only/future]
- `PUT users/api/user-statistics/` - Reason: [backend-only/future]
- `PATCH users/api/user-statistics/` - Reason: [backend-only/future]
- `DELETE users/api/user-statistics/` - Reason: [backend-only/future]
- `TRACE users/api/user-statistics/` - Reason: [backend-only/future]

- *All frontend calls matched a backend endpoint.*

## G) Verdict
**PASS**. All static frontend API calls map successfully.
