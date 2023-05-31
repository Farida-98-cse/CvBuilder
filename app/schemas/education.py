from typing import Any

from django.db import transaction
from ninja import ModelSchema

from app.models import Education


class EducationSchema(ModelSchema):
    class Config:
        model = Education
        model_fields = (
            "institution_name",
            "degree",
            "start_date",
            "end_date",
            "description"
        )

    @transaction.atomic
    def create_education(self, **kwargs: Any):
        _data = self.dict(exclude_none=True)
        _data.update(kwargs)
        return Education.objects.create(**_data)
