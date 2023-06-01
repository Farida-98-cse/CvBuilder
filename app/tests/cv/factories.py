import factory

from app.models import CV
from app.tests.users.factories import UserFactory


class CVFactory(factory.DjangoModelFactory):
    title = factory.Sequence(lambda n: "cv_title{0}".format(n))
    professional_experience = factory.Sequence(lambda n: "cv_professional_experience{0}".format(n))
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = CV
