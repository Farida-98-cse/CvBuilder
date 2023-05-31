from typing import Any

from django.db.models import QuerySet

from app.models import CV, Education


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
    pass
