package fmu.pg.sims.ui

/**
 * Stable identifiers for Compose UI / instrumentation tests. Kept in one place so test code
 * and screen code reference the same constants instead of matching on user-visible text (which
 * changes copy) or Material component structure (which changes with library upgrades).
 */
object TestTags {
    const val LOGIN_USERNAME_FIELD = "login_username_field"
    const val LOGIN_PASSWORD_FIELD = "login_password_field"
    const val LOGIN_SUBMIT_BUTTON = "login_submit_button"

    const val CHANGE_PASSWORD_OLD_FIELD = "change_password_old_field"
    const val CHANGE_PASSWORD_NEW_FIELD = "change_password_new_field"
    const val CHANGE_PASSWORD_CONFIRM_FIELD = "change_password_confirm_field"
    const val CHANGE_PASSWORD_SUBMIT_BUTTON = "change_password_submit_button"

    const val ONBOARDING_WELCOME_START_BUTTON = "onboarding_welcome_start_button"

    const val ONBOARDING_PERSONAL_FULL_NAME_FIELD = "onboarding_personal_full_name_field"
    const val ONBOARDING_PERSONAL_PHONE_FIELD = "onboarding_personal_phone_field"
    const val ONBOARDING_PERSONAL_EMAIL_FIELD = "onboarding_personal_email_field"
    const val ONBOARDING_PERSONAL_PRIMARY_BUTTON = "onboarding_personal_primary_button"

    const val ONBOARDING_TRAINING_HOSPITAL_DROPDOWN = "onboarding_training_hospital_dropdown"
    const val ONBOARDING_TRAINING_CURRENT_LEVEL_FIELD = "onboarding_training_current_level_field"
    const val ONBOARDING_TRAINING_PRIMARY_BUTTON = "onboarding_training_primary_button"

    const val ONBOARDING_SUPERVISOR_SEARCH_FIELD = "onboarding_supervisor_search_field"
    const val ONBOARDING_SUPERVISOR_NOT_LISTED_TOGGLE = "onboarding_supervisor_not_listed_toggle"
    const val ONBOARDING_SUPERVISOR_MANUAL_NAME_FIELD = "onboarding_supervisor_manual_name_field"
    const val ONBOARDING_SUPERVISOR_SUBMIT_REQUEST_BUTTON = "onboarding_supervisor_submit_request_button"
    const val ONBOARDING_SUPERVISOR_PRIMARY_BUTTON = "onboarding_supervisor_primary_button"
    fun supervisorSelectButton(optionId: Int) = "supervisor_select_button_$optionId"

    const val ONBOARDING_DOCUMENTS_PRIMARY_BUTTON = "onboarding_documents_primary_button"
    fun documentUploadButton(documentId: Int) = "document_upload_button_$documentId"
    fun documentDeferButton(documentId: Int) = "document_defer_button_$documentId"

    const val ONBOARDING_REVIEW_SUBMIT_BUTTON = "onboarding_review_submit_button"

    const val PENDING_REVIEW_REFRESH_BUTTON = "pending_review_refresh_button"
    const val PENDING_REVIEW_SIGN_OUT_BUTTON = "pending_review_sign_out_button"
    const val CORRECTION_REQUIRED_REVIEW_NOTE = "correction_required_review_note"
    const val CORRECTION_REQUIRED_FIX_NOW_BUTTON = "correction_required_fix_now_button"
    const val CORRECTION_REQUIRED_SIGN_OUT_BUTTON = "correction_required_sign_out_button"

    const val HOME_TAB_HOME = "home_tab_home"
    const val HOME_TAB_TRAINING = "home_tab_training"
    const val HOME_TAB_DOCUMENTS = "home_tab_documents"
    const val HOME_TAB_PROFILE = "home_tab_profile"
    const val HOME_OUTSTANDING_BANNER = "home_outstanding_banner"
    const val HOME_UPLOAD_DOCUMENTS_BUTTON = "home_upload_documents_button"
    const val HOME_ALL_COMPLETE_BANNER = "home_all_complete_banner"

    const val PROFILE_SIGN_OUT_BUTTON = "profile_sign_out_button"
}
