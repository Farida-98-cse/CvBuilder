from app.models import (
    CV
)
from django.core.exceptions import ObjectDoesNotExist


class CvCRUD:
    @staticmethod
    def get(id: int):
        try:
            cv = CV.objects.get(id=id)
            return cv
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_multi():
        try:
            cvs = CV.objects.all()
            return cvs
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create(data):
        new_book = CV.objects.create(**data)


cv_crud = CvCRUD()
