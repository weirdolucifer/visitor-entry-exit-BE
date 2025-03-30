from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from account.models import Employee, Department
from visitor.models import Visitor
from visitor_entry_exit.utils.base_model import BaseModel


class Pass(BaseModel):
    VISITOR = 'visitor'
    EMP_WORK_PASS = 'emp_work_pass'
    EMP_DAILY_PASS = 'emp_daily_pass'
    EMP_TEMP_VEH_PASS = 'emp_temp_veh_pass'
    FOREIGNER_VISITOR = 'foreigner_visitor'
    WORK_PASS = 'work_pass'
    NA = "na"

    PASS_TYPE_CHOICES = [
        (VISITOR, "Visitor"),
        (EMP_WORK_PASS, "Work Pass (Employee)"),
        (EMP_DAILY_PASS, "Daily Pass (Employee)"),
        (EMP_TEMP_VEH_PASS, "Temporary Vehicle Pass (Employee)"),
        (FOREIGNER_VISITOR, "Visitor (Foreigner)"),
        (WORK_PASS, "Work Pass"),
        (NA, "Not Applicable"),
    ]
    visitor = models.ForeignKey(
        Visitor, related_name="passes", on_delete=models.CASCADE, null=True, blank=True
    )
    employee = models.ForeignKey(
        Employee, related_name="passes", on_delete=models.CASCADE, null=True, blank=True
    )
    pass_type = models.CharField(max_length=20, choices=PASS_TYPE_CHOICES, default=NA)
    validity = models.DateTimeField(null=True, blank=True)
    pass_image = models.TextField(blank=True, null=True)
    local_pass_id = models.CharField(max_length=100, null=True, blank=True)

    def clean(self):
        if not self.visitor and not self.employee:
            raise ValidationError("Either visitor or employee must be provided.")

        if self.visitor and self.employee:
            raise ValidationError("Only one of visitor or employee should be provided, not both.")

        if self.employee and self.pass_type not in [self.EMP_WORK_PASS, self.EMP_DAILY_PASS, self.EMP_TEMP_VEH_PASS]:
            raise ValidationError("Only employee-related pass types are allowed for employees.")

        if self.visitor and self.pass_type in [self.EMP_WORK_PASS, self.EMP_DAILY_PASS, self.EMP_TEMP_VEH_PASS]:
            raise ValidationError("Visitor cannot have employee-related pass types.")

        existing_pass = Pass.objects.filter(
            validity=self.validity,
            pass_type=self.pass_type,
        )
        if self.employee:
            existing_pass = existing_pass.filter(employee=self.employee)
        elif self.visitor:
            existing_pass = existing_pass.filter(visitor=self.visitor)

        if existing_pass.exists():
            raise ValidationError("A pass with the same type, user, and validity already exists.")

    def save(self, *args, **kwargs):
        self.clean()
        if not self.validity:
            today = timezone.localdate()

            if self.pass_type in [self.EMP_WORK_PASS, self.EMP_TEMP_VEH_PASS]:
                self.validity = timezone.make_aware(
                    timezone.datetime.combine(today, timezone.datetime.min.time())
                ) + timezone.timedelta(days=30, hours=18)
            else:
                self.validity = timezone.make_aware(
                    timezone.datetime.combine(today, timezone.datetime.min.time())
                ) + timezone.timedelta(hours=18)

        if not self.local_pass_id:
            self.local_pass_id = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pass {self.visitor or self.employee} {self.pass_type}"

    @property
    def is_active(self):
        return self.validity > timezone.now()


class VisitLog(BaseModel):
    pass_id = models.ForeignKey(Pass, on_delete=models.CASCADE, related_name="visit_logs")
    whom_to_visit = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name="visit_to_employees",
                                      null=True, blank=True)
    visiting_department = models.ForeignKey(Department, on_delete=models.DO_NOTHING,
                                            related_name="visit_to_departments", null=True, blank=True)
    escorted_by = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name="escorted_visits", null=True,
                                    blank=True)
    purpose_of_visit = models.TextField()
    in_datetime = models.DateTimeField()
    submitted_devices = models.TextField(blank=True, null=True)
    token_no = models.CharField(max_length=50, blank=True, null=True)
    carried_devices = models.TextField(blank=True, null=True)
    vehicle_details = models.TextField(blank=True, null=True)
    out_datetime = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.pass_id.employee:
            if self.whom_to_visit or self.visiting_department:
                pass
        else:
            if not self.whom_to_visit and not self.visiting_department:
                raise ValidationError("Either 'whom_to_visit' or 'visiting_department' must be provided for visitors.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Visit Log {self.pass_id} for {self.whom_to_visit or self.visiting_department}"
