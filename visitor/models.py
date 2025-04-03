from django.db import models
from visitor_entry_exit.utils.base_model import BaseModel


class Visitor(BaseModel):
    CIVILIAN = "civilian"
    FOREIGNER = "foreigner"
    INTERNAL = "internal"
    GOV_AGENCY = "gov agency"

    VISITOR_TYPES = [
        (CIVILIAN, "Civilian"),
        (INTERNAL, "Internal"),
        (FOREIGNER, "Foreigner"),
        (GOV_AGENCY, "Gov Agency"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, unique=True)
    address = models.TextField()
    email = models.EmailField(blank=True, null=True)
    visitor_type = models.CharField(
        max_length=20, choices=VISITOR_TYPES, default=CIVILIAN
    )
    gov_id_type = models.CharField(max_length=50)
    gov_id_no = models.CharField(max_length=100)
    image = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"
