from django.urls import path

from sims.users import resident_onboarding_views as views

app_name = "resident_onboarding_api"

urlpatterns = [
    path("residents/upload-preview/", views.ResidentOnboardingUploadView.as_view(), name="resident_upload_preview"),
    path("residents/map-columns/", views.ResidentOnboardingMapView.as_view(), name="resident_map_columns"),
    path("residents/import/", views.ResidentOnboardingImportView.as_view(), name="resident_import"),
    path("residents/generate-logins/", views.ResidentOnboardingGenerateLoginsView.as_view(), name="resident_generate_logins"),
    path("residents/login-sheet/", views.ResidentLoginSheetView.as_view(), name="resident_login_sheet"),
    path("residents/login-sheet/export-excel/", views.ResidentLoginSheetExportExcelView.as_view(), name="resident_login_sheet_export_excel"),
    path("residents/login-sheet/export-pdf/", views.ResidentLoginSheetExportPdfView.as_view(), name="resident_login_sheet_export_pdf"),
    path("residents/mark-issued/", views.ResidentLoginIssuedView.as_view(), name="resident_mark_issued"),
    path("residents/batches/", views.ResidentBatchListView.as_view(), name="resident_batches"),
    path("residents/batches/<int:batch_id>/", views.ResidentBatchDetailView.as_view(), name="resident_batch_detail"),
    path("residents/batches/<int:batch_id>/residents/", views.ResidentBatchResidentsView.as_view(), name="resident_batch_residents"),
    path("residents/batches/<int:batch_id>/generate-logins/", views.ResidentBatchGenerateLoginsView.as_view(), name="resident_batch_generate_logins"),
    path("residents/batches/<int:batch_id>/login-sheet/export/", views.ResidentBatchLoginSheetExportView.as_view(), name="resident_batch_login_sheet_export"),
    path("residents/batches/<int:batch_id>/error-report/", views.ResidentBatchErrorReportView.as_view(), name="resident_batch_error_report"),
    path("residents/incomplete-profiles/", views.ResidentIncompleteProfilesView.as_view(), name="resident_incomplete_profiles"),
    path("residents/incomplete-profiles/export/", views.ResidentIncompleteProfilesExportView.as_view(), name="resident_incomplete_profiles_export"),
    path("residents/<int:resident_id>/reset-password/", views.ResidentResetPasswordView.as_view(), name="resident_reset_password"),
    path("residents/<int:resident_id>/", views.ResidentEditProfileView.as_view(), name="resident_edit_profile"),
    path("residents/<int:resident_id>/mark-profile-complete/", views.ResidentMarkProfileCompleteView.as_view(), name="resident_mark_profile_complete"),
]
