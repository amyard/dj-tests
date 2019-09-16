import uuid
import factory
from faker import Faker

from django.conf import settings
from .factories_common import BaseModelFactory


User = settings.AUTH_USER_MODEL
TEST_USER_PASSWORD = uuid.uuid4().hex
fake = Faker()


class UserFactory(BaseModelFactory):
    username = factory.Sequence(lambda n: 'username_{}'.format(n))
    email = factory.Sequence(lambda n: 'email{}gmail.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', TEST_USER_PASSWORD)

    class Meta:
        model = User