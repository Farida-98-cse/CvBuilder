from django.http import JsonResponse
from ninja_extra import api_controller, route, status
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt.authentication import JWTAuth

from app.mixins import SkillViewMixin
from app.schemas.cv import CvRetrieveSchema
from app.schemas.skill import SkillSchema
from app.utils.custom_exceptions import ObjectNotFoundException


@api_controller("/skills", tags=["skill"], auth=JWTAuth(), permissions=[IsAuthenticated])
class SkillController(SkillViewMixin):

    @route.post("/create-skill", url_name="Define skills")
    def create_skill(self, skill: SkillSchema):
        cv = CvRetrieveSchema.get_cv(user_id=self.context.request.user.id)
        if not cv:
            raise ObjectNotFoundException
        skill = skill.create_skill(cv_id=cv.id)
        return SkillSchema(name=skill.name)

    @route.delete(
        "/{int:skill_id}", url_name="destroy"
    )
    def delete_education(self, skill_id: int):
        skill = self.get_object_or_exception(
            self.get_queryset(skill_id=skill_id),
            error_message="Education with id {} does not exist".format(skill_id),
        )
        skill.delete()
        return self.create_response(
            "Item Deleted", status_code=status.HTTP_204_NO_CONTENT
        )
