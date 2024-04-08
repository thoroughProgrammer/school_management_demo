from dataclasses import fields
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .models import User, Administrator, Staff, Student, Session, ClassLevel, Subject, Fee, Payment, StudentAssessment, Term

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ( 'school_id', 'email', 'username', 'password')}),
        ("Personal Info", {'fields': ('last_name', 'first_name', 'other_names', 'phone_number')}),
        ("Permissions", {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ("Important Dates", {'fields': ('last_login', 'date_joined')})
    )

    readonly_fields = ['school_id']

    add_fieldsets = (
        ('Auth Field', {"fields": ('first_name', 'last_name', 'other_names', 'email', 'username', 'password1', 'password2')}),
        ('Status Field', {"fields": ('user_type', 'is_active', 'is_staff')}),
        ('Others Field', {"fields": ('gender', 'phone_number')})
    )

    radio_fields = {"user_type": admin.HORIZONTAL, 'gender': admin.HORIZONTAL}

# admin.site.register(User, CustomUserAdmin)
admin.site.register(User)
admin.site.register(Administrator)
admin.site.register(Staff)
admin.site.register(Student)
admin.site.register(Session)
admin.site.register(ClassLevel)
admin.site.register(Subject)
admin.site.register(Fee)
admin.site.register(Payment)
admin.site.register(StudentAssessment)
admin.site.register(Term)

# admin.autodiscover()
# admin.site.enable_nav_sidebar = False
