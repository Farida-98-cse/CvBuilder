from app.models import CV
from typing import Dict


def build_cv_data(cv: CV) -> Dict:
    cv_data = dict(user=dict(username=cv.user.username, email=cv.user.email),
                   title=cv.title, professional_summary=cv.professional_summary, work_experience=[
            dict(company_name=experience.company_name, job_title=experience.job_title,
                 start_date=str(experience.start_date),
                 end_date=str(experience.end_date), description=experience.description)
            for experience in cv.workexperience_set.all()
        ], education=[
            dict(institution_name=education.institution_name, degree=education.degree,
                 start_date=str(education.start_date),
                 end_date=str(education.end_date), description=education.description)
            for education in cv.education_set.all()
        ], skills=[
            skill.name for skill in cv.skill_set.all()
        ])
    return cv_data
