from re import sub
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from accounts.login_middleware import is_logged_in

from accounts.models import (
    User,
    Administrator,
    Staff,
    Student,
    Session,
    ClassLevel,
    Subject,
    Fee,
    Payment,
    StudentAssessment,
)
from accounts.forms import AddStudentForm, EditStudentForm
from http.client import HTTPResponse

# for payment pdf generation
from django.template.loader import get_template, render_to_string
from weasyprint import HTML, CSS
import tempfile
import requests

# import asyncio
# from pyppeteer import launch


@login_required(login_url="login_page")
@is_logged_in
def home(request, user_school_id):
    user = User.objects.get(school_id=request.user.school_id)
    student = user.student
    if request.user.profile_pic_url:
        profile_pic_status_code = requests.get(request.user.profile_pic_url).status_code
        
        if requests.get(request.user.profile_pic_url).status_code == 200:
            profile_pic = request.user.profile_pic_url
        else:
            profile_pic = None

    subjects = student.class_level.subject_set.all()
    course = ClassLevel.objects.get(id=student.class_level.id)
    fee_term_one = Fee.objects.filter(course_id=course, term="Term 1")
    fee_term_two = Fee.objects.filter(course_id=course, term="Term 2")
    fee_term_three = Fee.objects.filter(course_id=course, term="Term 3")
    fee_others = Fee.objects.filter(course_id=course, term="Not Term-related")

    context = {
        "user_school_id": request.user.school_id,
        "user_first_name": request.user.first_name,
        "user_last_name": request.user.last_name,
        "user_other_names": request.user.other_names,
        "user_profile_pic_url": profile_pic,
        "subjects": subjects,
        "fee_term_one": fee_term_one,
        "fee_term_two": fee_term_two,
        "fee_term_three": fee_term_three,
        "fee_others": fee_others,
    }

    return render(request, "student_templates/home_template.html", context)


@login_required(login_url="login_page")
@is_logged_in
def profile(request, user_school_id):
    user = User.objects.get(school_id=request.user.school_id)
    student = user.student

    subjects = student.class_level.subject_set.all()
    course = ClassLevel.objects.get(id=student.class_level.id)
    fee_term_one = Fee.objects.filter(course_id=course, term="Term 1")
    fee_term_two = Fee.objects.filter(course_id=course, term="Term 2")
    fee_term_three = Fee.objects.filter(course_id=course, term="Term 3")
    fee_others = Fee.objects.filter(course_id=course, term="Not Term-related")

    context = {
        "user": user,
        "user_school_id": request.user.school_id,
        "user_first_name": request.user.first_name,
        "user_last_name": request.user.last_name,
        "user_other_names": request.user.other_names,
        "user_profile_pic_url": request.user.profile_pic_url,
        "student": student,
        "gender_data": user.gender_data,
        "fee_term_one": fee_term_one,
        "fee_term_two": fee_term_two,
        "fee_term_three": fee_term_three,
        "fee_others": fee_others,
    }
    return render(request, "student_templates/student_profile.html", context)


@login_required(login_url="login_page")
@is_logged_in
def edit_profile(request, user_school_id):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect("/" + request.user.school_id + "/student_profile")

    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        other_names = request.POST.get("other_names")
        password = request.POST.get("password")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")

        try:
            user = User.objects.get(school_id=request.user.school_id)
            user.first_name = first_name
            user.last_name = last_name
            user.other_names = other_names
            user.email = email
            user.gender = gender
            user.phone_number = phone_number
            user.student.address = address

            if password != None and password != "":
                user.set_password(password)
            user.save()

            messages.success(request, "Profile Updated Successfully")

        except:
            messages.error(request, "Failed to Update Profile")

        finally:
            return redirect("/" + request.user.school_id + "/student_profile")


@login_required(login_url="login_page")
@is_logged_in
def initiate_payment(request, user_school_id, fee_id):
    fee = Fee.objects.get(id=fee_id)
    user = User.objects.get(school_id=request.user.school_id)
    payment_model = Payment(fee_id=fee, student=user.student)
    current_session = Session.objects.get(current_session=True)
    payment_model.session = str(current_session).split(" ")[0]
    payment_model.save()
    student = user.student

    subjects = student.class_level.subject_set.all()
    course = ClassLevel.objects.get(id=student.class_level.id)
    fee_term_one = Fee.objects.filter(course_id=course, term="Term 1")
    fee_term_two = Fee.objects.filter(course_id=course, term="Term 2")
    fee_term_three = Fee.objects.filter(course_id=course, term="Term 3")
    fee_others = Fee.objects.filter(course_id=course, term="Not Term-related")

    context = {
        "user_first_name": request.user.first_name,
        "user_last_name": request.user.last_name,
        "user_other_names": request.user.other_names,
        "user_school_id": request.user.school_id,
        "user_profile_pic_url": request.user.profilic_pic_url,
        "fee": fee,
        "payment": payment_model,
        "paystack_public_key": settings.PAYSTACK_PUBLIC_KEY,
        "fee_term_one": fee_term_one,
        "fee_term_two": fee_term_two,
        "fee_term_three": fee_term_three,
        "fee_others": fee_others,
    }
    return render(request, "student_templates/make_payment.html", context)


@login_required(login_url="login_page")
@is_logged_in
def verify_payment(request: HttpRequest, ref: str) -> HTTPResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(
            request, "{} payment Successful".format(payment.fee_id.fee_name.title())
        )
        all_payments = Payment.objects.filter(verified=False)
        all_payments.delete()

    user_school_id = request.user.school_id
    return redirect("/" + request.user.school_id + "/payment_history")


@login_required(login_url="login_page")
@is_logged_in
def payment_history(request, user_school_id):
    user = User.objects.get(school_id=request.user.school_id)
    student = user.student
    course = ClassLevel.objects.get(id=student.class_level.id)
    payment_all = Payment.objects.filter(student=student, verified=True)
    fee_term_one = Fee.objects.filter(course_id=course, term="Term 1")
    fee_term_two = Fee.objects.filter(course_id=course, term="Term 2")
    fee_term_three = Fee.objects.filter(course_id=course, term="Term 3")
    fee_others = Fee.objects.filter(course_id=course, term="Not Term-related")

    context = {
        "user_first_name": request.user.first_name,
        "user_last_name": request.user.last_name,
        "user_other_names": request.user.other_names,
        "user_school_id": request.user.school_id,
        "user_profile_pic_url": request.user.profilic_pic_url,
        "payment_all": payment_all,
        "course": course,
        "fee_term_one": fee_term_one,
        "fee_term_two": fee_term_two,
        "fee_term_three": fee_term_three,
        "fee_others": fee_others,
    }
    return render(request, "student_templates/payment_history.html", context)


@login_required(login_url="login_page")
@is_logged_in
def payment_pdf(request, *args, **kwargs):
    ref = kwargs.get("ref")
    payment = get_object_or_404(Payment, ref=ref)
    template_path = "student_templates/payment_pdf.html"
    context = {"payment": payment}

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="payment.pdf"'
    response["Content-Transfer-Encoding"] = "binary"

    html_string = render_to_string(template_path, context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())

    result = html.write_pdf(
        stylesheets=[CSS((settings.STATIC_FILES + "/payment/pdf.css"))],
        presentational_hints=True,
    )

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output = open(output.name, "rb")
        response.write(output.read())

    return response

    # template = get_template(template_path)
    # html = template.render(context)


@login_required(login_url="login_page")
@is_logged_in
def student_view_result(request, user_school_id, session_id):
    user = User.objects.get(school_id=request.user.school_id)
    session = Session.objects.get(id=session_id)
    terms = session.term_set.all()
    assessments = StudentAssessment.objects.filter(
        student=user.student, session=session
    )
    subjects = Subject.objects.filter(
        studentassessment__student=user.student, studentassessment__session=session
    ).distinct()
    context = {
        "user": user,
        "user_school_id": request.user.school_id,
        "terms": terms,
        "subjects": subjects,
        "assessments": assessments,
    }
    return render(request, "student_templates/student_result.html", context)


@login_required(login_url="login_page")
@is_logged_in
def payment_status(request, payment_ref):
    return HttpResponse("successfully, payment reference: " + payment_ref)


@login_required(login_url="login_page")
@is_logged_in
def grade_card(request, user_school_id):
    user = User.objects.get(school_id=request.user.school_id)
    assessments = StudentAssessment.objects.filter(student=user.student)
    temp_session_list = []

    def unique(x):
        if x.session not in temp_session_list:
            temp_session_list.append(x.session)
            return x

    filtered_assessments = filter(unique, assessments)

    context = {
        "user_school_id": user.school_id,
        "filtered_assessments": filtered_assessments,
    }

    return render(request, "student_templates/grade_card.html", context)
