from django.http import JsonResponse
from ninja_extra import api_controller, route, status
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt.authentication import JWTAuth

from app.mixins import CvViewMixin, ShowCvControllerMixin
from app.schemas.cv import PrimaryCvSchema, CvRetrieveSchema, CvUpdateSchema, CvDraftSchema
from app.services.cv_service import build_cv_data
from app.utils.custom_exceptions import ObjectNotFoundException


@api_controller("/cv", tags=["cv"], auth=JWTAuth(), permissions=[IsAuthenticated])
class CvController(CvViewMixin, ShowCvControllerMixin):
    @route.post("/create", response=PrimaryCvSchema, url_name="Create CV")
    def create_cv(self, cv: PrimaryCvSchema):
            cv = cv.create_cv(user_id=self.context.request.user.id)
            return PrimaryCvSchema(title=cv.title, professional_summary=cv.professional_summary)

    @route.get("/{int:user_id}", response=CvRetrieveSchema, url_name="get-cv-detail")
    def retrieve_cv(self, user_id: int):
        cv = CvRetrieveSchema.get_cv(user_id)
        return cv

    @route.generic(
        "/{int:cv_id}",
        methods=["PUT"],
        response=CvRetrieveSchema,
        url_name="update",
    )
    def update_cv(self, cv_id: int, cv_schema: CvUpdateSchema):
        cv = self.get_object_or_exception(self.get_queryset(), id__exact=cv_id)
        cv_schema.update_cv(user_id=self.context.request.user.id)
        return cv_schema.dict()

    @route.delete(
        "/{int:cv_id}", url_name="destroy"
    )
    def delete_cv(self, cv_id: int):
        cv = self.get_object_or_exception(
            self.get_queryset(),
            id=cv_id,
            error_message="Cv with id {} does not exist".format(cv_id),
        )
        cv.delete()
        return self.create_response(
            "Item Deleted", status_code=status.HTTP_204_NO_CONTENT
        )

    @route.get("final-cv/{int:user_id}", response=CvDraftSchema, url_name="show-cv")
    def show_cv(self, user_id: int):
        cv = self.get_object_or_exception(
            self.get_cv_queryset(user_id=user_id))
        if not cv:
            raise ModelNotFoundException
        response = build_cv_data(cv)
        return response

