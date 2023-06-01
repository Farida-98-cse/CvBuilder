from typing import Any

from django.db import transaction
from ninja_schema import ModelSchema

from app.models import WorkExperience


class WorkSchema(ModelSchema):
    class Config:
        model = WorkExperience
        include = ("company_name", "job_title", "start_date", "end_date", "description")

    @transaction.atomic
    def create_work_experience(self, **kwargs: Any):
        _data = self.dict(exclude_none=True)
        _data.update(kwargs)
        return WorkExperience.objects.create(**_data)


class WorkUpdateSchema(ModelSchema):
    class Config:
        model = WorkExperience
        include = ("company_name", "job_title", "start_date", "end_date", "description")

    @transaction.atomic
    def update_work_experience(self, **kwargs: Any):
        _data = self.dict(exclude_none=True)
        _data.update(kwargs)
        return WorkExperience.objects.update(**_data)


class WorkRetrieveSchema(ModelSchema):
    class Config:
        model = WorkExperience
        include = ("company_name", "job_title", "start_date", "end_date", "description")
