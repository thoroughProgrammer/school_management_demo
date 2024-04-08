# from channels.auth import login, logout
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from accounts.school_id_backend import SchoolIdBackend
from accounts.login_middleware import is_logged_in


@is_logged_in
def login_page(request):
    return render(request, "login.html")


def do_login(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")

    user = SchoolIdBackend.authenticate(
        request,
        school_id=request.POST.get("school_id"),
        password=request.POST.get("password"),
    )

    print(user)

    if user != None:
        login(request, user, backend="accounts.school_id_backend.SchoolIdBackend")
        user_type = user.user_type

        if user_type == 1:
            request.session.set_expiry(600)
            return redirect("/" + user.school_id + "/admin_home")

        elif user_type == 2:
            request.session.set_expiry(600)
            return redirect("/" + user.school_id + "/staff_home")

        elif user_type == 3:
            request.session.set_expiry(600)
            return redirect("/" + user.school_id + "/student_home")

        else:
            messages.error(request, "Invalid Login!")
            return redirect("/")

    else:
        messages.error(request, "Invalid Login Credentials!")
        return redirect("/")


def get_user_details(request):
    if request.user != None:
        return HttpResponse(
            "User: " + request.user.email + " User Type: " + request.user.user_type
        )
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")
