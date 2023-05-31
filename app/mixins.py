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


class ShowCvControllerMixin:
    def get_queryset(self, user_id) -> QuerySet:
        cv = CV.objects.select_related('user').prefetch_related('workexperience_set', 'education_set', 'skill_set').get(
            user=)

        cv_data = {
            'user': {
                'username': cv.user.username,
                'email': cv.user.email,
                # Include any other user fields you want to include
            },
            'title': cv.title,
            'professional_summary': cv.professional_summary,
            'work_experience': [
                {
                    'company_name': experience.company_name,
                    'job_title': experience.job_title,
                    'start_date': experience.start_date,
                    'end_date': experience.end_date,
                    'description': experience.description,
                }
                for experience in cv.workexperience_set.all()
            ],
            'education': [
                {
                    'institution_name': education.institution_name,
                    'degree': education.degree,
                    'start_date': education.start_date,
                    'end_date': education.end_date,
                    'description': education.description,
                }
                for education in cv.education_set.all()
            ],
            'skills': [
                skill.name for skill in cv.skill_set.all()
            ],
        }
        return cv_data
