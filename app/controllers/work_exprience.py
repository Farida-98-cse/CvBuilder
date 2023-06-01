from ninja_extra import api_controller, route, status
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt.authentication import JWTAuth

from app.mixins import WorkViewMixin
from app.schemas.cv import CvRetrieveSchema
from app.schemas.work_experience import WorkSchema, WorkRetrieveSchema, WorkUpdateSchema
from app.utils.custom_exceptions import ObjectNotFoundException


@api_controller("/work-experience", tags=["experience"], auth=JWTAuth(), permissions=[IsAuthenticated])
class WorkController(WorkViewMixin):

    @route.post("/create-work-experience", url_name="Define work experiences", response=WorkSchema)
    def create_work(self, work: WorkSchema):
        cv = CvRetrieveSchema.get_cv(user_id=self.context.request.user.id)
        if not cv:
            raise ObjectNotFoundException
        work = work.create_work_experience(cv_id=cv.id)
        return WorkSchema(company_name=work.company_name, job_title=work.job_title, start_date=work.start_date,
                          end_date=work.end_date, description=work.description, id=work.id)

    @route.generic(
        "/{int:work_id}",
        methods=["PUT"],
        response=WorkRetrieveSchema,
        url_name="update",
    )
    def update_work_experience(self, work_id: int, work_schema: WorkUpdateSchema):
        work = self.get_object_or_exception(self.get_queryset(work_id=work_id), id__exact=work_id)
        if not work:
            raise ObjectNotFoundException
        work_schema.update_work_experience(id=work_id)
        return work_schema.dict()

    @route.delete(
        "/{int:work_id}", url_name="destroy"
    )
    def delete_work(self, work_id: int):
        work = self.get_object_or_exception(
            self.get_queryset(work_id=work_id),
            error_message="work experience with id {} does not exist".format(work_id),
        )
        work.delete()
        return self.create_response(
            "Item Deleted", status_code=status.HTTP_204_NO_CONTENT
        )
