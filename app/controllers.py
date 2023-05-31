from django.http import JsonResponse

from ninja_extra import api_controller, route
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt import schema
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import TokenObtainSlidingController
from ninja_jwt.tokens import SlidingToken
from app.mixins import CvViewMixin, EducationViewMixin, SkillViewMixin, WorkViewMixin, ShowCvControllerMixin
from app.schemas.cv import PrimaryCvSchema, CvUpdateSchema, CvRetrieveSchema, get_cv
from app.schemas.education import EducationSchema, EducationRetrieveSchema, EducationUpdateSchema
from app.schemas.skill import SkillSchema
from app.schemas.user import *
from app.schemas.work_experience import WorkSchema, WorkRetrieveSchema, WorkUpdateSchema

User = get_user_model()


@api_controller("/auth", tags=["users"], auth=JWTAuth())
class UserController:
    @route.post(
        "/create", response={201: UserTokenOutSchema}, url_name="user-create", auth=None
    )
    def create_user(self, user_schema: CreateUserSchema):
        user = user_schema.create()
        token = SlidingToken.for_user(user)
        return UserTokenOutSchema(
            user=user,
            token=str(token),
            token_exp_date=datetime.utcfromtimestamp(token["exp"]),
        )


@api_controller("/auth", tags=["auth"], auth=JWTAuth())
class UserTokenController(TokenObtainSlidingController):
    auto_import = True

    @route.post("/login", response=UserTokenOutSchema, url_name="login", auth=None)
    def obtain_token(self, user_token: schema.TokenObtainSlidingSerializer):
        user = user_token._user
        token = SlidingToken.for_user(user)
        return UserTokenOutSchema(
            user=user,
            token=str(token),
            token_exp_date=datetime.utcfromtimestamp(token["exp"]),
        )

    @route.post(
        "/api-token-refresh",
        response=schema.TokenRefreshSlidingSerializer,
        url_name="refresh",
    )
    def refresh_token(self, refresh_token: schema.TokenRefreshSlidingSchema):
        refresh = schema.TokenRefreshSlidingSerializer(**refresh_token.dict())
        return refresh


# Cv controllers

@api_controller("/cv", tags=["cv"], auth=JWTAuth(), permissions=[IsAuthenticated])
class CvControllers(CvViewMixin):
    @route.post("/create", response=PrimaryCvSchema, url_name="Create CV")
    def create_cv(self, cv: PrimaryCvSchema):
        try:
            cv = cv.create_cv(user_id=self.context.request.user.id)
            return JsonResponse(
                {"bio": cv.professional_summary, "title": cv.title}
            )
        except Exception as ex:
            raise ex

    @route.get("/{int:cv_id}", response=CvRetrieveSchema, url_name="get-cv-detail")
    def retrieve_cv(self, cv_id: str):
        cv = CvRetrieveSchema.get_cv(cv_id)
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


@api_controller("/education", tags=["education"], auth=JWTAuth(), permissions=[IsAuthenticated])
class EducationController(EducationViewMixin):
    @route.post("/create-education", response=EducationSchema, url_name="Define Education history")
    def create_education_program(self, education: EducationSchema):
        try:
            cv = get_cv(user_id=self.context.request.user.id)
            education = education.create_education(cv_id=cv.id)
            return EducationSchema(institution_name=education.institution_name, degree=education.degree,
                                   start_date=education.start_date, end_date=education.end_date,
                                   description=education.description)
        except Exception as ex:
            raise ex

    @route.generic(
        "/{int:education_id}",
        methods=["PUT"],
        response=EducationRetrieveSchema,
        url_name="update",
    )
    def update_cv(self, education_id: int, education_schema: EducationUpdateSchema):
        education = self.get_object_or_exception(self.get_queryset(education_id=education_id), id__exact=education_id)
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


@api_controller("/skills", tags=["skill"], auth=JWTAuth(), permissions=[IsAuthenticated])
class SkillController(SkillViewMixin):

    @route.post("/create-skill", url_name="Define skills")
    def create_skill(self, skill: SkillSchema):
        try:
            cv = get_cv(user_id=self.context.request.user.id)
            skill = skill.create_skill(cv_id=cv.id)
            return JsonResponse({
                "name": skill.name
            })
        except Exception as ex:
            raise ex

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


@api_controller("/work-experience", tags=["experience"], auth=JWTAuth(), permissions=[IsAuthenticated])
class WorkController(WorkViewMixin):

    @route.post("/create-work-experience", url_name="Define work experiences", response=WorkSchema)
    def create_work(self, work: WorkSchema):
        try:
            cv = get_cv(user_id=self.context.request.user.id)
            work = work.create_work_experience(cv_id=cv.id)
            return WorkSchema(company_name=work.company_name, job_title=work.job_title, start_date=work.start_date,
                              end_date=work.end_date, description=work.description, id=work.id)
        except Exception as ex:
            raise ex

    @route.generic(
        "/{int:work_id}",
        methods=["PUT"],
        response=WorkRetrieveSchema,
        url_name="update",
    )
    def update_work_experience(self, work_id: int, work_schema: WorkUpdateSchema):
        work = self.get_object_or_exception(self.get_queryset(work_id=work_id), id__exact=work_id)
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


@api_controller("/show-cv", tags=["show-cv"], auth=JWTAuth(), permissions=[IsAuthenticated])
class ShowCvController(ShowCvControllerMixin):

    @route.get("/{int:user_id}", response=CvRetrieveSchema, url_name="show-cv")
    def show_cv(self, user_id: int):
        cv = self.get_object_or_exception(
            self.get_queryset(cv_id=user_id))
