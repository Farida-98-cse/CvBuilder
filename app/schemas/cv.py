from ninja import ModelSchema

from app.models import CV


class PrimaryCvSchema(ModelSchema):
    class Config:
        model = CV
        model_fields = (
            "title",
            "professional_summary"
        )
