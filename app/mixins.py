from typing import Any

from django.db.models import QuerySet

from app.models import CV


class CvViewMixin:
    request: Any

    def get_queryset(self) -> QuerySet:
        return CV.objects.filter(owner_id=self.context.request.user)
