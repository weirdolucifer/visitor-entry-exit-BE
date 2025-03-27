from django.db import models
from visitor_entry_exit.utils.base_model import BaseModel


class Employee(BaseModel):
    employee_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    rank = models.CharField(max_length=100)
    extension = models.CharField(max_length=10)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}, {self.rank}"


class Department(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    extension = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"
