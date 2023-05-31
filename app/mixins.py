from typing import Any

from django.db.models import QuerySet

from app.models import CV, Education, Skill, WorkExperience


class CvViewMixin:
    request: Any

    def get_queryset(self) -> QuerySet:
        return CV.objects.filter(user_id=self.context.request.user.id)


class EducationViewMixin:
    request: Any

    # def get_education(self):
    #     return Education.objects.filter(cv_id=self.context.request.cv_id).first()
    def get_queryset(self, education_id) -> QuerySet:
        return Education.objects.filter(id=education_id)


class SkillViewMixin:
    request: Any

    def get_queryset(self, skill_id) -> QuerySet:
        return Skill.objects.filter(id=skill_id)


class WorkViewMixin:
    request: Any

    def get_queryset(self, work_id) -> QuerySet:
        return WorkExperience.objects.filter(id=work_id)
