from functools import wraps
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


def is_logged_in(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        modulename = function.__module__
        user = request.user

        if user.is_authenticated:
            request.session.set_expiry(600)
            if user.user_type == 1:
                if modulename == "accounts.views_admin":
                    return function(request, *args, **kwargs)

                return redirect("/" + user.school_id + "/admin_home")

            if user.user_type == 2:
                if modulename == "accounts.views_staff":
                    return function(request, *args, **kwargs)

                return redirect("/" + user.school_id + "/staff_home")

            if user.user_type == 3:
                if modulename == "accounts.views_student":
                    return function(request, *args, **kwargs)

                return redirect("/" + user.school_id + "/student_home")

        return function(request, *args, **kwargs)

    return wrap
