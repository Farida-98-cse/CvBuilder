import pytest
from django.contrib.auth.models import User
from app.controllers import CvController
from app.models import CV
from app.tests.utils.test_utils import get_authentication_header
from ninja_extra import status, testing
from app.tests.utils.conftest import user


@pytest.mark.django_db
class TestCVView:
    def test_users_can_create_cv(self, user):
        headers = get_authentication_header(user)
        client = testing.TestClient(CvController)
        payload = dict(title="New cv", professional_experience="Some description")
        response = client.post(
            str(CvController.create_cv), json=payload, headers=headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert CV.objects.filter(
            name="New cv"
        ).first(), "Cv was not created"
