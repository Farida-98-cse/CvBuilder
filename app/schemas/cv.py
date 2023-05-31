from typing import Any

from django.db import transaction
from ninja import ModelSchema

from app.models import CV


class PrimaryCvSchema(ModelSchema):
    class Config:
        model = CV
        model_fields = (
            "title",
            "professional_summary"
        )

    @transaction.atomic
    def create_cv(self, **kwargs: Any):
        _data = self.dict(exclude_none=True)
        _data.update(kwargs)
        return CV.objects.create(**_data)


class CvUpdateSchema(ModelSchema):
    class Config:
        model = CV
        model_fields = [
            "title",
            "professional_summary"
        ]
        optional = "__all__"

    @transaction.atomic
    def update_cv(self, **kwargs: Any):
        _data = self.dict(exclude_none=True)
        _data.update(kwargs)
        return CV.objects.update(**_data)


class CvRetrieveSchema(ModelSchema):
    class Config:
        model = CV
        model_fields = ["title", "professional_summary"]
