from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from tests.factories_projects import ProjectFactory
from tests.factories_tasks import TaskFactory
from tests.factories_users import UserFactory

from tasks.models import Project, Task


User = get_user_model()


class TastTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create(username='user1', email='user1@gmail.com', password='zaza1234')
        cls.pr = Project.objects.create(title='project1', user = cls.user)
        cls.task = Task.objects.create(title='task1', project = cls.pr)

    def test_slug_model(self):
        self.assertEqual(self.task.slug, 'task1-user1')

    def test_tasks(self):
        self.assertEqual(self.pr.title, 'project1')

    def test_tasks_slug_unique(self):
        unique = self.task._meta.get_field('slug').unique
        self.assertEquals(unique, True)

    def test_task_title_max_length(self):
        max_length = self.task._meta.get_field('title').max_length
        self.assertEquals(max_length, 255)


class TaskListViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = UserFactory(is_active=True)
        cls.pr = ProjectFactory(user=cls.user)
        cls.task = TaskFactory()
        cls.url = reverse('tasks:task_list')

        cls.user2 = UserFactory()

    def test_get_objects_not_logged_users(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/en/users/login/?next=/en/task-list/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def user_task_for_logged_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        obj = Task.objects.filter(project__user=self.user)

        self.assertEqual(response.status_code, 200)
        assert 'base.html' in [t.name for t in response.templates]
        assert 'tasks/task_list.html' in [t.name for t in response.templates]
        self.assertEqual(obj.count(), 1)

    def test_taks_no_data(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.url)
        obj = Task.objects.filter(project__user=self.user2).exists()

        self.assertEqual(response.status_code, 200)
        assert 'base.html' in [t.name for t in response.templates]
        assert 'tasks/task_list.html' in [t.name for t in response.templates]
        self.assertContains(response, 'Sorry, no tasks yet.')
        self.assertFalse(obj)
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_check_amount_of_tasks(self):
        pr1 = ProjectFactory(user=self.user)
        TaskFactory.create_batch(5, project=pr1)
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 5)

    def test_amount_of_tasks_for_user(self):
        pr1 = ProjectFactory(user=self.user)
        pr2 = ProjectFactory(user=self.user2)
        TaskFactory.create_batch(5, project=pr1)
        TaskFactory.create_batch(2, project=pr2)
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(len(response.context['object_list']), 5)

