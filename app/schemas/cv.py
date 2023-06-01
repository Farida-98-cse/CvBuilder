from datetime import datetime
from typing import Any

from django.db import transaction
from ninja import ModelSchema, Schema

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
    professional_summary: str = None

    class Config:
        model = CV
        model_fields = ["title", "professional_summary"]

    def get_cv(user_id: int):
        return CV.objects.filter(user_id=user_id).first()


class UserSchema:
    user_name: str
    email: str


class WorkExpSchema:
    company_name: str = None
    job_title: str = None
    start_date: datetime = None
    end_date: datetime = None
    description: str = None


class EducationOutSchema:
    institution_name: str = None
    degree: str = None
    start_date: datetime = None
    end_date: datetime = None
    description: str = None


class SkillOutSchema:
    name: str


class CvDraftSchema(Schema):
    user: UserSchema = None
    title: str = None
    professional_summary: str = None
    work_experience: WorkExpSchema = None
    education: EducationOutSchema = None
    skills: SkillOutSchema = None

    class Config:
        arbitrary_types_allowed = True
