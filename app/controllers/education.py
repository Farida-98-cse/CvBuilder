from ninja_extra import api_controller, route, status
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt.authentication import JWTAuth

from app.mixins import EducationViewMixin
from app.schemas.cv import CvRetrieveSchema
from app.schemas.education import EducationSchema, EducationRetrieveSchema, EducationUpdateSchema


@api_controller("/education", tags=["education"], auth=JWTAuth(), permissions=[IsAuthenticated])
class EducationController(EducationViewMixin):
    @route.post("/create-education", response=EducationSchema, url_name="Define Education history")
    def create_education_program(self, education: EducationSchema):
        cv = CvRetrieveSchema.get_cv(user_id=self.context.request.user.id)
        education = education.create_education(cv_id=cv.id)
        return EducationSchema(institution_name=education.institution_name, degree=education.degree,
                               start_date=education.start_date, end_date=education.end_date,
                               description=education.description)

    @route.generic(
        "/{int:education_id}",
        methods=["PUT"],
        response=EducationRetrieveSchema,
        url_name="update",
    )
    def update_cv(self, education_id: int, education_schema: EducationUpdateSchema):
        education = self.get_object_or_exception(self.get_queryset(education_id=education_id), id__exact=education_id)
        if not education:
            raise ModuleNotFoundError
        education_schema.update_education(id=education_id)
        return education_schema.dict()

    @route.delete(
        "/{int:education_id}", url_name="destroy"
    )
    def delete_education(self, education_id: int):
        education = self.get_object_or_exception(
            self.get_queryset(education_id=education_id),
            error_message="Education with id {} does not exist".format(education_id),
        )
        education.delete()
        return self.create_response(
            "Item Deleted", status_code=status.HTTP_204_NO_CONTENT
        )
