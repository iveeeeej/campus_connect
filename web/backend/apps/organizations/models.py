from django.db import models


class Organization(models.Model):
    class Code(models.TextChoices):
        USG = "USG", "University Student Government"
        SITE = "SITE", "Society of Information Technology Enthusiasts"
        PAFE = "PAFE", "PAFE"
        AFPROTECH = "AFPROTECH", "AFPROTECH"

    class Type(models.TextChoices):
        UNIVERSITY_WIDE = "UNIVERSITY_WIDE", "University-wide"
        COURSE_DEPARTMENT = "COURSE_DEPARTMENT", "Course/Department"

    code = models.CharField(max_length=20, choices=Code.choices, unique=True)
    name = models.CharField(max_length=150)
    organization_type = models.CharField(max_length=32, choices=Type.choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.code
