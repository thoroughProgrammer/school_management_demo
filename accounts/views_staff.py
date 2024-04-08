import json
from multiprocessing import context
import re

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.decorators import login_required
from accounts.login_middleware import is_logged_in


from .models import (
    ClassLevel,
    User,
    Staff,
    Student,
    Session,
    Subject,
    StudentAssessment,
    Term,
)


@login_required(login_url="login_page")
@is_logged_in
def home(request, user_school_id):

    user = User.objects.get(school_id=request.user.school_id)

    # Fetching All Students under Staff

    subjects = Subject.objects.filter(staff=user)
    class_level_list = []
    for subject in subjects:
        class_level = ClassLevel.objects.get(id=subject.class_level.id)
        class_level_list.append(class_level)

    students_count = Student.objects.filter(class_level__in=class_level_list).count()
    subject_count = subjects.count()
    current_term = Term.objects.get(current_term=True)
    current_session = current_term.session

    chart_bg_color = [
        "#f56954",
        "#00a65a",
        "#f39c12",
        "#00c0ef",
        "#d2d6de",
        "#3c8dbc",
        "#ffe4e1",
        "#696969",
        "#8b0000",
        "#006400",
        "#000080",
        "#4b0082",
        "#ff4500",
        "#c71585",
        "#008080",
        "#bdb76b",
        "#800000",
        "#faebd7",
        "#2f4f4f",
        "#dc143c",
        "#008000",
        "#4169e1",
        "#800080",
        "#ff6347",
        "#ff1493",
        "#db7093",
        "#ff8c00",
        "#ff7f50",
        "#20b2aa",
        "#5f9ea0",
        "#00ced1",
        "#48d1cc",
        "#ffd700",
        "#ffdab9",
        "#f0e68c",
        "#fafad2",
        "#a52a2a",
        "#8b4513",
        "#d2691e",
        "#a0522d",
        "#b8860b",
        "#cd853f",
        "#bc8f8f",
        "#daa520",
        "#f4a460",
        "#d2b48c",
        "#fff8dc",
        "#000",
        "#ffebcd",
        "#fff",
        "#ffdead",
        "#ffa500",
        "#ffc0cb",
        "#ff69b4",
        "#e6e6fa",
        "#d8bfd8",
        "#dda0dd",
        "#ee82ee",
        "#9370db",
        "#ba55d3",
        "#6a5acd",
        "#ff00ff",
        "#7b68ee",
        "#9932cc",
        "#fffafa",
        "#a9a9a9",
        "#fffff0",
        "#708090",
        "#f0fff0",
        "#808080",
        "#f0ffff",
        "#dcdcdc",
        "#ffa07a",
        "#c0c0c0",
        "#cd5c5c",
        "#ff0000",
        "#e9967a",
        "#556b2f",
        "#228b22",
        "#2e8b57",
        "#808000",
        "#6b8e23",
        "#3cb371",
        "#b0e0e6",
        "#98fb98",
        "#4682b4",
        "#adff2f",
        "#4169e1",
        "#191970",
        "#9acd32",
        "#66cdaa",
        "#8fbc8f",
        "#6495ed",
    ]

    subject_students_dict = {}
    subject_assessments_label_dict = {}
    subject_bg_color_dict = {}
    subject_student_assessment_scores_dict = {}
    subject_assessment_type_desc_dict = {}

    assessment_count = 0
    for subject in subjects:

        student_list = []
        assessments_label_list = []
        student_assessments_list = []
        student_assessment_score_list = []
        assessment_type_list = []

        students = subject.class_level.student_set.all()
        if students.exists():
            assessments = StudentAssessment.objects.filter(
                term=current_term, student=students[0], subject=subject
            )

            for assessment_desc in assessments:
                assessments_label_list.append(assessment_desc.assessment_desc)
                assessment_type_list.append(assessment_desc.assessment_type)

            assessment_type_distinct = list()
            map(
                lambda x: not x in assessment_type_distinct
                and assessment_type_distinct.append(x),
                assessment_type_list,
            )

            assessment_type_dict = {}
            for assessment_type in assessment_type_distinct:
                assessment_type_desc_list = []
                for assessment in assessments:
                    if assessment.assessment_type == assessment_type:
                        assessment_type_desc_list.append(assessment.assessment_desc)

                    assessment_type_dict[assessment_type] = assessment_type_desc_list

            subject_assessment_type_desc_dict[
                (subject.id, subject.subject_name)
            ] = assessment_type_dict

            assessment_desc_no = len(assessments_label_list)
            color_set = chart_bg_color[0:assessment_desc_no]
            subject_bg_color_dict[subject.id] = color_set
            subject_assessments_label_dict[subject.id] = assessments_label_list

            for student in students:
                score_list = []
                student_list.append(student.user.school_id)
                student_assessments = StudentAssessment.objects.filter(
                    term=current_term, student=student, subject=subject
                )
                for score in student_assessments:
                    score_list.append(score.score)
                student_assessments_list.append(score_list)

            for i in list(zip(*student_assessments_list)):
                student_assessment_score_list.append(str(list(i)))

            subject_student_assessment_scores_dict[
                (subject.id, subject.subject_name)
            ] = student_assessment_score_list

            subject_students_dict[subject.id] = student_list

        assessment_count = assessment_count + assessments.count()

    context = {
        "user": user,
        "user_school_id": request.user.school_id,
        "user_first_name": request.user.first_name,
        "user_last_name": request.user.last_name,
        "user_other_names": request.user.other_names,
        "students_count": students_count,
        "subject_count": subject_count,
        "assessment_count": assessment_count,
        "subjects": subjects,
        "current_session": current_session,
        "current_term": current_term,
        "subject_students_dict": subject_students_dict,
        "subject_assessments_label_dict": subject_assessments_label_dict,
        "subject_bg_color_dict": subject_bg_color_dict,
        "subject_student_assement_scores_dict": subject_student_assessment_scores_dict,
    }

    return render(request, "staff_templates/home_template.html", context)


@login_required(login_url="login_page")
@is_logged_in
def profile(request, user_school_id):
    user = User.objects.get(school_id=request.user.school_id)
    staff = user.staff

    context = {
        "user": user,
        "user_school_id": request.user.school_id,
        "user_first_name": request.user.first_name,
        "user_last_name": request.user.last_name,
        "user_other_names": request.user.other_names,
        "staff": staff,
        "gender_data": user.gender_data,
    }
    return render(request, "staff_templates/staff_profile.html", context)


@login_required(login_url="login_page")
@is_logged_in
def edit_profile(request, user_school_id):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect("/" + request.user.school_id + "/staff_profile")

    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        other_names = request.POST.get("other_names")
        password = request.POST.get("password")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        phone_number = request.POST.get("phone_number")
        profile_pic = request.FILES.get("profile_pic")

        try:
            user = User.objects.get(school_id=request.user.school_id)
            user.first_name = first_name
            user.last_name = last_name
            user.other_names = other_names
            user.email = email
            user.gender = gender
            user.phone_number = phone_number

            if password != None and password != "":
                user.set_password(password)

            if profile_pic != None or profile_pic != "":
                user.profile_pic = profile_pic

            user.save()

            messages.success(request, "Profile Updated Successfully")

        except:
            messages.error(request, "Failed to Update Profile")

        finally:
            return redirect("/" + request.user.school_id + "/staff_profile")


@csrf_exempt
def get_students(request):
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year")

    subject = Subject.objects.get(id=subject_id)
    # session_model=Session.object.get(id=session_year)
    students = Student.objects.filter(course_id=subject.course_id)
    list_data = []

    for student in students:
        data_small = {
            "id": student.user.school_id,
            "name": student.user.first_name + " " + student.user.last_name,
        }
        list_data.append(data_small)
    return JsonResponse(
        json.dumps(list_data), content_type="application/json", safe=False
    )


@login_required(login_url="login_page")
@is_logged_in
def view_subjects(request, user_school_id):
    user = User.objects.get(school_id=request.user.school_id)
    subjects = user.subject_set.all()

    context = {
        "user_school_id": request.user.school_id,
        "user_first_name": request.user.first_name,
        "user_last_name": request.user.last_name,
        "user_other_names": request.user.other_names,
        # 'user_profile_pic': request.session.get('user_profile_pic'),
        "user": user,
        "subjects": subjects,
    }

    return render(request, "staff_templates/staff_subjects.html", context)


# def select_assessment_term(request, user_school_id, subject_id, assessment_action):
#     subject = Subject.objects.get(id=subject_id)
#     terms = Term.objects.all()
#     sessions = Session.objects.all()
#     if assessment_action == "staff_add_result":
#         staff_add_result = True
#         context = {
#         "user_school_id": request.user.school_id,
#         "user_first_name": request.user.first_name,
#         "user_last_name": request.user.last_name,
#         "user_other_names": request.user.other_names,
#         "subject": subject,
#         "terms": terms,
#         "sessions": sessions,
#         "staff_add_result": staff_add_result
#         }

#         return render(request, "staff_templates/select_assessment_term.html", context)

#     if assessment_action == "staff_final_assessment":
#         staff_add_result = False
#         context = {
#         "user_school_id": request.user.school_id,
#         "user_first_name": request.user.first_name,
#         "user_last_name": request.user.last_name,
#         "user_other_names": request.user.other_names,
#         "subject": subject,
#         "terms": terms,
#         "sessions": sessions,
#         "staff_add_result": staff_add_result
#         }
#         return render(request, "staff_templates/select_assessment_term.html", context)


@login_required(login_url="login_page")
@is_logged_in
def staff_add_result(request, user_school_id, subject_id):
    subject = Subject.objects.get(id=subject_id)
    sessions = Session.objects.all()
    current_session = Session.objects.get(current_session=True)
    current_term = current_session.term_set.get(current_term=True)

    context = {
        "user_school_id": request.user.school_id,
        "user_first_name": request.user.first_name,
        "user_last_name": request.user.last_name,
        "user_other_names": request.user.other_names,
        "subject": subject,
        "assessment_choices": StudentAssessment.assessment_choices,
        "sessions": sessions,
        "current_session": current_session,
        "current_term": current_term,
        "subject_term_id": str(subject.id) + "," + str(current_term.id),
    }

    return render(request, "staff_templates/staff_add_result.html", context)


@login_required(login_url="login_page")
@is_logged_in
def get_students_assessment(request, user_school_id):
    subject_id = request.GET.get("subjectId")
    session_id = (
        request.GET.get("sessionId")
        if request.GET.get("sessionId") != ""
        else Session.objects.get(current_session=True).id
    )
    current_session = Session.objects.get(current_session=True)
    subject = Subject.objects.get(id=subject_id)
    terms = Session.objects.get(id=session_id).term_set.all()
    current_term = Term.objects.get(current_term=True)

    if current_session.id == int(session_id):
        students = subject.class_level.student_set.all()
    else:
        students = Student.objects.filter(
            studentassessment__session=session_id, studentassessment__subject=subject
        ).distinct()

    data = {
        "terms": list(terms.values()),
        "students": [],
        "current_term_id": current_term.id,
    }

    for student in list(students.values()):
        student_user = User.objects.get(student__id=student["id"])
        student_data = {
            "school_id": student_user.school_id,
            "first_name": student_user.first_name,
            "last_name": student_user.last_name,
            "other_name": student_user.other_names,
            "assessments": {},
        }
        for term in terms:
            student_data["assessments"][term.id] = list(
                student_user.student.studentassessment_set.filter(
                    term=term, subject=subject
                ).values()
            )
        data["students"].append(student_data)

    return JsonResponse(
        data,
        content_type="application/json",
        safe=False,
    )


@login_required(login_url="login_page")
@is_logged_in
def save_student_result(request, user_school_id):
    if request.method != "POST":
        print("failed")
        return redirect("/" + request.user.school_id + "/subjects")

    data = json.loads(request.POST["data"])
    subject = Subject.objects.get(id=data.get("subject_id"))
    session = Session.objects.get(id=data.get("session_id"))
    term = Term.objects.get(id=data.get("term_id"))
    deleted_assessments = data.get("deleted_assessments")
    new_assessments = data.get("new_assessments")
    edited_assessments = data.get("edited_assessments")
    msg = []
    try:
        with transaction.atomic():

            # handle deleted assessments
            if deleted_assessments:
                # for assessment in deleted_assessments:
                #     assessment_obj_list = StudentAssessment.objects.filter(
                #         assessment_desc=assessment
                #     ).delete()
                for assessment in deleted_assessments:
                    assessment_obj_list = StudentAssessment.objects.filter(
                        session=session,
                        term=term,
                        subject=subject,
                        assessment_desc=assessment,
                    ).delete()
                msg.append("deleted")

            # handle new assessments
            if new_assessments:
                for assessment in new_assessments:
                    student = User.objects.get(
                        school_id=assessment.get("student_school_id")
                    ).student
                    assessment_type = assessment.get("assessment_type")
                    assessment_desc = assessment.get("assessment_desc")
                    score = float(assessment.get("assessment_score"))

                    StudentAssessment.objects.create(
                        student=student,
                        subject=subject,
                        term=term,
                        session=session,
                        assessment_type=assessment_type,
                        assessment_desc=assessment_desc,
                        score=score,
                    )
                msg.append("added")

            # handle edited assessments
            if edited_assessments:
                for assessment in edited_assessments:
                    assessment_obj = StudentAssessment.objects.get(
                        id=assessment.get("assessment_id")
                    )
                    assessment_obj.assessment_desc = assessment.get("assessment_desc")
                    assessment_obj.score = assessment.get("assessment_score")
                    assessment_obj.save()
                msg.append("edited")

        messages.success(
            request, "Assessments {} successfully".format(" and ".join(msg))
        )

    except Exception as e:
        print("error: ", e)
        messages.error(request, "Failed to add assessments")

    finally:
        return JsonResponse(
            json.dumps(
                {
                    "redirectUrl": "/"
                    + request.user.school_id
                    + "/"
                    + str(subject.id)
                    + "/staff_add_result"
                }
            ),
            content_type="application/json",
            safe=False,
        )


@login_required(login_url="login_page")
@is_logged_in
def final_assessment(request, user_school_id, subject_id):
    sessionId = request.GET.get("sessionId")
    subject = Subject.objects.get(id=subject_id)
    assessments = StudentAssessment.objects.filter(subject=subject_id)
    students = subject.class_level.student_set.all()
    assessments_student_zero = students[0].studentassessment_set.all()
    sessions = Session.objects.all()
    current_session = Session.objects.get(current_session=True)
    current_term = current_session.term_set.get(current_term=True)

    assessments_type_and_num = {}
    assessments_desc = {}

    for assessment in assessments_student_zero:

        if assessment.assessment_type in assessments_type_and_num:
            assessments_type_and_num[assessment.assessment_type] += 1
            assessments_desc[assessment.assessment_type] = assessments_desc[
                assessment.assessment_type
            ] + [assessment.assessment_desc]

        else:
            assessments_type_and_num[assessment.assessment_type] = 1
            assessments_desc[assessment.assessment_type] = [assessment.assessment_desc]

    context = {
        "user_school_id": request.user.school_id,
        "user_first_name": request.user.first_name,
        "user_last_name": request.user.last_name,
        "user_other_names": request.user.other_names,
        "subject": subject,
        "students": students,
        "assessments": assessments,
        "assessments_type_and_number": assessments_type_and_num,
        "assessments_desc": assessments_desc,
        "sessions": sessions,
        "current_session": current_session,
        "current_term": current_term,
    }

    return render(request, "staff_templates/final_assessment.html", context)


@login_required(login_url="login_page")
@is_logged_in
def get_final_assessment(request, user_school_id):
    subject_id = request.GET.get("subjectId")
    session_id = (
        request.GET.get("sessionId")
        if request.GET.get("sessionId") != ""
        else Session.objects.get(current_session=True).id
    )
    current_session = Session.objects.get(current_session=True)
    subject = Subject.objects.get(id=subject_id)
    terms = Session.objects.get(id=session_id).term_set.all()

    if current_session.id == int(session_id):
        students = subject.class_level.student_set.all()
    else:
        students = Student.objects.filter(
            studentassessment__session=session_id, studentassessment__subject=subject
        ).distinct()

    data = {
        "terms": list(terms.values()),
        "assessment_type_and_descs": {},
        "students": [],
    }

    for term in terms:
        data["assessment_type_and_descs"][term.id] = {}

    assessments = StudentAssessment.objects.filter(
        session=session_id, subject=subject_id
    )
    if assessments.exists():
        for assessment in assessments[0].student.studentassessment_set.filter(
            subject=subject_id
        ):
            try:
                data["assessment_type_and_descs"][assessment.term.id][
                    assessment.assessment_type
                ].append(assessment.assessment_desc)
            except KeyError:
                data["assessment_type_and_descs"][assessment.term.id][
                    assessment.assessment_type
                ] = [assessment.assessment_desc]

        for student in list(students.values()):
            student_user = User.objects.get(student__id=student["id"])
            student_data = {
                "school_id": student_user.school_id,
                "first_name": student_user.first_name,
                "last_name": student_user.last_name,
                "other_name": student_user.other_names,
                "assessments": {},
            }
            for term in terms:
                student_data["assessments"][term.id] = list(
                    student_user.student.studentassessment_set.filter(
                        term=term
                    ).values()
                )
            data["students"].append(student_data)

    return JsonResponse(
        data,
        content_type="application/json",
        safe=False,
    )
