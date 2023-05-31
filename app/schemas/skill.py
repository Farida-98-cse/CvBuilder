from typing import Any

from django.db import transaction
from ninja import ModelSchema

from app.models import Skill


class SkillSchema(ModelSchema):
    class Config:
        model = Skill
        model_fields = ("name", "id")

    @transaction.atomic
    def create_skill(self, **kwargs: Any):
        _data = self.dict(exclude_none=True)
        _data.update(kwargs)
        return Skill.objects.create(**_data)


class SkillUpdateSchema(ModelSchema):
    class Config:
        model = Skill
        model_fields = (
            "name",
            "id"
        )

    @transaction.atomic
    def update_education(self, **kwargs: Any):
        _data = self.dict(exclude_none=True)
        _data.update(kwargs)
        return Skill.objects.update(**_data)


class SkillRetrieveSchema(ModelSchema):
    class Config:
        model = Skill
        model_fields = (
            "name"
        )
