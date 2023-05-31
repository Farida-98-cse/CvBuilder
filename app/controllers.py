from datetime import datetime
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from ninja_extra import api_controller, route, status
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt import schema
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import TokenObtainSlidingController
from ninja_jwt.tokens import SlidingToken

from app.crud.cv import cv_crud
from app.mixins import CvViewMixin
from app.schemas.cv import PrimaryCvSchema
from app.schemas.user import *

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
    # TODO Add refresh token
    # @route.post(
    #     "/api-token-refresh",
    #     response=schema.TokenRefreshSlidingSerializer,
    #     url_name="refresh",
    # )
    # def refresh_token(self, refresh_token: schema.TokenRefreshSlidingSchema):
    #     refresh = schema.TokenRefreshSlidingSerializer(**refresh_token.dict())
    #     return refresh


# Cv controllers

@api_controller("/cv", tags=["cv"], auth=JWTAuth(), permissions=[IsAuthenticated])
class CvControllers(CvViewMixin):
    @route.post("/create", response=PrimaryCvSchema, url_name="Create CV")
    def create_cv(self, cv: PrimaryCvSchema):
        try:
            data = cv.dict()
            cv = cv_crud.create(data)
            return JsonResponse({
                'your cv': data
            })
        except Exception as ex:
            raise ex