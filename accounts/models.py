from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import generate_school_id
from .managers import UserManager
import secrets
from .paystack import PayStack
import os
from dotenv import load_dotenv

load_dotenv()


# Overriding the Default Django Auth User and adding One More Field (user_type)
class User(AbstractUser):
    school_id = models.CharField(
        default=generate_school_id, max_length=100, editable=False, unique=True
    )
    user_type_data = ((1, "Administrator"), (2, "Staff"), (3, "Student"))
    user_type = models.PositiveIntegerField(default=1, choices=user_type_data)
    other_names = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    profile_pic = models.ImageField(blank=True, null=True)
    profile_pic_url = models.CharField(max_length=255, blank=True, null=True)
    gender_data = ((1, "Female"), (2, "Male"))
    gender = models.PositiveIntegerField(default=1, choices=gender_data)
    phone_number = models.CharField(blank=True, null=True, max_length=14)


class Administrator(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.school_id + " " + self.user.last_name + self.user.first_name


class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.school_id + " " + self.user.last_name + self.user.first_name


class Session(models.Model):
    id = models.AutoField(primary_key=True)
    session_start = models.PositiveIntegerField()
    session_end = models.PositiveIntegerField()
    current_session = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "{}/{}".format(self.session_start, self.session_end)


class Term(models.Model):
    term_data = ((1, "Term 1"), (2, "Term 2"), (3, "Term 3"))
    term = models.PositiveIntegerField(choices=term_data, default=1)
    current_term = models.BooleanField(default=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.term_data[self.term - 1][1])


class ClassLevel(models.Model):
    id = models.AutoField(primary_key=True)
    class_level_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.class_level_name


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, default=1)
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject_name + " " + self.class_level.class_level_name


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    class_level = models.ForeignKey(
        ClassLevel, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    is_old = models.BooleanField(default=False)
    previous_class = models.ForeignKey(
        ClassLevel,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="previous_class",
    )
    session_completed = models.CharField(max_length=200, blank=True, null=True)
    # gender = models.CharField(max_length=50)
    dob = models.DateField(null=True, blank=True)
    student_status_choices = ((1, "Ongoing"), (2, "Graduated"), (3, "Left"))
    student_status = models.PositiveIntegerField(
        choices=student_status_choices, default=1
    )
    term_enrolled = models.ForeignKey(
        Term, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    current_session = models.ForeignKey(
        Session, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            self.user.school_id + " " + self.user.last_name + " " + self.user.first_name
        )


term_choices = (
    ("Not Term-related", "Not Term-related"),
    ("Term 1", "Term 1"),
    ("Term 2", "Term 2"),
    ("Term 3", "Term 3"),
)
PAYSTACK_RECEIPT_EMAIL = os.environ.get("PAYSTACK_RECEIPT_EMAIL")


class Fee(models.Model):
    id = models.AutoField(primary_key=True)
    fee_name = models.CharField(max_length=255)
    fee_amount = models.PositiveIntegerField()
    course_id = models.ManyToManyField(ClassLevel)
    term = models.CharField(max_length=50, choices=term_choices)
    custom_id = models.CharField(max_length=10)
    fee_email = models.EmailField(max_length=255, default=PAYSTACK_RECEIPT_EMAIL)


class Payment(models.Model):
    fee_id = models.ForeignKey(Fee, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    ref = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    session = models.CharField(max_length=200)

    class Meta:
        ordering = ("-date_created",)

    def __str__(self) -> str:
        return f"Payment: {self.fee_id.fee_amount}"

    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(25)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self) -> int:
        return self.fee_id.fee_amount * 100

    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.fee_id.fee_amount)
        print("\n\n", status, "\n\n")
        if status:
            if result["amount"] / 100 == self.fee_id.fee_amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False


# class StudentResult(models.Model):
#     id=models.AutoField(primary_key=True)
#     student=models.ForeignKey(Student,on_delete=models.CASCADE)
#     subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
#     subject_exam_marks=models.FloatField(default=0)
#     subject_test_marks=models.FloatField(default=0)
#     #subject_test_two_marks=models.FloatField(default=0)
#     #subject_assignment_marks=models.FloatField(default=0)
#     created_at=models.DateField(auto_now_add=True)
#     updated_at=models.DateField(auto_now_add=True)


class StudentAssessment(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.DO_NOTHING, null=True, blank=True)
    session = models.ForeignKey(
        Session, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    # assessment_choices = (
    #     (1, 'assignment'),
    #     (2, 'test'),
    #     (3, 'examination'),
    #     (4, 'project'),
    # )
    assessment_choices = (
        ("assignment", "assignment"),
        ("test", "test"),
        ("examination", "examination"),
        ("project", "project"),
    )
    assessment_type = models.CharField(
        choices=assessment_choices, default=1, max_length=120
    )
    assessment_desc = models.CharField(max_length=125, null=True, blank=True)
    score = models.FloatField(default=0)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)


# Creating Django Signals

# It's like trigger in database. It will run only when Data is Added in User model


@receiver(post_save, sender=User)
# Now Creating a Function which will automatically insert data in Administrator, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            Administrator.objects.create(user=instance)
        if instance.user_type == 2:
            Staff.objects.create(user=instance)
        if instance.user_type == 3:
            Student.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.administrator.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.student.save()
