import factory
from tests.factories_common import BaseModelFactory
from tests.factories_users import UserFactory

from tasks.models import Project


class ProjectFactory(BaseModelFactory):
    user = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: 'new title for project {}'.format(n))
    slug = factory.Sequence(lambda n: 'new-title-for-project-{}'.format(n))

    class Meta:
        model = Project