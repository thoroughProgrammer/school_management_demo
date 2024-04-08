from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .forms import EditResultForm
from .models import User,Student, Subject, StudentAssessment


class EditResultViewClass(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(school_id=kwargs.get('user_school_id'))

        # data used in every view
        request.session['user_school_id'] = user.school_id
        request.session['user_first_name'] = user.first_name
        request.session['user_last_name'] = user.last_name
        request.session['user_other_names'] = user.other_names

        edit_result_form=EditResultForm(staff=user)
        return render(request,"staff_templates/edit_student_result.html",{"form":edit_result_form,'user_school_id': request.session.get('user_school_id')})

    def post(self,request,*args,**kwargs):
        user = User.objects.get(school_id=kwargs.get('user_school_id'))

        # data used in every view
        request.session['user_school_id'] = user.school_id
        request.session['user_first_name'] = user.first_name
        request.session['user_last_name'] = user.last_name
        request.session['user_other_names'] = user.other_names

        form=EditResultForm(staff=user,data=request.POST)
        if form.is_valid():
            student_admin_id = form.cleaned_data['student_ids']
            test_one_marks = form.cleaned_data['test_one_marks']
            test_two_marks = form.cleaned_data['test_two_marks']
            exam_marks = form.cleaned_data['exam_marks']
            subject_id = form.cleaned_data['subject_id']

            student_obj = Student.objects.get(user=student_admin_id)
            subject_obj = Subject.objects.get(id=subject_id)
            result=StudentResult.objects.get(subject_id=subject_obj,student_id=student_obj)
            result.subject_test_one_marks=test_one_marks
            result.subject_test_two_marks=test_two_marks
            result.subject_exam_marks=exam_marks
            result.save()
            messages.success(request, "Successfully Updated Result")
            return HttpResponseRedirect(reverse("edit_student_result"))
        else:
            messages.error(request, "Failed to Update Result")
            form=EditResultForm(request.POST,staff=user)
            return render(request,"staff_templates/edit_student_result.html",{"form":form,'user_school_id': request.session.get('user_school_id')})
