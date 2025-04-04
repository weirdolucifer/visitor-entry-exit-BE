# Generated by Django 5.1.7 on 2025-03-30 15:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_department_active"),
        ("pass", "0001_initial"),
        ("visitor", "0003_alter_visitor_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="pass",
            name="employee",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="passes",
                to="account.employee",
            ),
        ),
        migrations.AddField(
            model_name="pass",
            name="local_pass_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="pass",
            name="pass_type",
            field=models.CharField(
                choices=[
                    ("visitor", "Visitor"),
                    ("emp_work_pass", "Work Pass (Employee)"),
                    ("emp_daily_pass", "Daily Pass (Employee)"),
                    ("emp_temp_veh_pass", "Temporary Vehicle Pass (Employee)"),
                    ("foreigner_visitor", "Visitor (Foreigner)"),
                    ("work_pass", "Work Pass"),
                    ("na", "Not Applicable"),
                ],
                default="na",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="pass",
            name="visitor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="passes",
                to="visitor.visitor",
            ),
        ),
        migrations.CreateModel(
            name="VisitLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("purpose_of_visit", models.TextField()),
                ("in_datetime", models.DateTimeField()),
                ("submitted_devices", models.TextField(blank=True, null=True)),
                ("token_no", models.CharField(blank=True, max_length=50, null=True)),
                ("carried_devices", models.TextField(blank=True, null=True)),
                ("vehicle_details", models.TextField(blank=True, null=True)),
                ("out_datetime", models.DateTimeField(blank=True, null=True)),
                (
                    "escorted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="escorted_visits",
                        to="account.employee",
                    ),
                ),
                (
                    "pass_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="visit_logs",
                        to="pass.pass",
                    ),
                ),
                (
                    "visiting_department",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="visit_to_departments",
                        to="account.department",
                    ),
                ),
                (
                    "whom_to_visit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="visit_to_employees",
                        to="account.employee",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
