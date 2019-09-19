import factory
from faker import Faker

from tasks.models import Task
from tests.factories_common import BaseModelFactory
from tests.factories_projects import ProjectFactory

fake = Faker()


class TaskFactory(BaseModelFactory):
    title = factory.Sequence(lambda n: 'task {}'.format(n))
    slug = factory.Sequence(lambda n: 'task-{}'.format(n))
    description = fake.text()
    project = factory.SubFactory(ProjectFactory)

    class Meta:
        model = Task