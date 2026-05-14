# Generated for Campus Connect Phase 1.

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Organization",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "code",
                    models.CharField(
                        choices=[
                            ("USG", "University Student Government"),
                            ("SITE", "Society of Information Technology Enthusiasts"),
                            ("PAFE", "PAFE"),
                            ("AFPROTECH", "AFPROTECH"),
                        ],
                        max_length=20,
                        unique=True,
                    ),
                ),
                ("name", models.CharField(max_length=150)),
                (
                    "organization_type",
                    models.CharField(
                        choices=[
                            ("UNIVERSITY_WIDE", "University-wide"),
                            ("COURSE_DEPARTMENT", "Course/Department"),
                        ],
                        max_length=32,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["code"],
            },
        ),
    ]
