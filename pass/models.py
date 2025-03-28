from django.db import models
from django.utils import timezone

from visitor.models import Visitor
from visitor_entry_exit.utils.base_model import BaseModel


class Pass(BaseModel):
    DAILY = "daily"
    LIMITED = "limited"
    NA = "NA"

    PASS_TYPE_CHOICES = [
        (DAILY, "Daily"),
        (LIMITED, "Limited"),
        (NA, "Not Applicable"),
    ]
    visitor = models.ForeignKey(
        Visitor, related_name="passes", on_delete=models.CASCADE
    )
    pass_type = models.CharField(max_length=7, choices=PASS_TYPE_CHOICES, default="NA")
    validity = models.DateTimeField(null=True, blank=True)
    pass_image = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.validity:
            today = timezone.localdate()
            self.validity = timezone.make_aware(
                timezone.datetime.combine(today, timezone.datetime.min.time())
            ) + timezone.timedelta(hours=18)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pass {self.visitor} {self.pass_type}"

    @property
    def is_active(self):
        return self.validity > timezone.now()
