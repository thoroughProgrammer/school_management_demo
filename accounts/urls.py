from django.urls import path

from . import views, views_admin, views_staff, views_student
from .edit_result_view_class import EditResultViewClass

urlpatterns = [
    path("", views.login_page, name="login_page"),
    path("doLogin", views.do_login, name="do_login"),
    path("logout_user/", views.logout_user, name="logout_user"),
    
    # ADMINISTRATOR
    path("<user_school_id>/admin_home", views_admin.home, name="admin_home"),
    path("<user_school_id>/profile", views_admin.profile, name="admin_profile"),
    path("<user_school_id>/add_staff", views_admin.add_staff, name="add_staff"),
    path("<user_school_id>/add_student", views_admin.add_student, name="add_student"),
    path("<user_school_id>/add_class", views_admin.add_class, name="add_class"),
    path("<user_school_id>/add_subject", views_admin.add_subject, name="add_subject"),
    path("<user_school_id>/add_session", views_admin.add_session, name="add_session"),
    path(
        "<user_school_id>/current_session",
        views_admin.select_session,
        name="select_session",
    ),
    path("<user_school_id>/add_fee", views_admin.add_fee, name="add_fee"),
    path(
        "<user_school_id>/add_staff_save",
        views_admin.add_staff_save,
        name="add_staff_save",
    ),
    path(
        "<user_school_id>/add_student_save",
        views_admin.add_student_save,
        name="add_student_save",
    ),
    path(
        "<user_school_id>/add_class_save",
        views_admin.add_class_save,
        name="add_class_save",
    ),
    path(
        "<user_school_id>/add_subject_save",
        views_admin.add_subject_save,
        name="add_subject_save",
    ),
    path(
        "<user_school_id>/add_session_save",
        views_admin.add_session_save,
        name="add_session_save",
    ),
    path(
        "<user_school_id>/select_session_save",
        views_admin.select_session_save,
        name="select_session_save",
    ),
    path(
        "<user_school_id>/add_fee_save", views_admin.add_fee_save, name="add_fee_save"
    ),
    path(
        "<user_school_id>/edit_admin/",
        views_admin.edit_admin_profile,
        name="edit_admin_profile",
    ),
    path(
        "<user_school_id>/edit_staff/<staff_school_id>",
        views_admin.edit_staff,
        name="edit_staff",
    ),
    path(
        "<user_school_id>/edit_student/<student_school_id>",
        views_admin.edit_student,
        name="edit_student",
    ),
    path(
        "<user_school_id>/edit_class/<class_level_id>",
        views_admin.edit_class,
        name="edit_class",
    ),
    path(
        "<user_school_id>/edit_subject/<subject_id>",
        views_admin.edit_subject,
        name="edit_subject",
    ),
    path(
        "<user_school_id>/edit_session/<session_id>",
        views_admin.edit_session,
        name="edit_session",
    ),
    path(
        "<user_school_id>/edit_fee/<str:fee_id>", views_admin.edit_fee, name="edit_fee"
    ),
    path(
        "<user_school_id>/edit_staff_save",
        views_admin.edit_staff_save,
        name="edit_staff_save",
    ),
    path(
        "<user_school_id>/edit_student_save",
        views_admin.edit_student_save,
        name="edit_student_save",
    ),
    path(
        "<user_school_id>/edit_class_save",
        views_admin.edit_class_save,
        name="edit_class_save",
    ),
    path(
        "<user_school_id>/edit_subject_save",
        views_admin.edit_subject_save,
        name="edit_subject_save",
    ),
    path(
        "<user_school_id>/edit_session_save",
        views_admin.edit_session_save,
        name="edit_session_save",
    ),
    path(
        "<user_school_id>/delete_staff/<staff_school_id>",
        views_admin.delete_staff,
        name="delete_staff",
    ),
    path(
        "<user_school_id>/delete_student/<student_school_id>",
        views_admin.delete_student,
        name="delete_student",
    ),
    path(
        "<user_school_id>/delete_class/<class_level_id>",
        views_admin.delete_class,
        name="delete_class",
    ),
    path(
        "<user_school_id>/delete_subject/<subject_id>",
        views_admin.delete_subject,
        name="delete_subject",
    ),
    path(
        "<user_school_id>/delete_session/<session_id>",
        views_admin.delete_session,
        name="delete_session",
    ),
    path(
        "<user_school_id>/delete_fee/<fee_id>",
        views_admin.delete_fee,
        name="delete_fee",
    ),
    path(
        "<user_school_id>/manage_staff", views_admin.manage_staff, name="manage_staff"
    ),
    path(
        "<user_school_id>/manage_student",
        views_admin.manage_student,
        name="manage_student",
    ),
    path(
        "<user_school_id>/manage_class", views_admin.manage_class, name="manage_class"
    ),
    path(
        "<user_school_id>/manage_subject",
        views_admin.manage_subject,
        name="manage_subject",
    ),
    path(
        "<user_school_id>/manage_session",
        views_admin.manage_session,
        name="manage_session",
    ),
    path("<user_school_id>/manage_fee", views_admin.manage_fee, name="manage_fee"),
    path(
        "<user_school_id>/manage_class/<class_level_name>/manage_students",
        views_admin.manage_class_students,
        name="manage_class_students",
    ),
    path(
        "<user_school_id>/manage_class/<class_level_name>/manage_subjects",
        views_admin.manage_class_subjects,
        name="manage_class_subjects",
    ),
    path(
        "<user_school_id>/manage_class/<class_level_name>/add_student",
        views_admin.manage_class_add_student,
        name="manage_class_add_student",
    ),
    path(
        "<user_school_id>/manage_class/<class_level_name>/add_subject",
        views_admin.manage_class_add_subject,
        name="manage_class_add_subject",
    ),
    path(
        "<user_school_id>/student_records/<course_id>/",
        views_admin.student_records,
        name="student_records",
    ),
    path(
        "student_records_doc/<course_id>/",
        views_admin.student_records_doc,
        name="student_records_doc",
    ),
    path(
        "<user_school_id>/payment_history/<student_school_id>",
        views_admin.view_fee_payments,
        name="view_fee_payments",
    ),
    path(
        "<user_school_id>/manage_class/<class_level_name>/change_class",
        views_admin.change_class_level,
        name="change_students_class",
    ),
    path(
        "<user_school_id>/manage_class/change_class_level",
        views_admin.change_class_level_save,
        name="change_students_class_save",
    ),
    path(
        "<user_school_id>/completed/manage_students",
        views_admin.manage_students_completed,
        name="manage_students_completed",
    ),
    path(
        "<user_school_id>/left/manage_students",
        views_admin.manage_students_left,
        name="manage_students_left",
    ),
    
    # STAFF
    path("<user_school_id>/staff_home", views_staff.home, name="staff_home"),
    path("<user_school_id>/staff_profile", views_staff.profile, name="staff_profile"),
    path(
        "<user_school_id>/edit_staff_profile",
        views_staff.edit_profile,
        name="edit_staff_profile",
    ),
    # path('<user_school_id>/<subject_id>/<assessment_action>/term?session?', views_staff.select_assessment_term, name="select_assessment_term"),
    path(
        "<user_school_id>/<subject_id>/staff_add_result",
        views_staff.staff_add_result,
        name="staff_add_result",
    ),
    path(
        "<user_school_id>/get_students_assessment",
        views_staff.get_students_assessment,
        name="get_students_assessment",
    ),
    path(
        "<user_school_id>/<subject_id>/staff_final_assessment",
        views_staff.final_assessment,
        name="staff_final_assessment",
    ),
    path(
        "<user_school_id>/get_final_assessment",
        views_staff.get_final_assessment,
        name="get_final_assessment",
    ),
    path(
        "<user_school_id>/save_student_result",
        views_staff.save_student_result,
        name="save_student_result",
    ),
    path("<user_school_id>/subjects", views_staff.view_subjects, name="staff_subjects"),


    # STUDENT
    path("<user_school_id>/student_home", views_student.home, name="student_home"),
    path(
        "<user_school_id>/student_profile",
        views_student.profile,
        name="student_profile",
    ),
    path(
        "<user_school_id>/edit_student_profile",
        views_student.edit_profile,
        name="edit_student_profile",
    ),
    path(
        "<user_school_id>/make_payment/<fee_id>",
        views_student.initiate_payment,
        name="initiate_payment",
    ),
    path("<str:ref>/", views_student.verify_payment, name="verify_payment"),
    path(
        "<user_school_id>/payment_history",
        views_student.payment_history,
        name="payment_history",
    ),
    path("payment_pdf/<str:ref>", views_student.payment_pdf, name="payment_pdf"),
    path("<user_school_id>/grade_card", views_student.grade_card, name="grade_card"),
    path(
        "<user_school_id>/<session_id>/results",
        views_student.student_view_result,
        name="student_view_result",
    ),
]
