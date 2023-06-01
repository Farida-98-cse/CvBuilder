import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from ninja_extra import status
from app.tests.utils.test_utils import get_authentication_header


@pytest.mark.django_db
class TestUserView:
    def test_create_new_user_weak_password_should_fail(self, random_email, random_username, client):
        url = reverse("store:user-create")
        payload = {
            "username": random_username,
            "email": random_email,
            "password": "password",
            "first_name": "test",
            "last_name": "test",
        }
        response = client.post(
            url, payload, format="json", content_type="application/json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["token"]

    def test_delete_user_success(self, app_admin, user, client):
        headers = get_authentication_header(app_admin, header_key="HTTP_AUTHORIZATION")

        url = reverse("store:user-delete", kwargs={"pk": user.id})
        response = client.delete(url, format="json", **headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        user = User.objects.filter(pk=user.pk).first()
        assert user is None
