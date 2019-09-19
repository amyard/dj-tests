from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.translation import activate

from tests.factories_users import UserFactory
from tests.factories_tasks import ProjectFactory
from tasks.models import Project
from tasks.forms import ProjectCreateForm
User = get_user_model()


class ProjectTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = UserFactory(is_active=True)
        cls.url = reverse('tasks:base_view')

    def test_login_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        curr_user = response.wsgi_request.user
        self.assertEqual(curr_user, self.user)

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user)
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location_localization(self):
        activate('en')
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks:base_view"))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('tasks:base_view'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        assert 'base.html' in [t.name for t in response.templates]


class ProjectTestCaseListView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = UserFactory(is_active=True)
        cls.user2 = UserFactory(is_active=True)
        cls.url = reverse('tasks:project_list')

    def test_no_data(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry, no projects yet.")
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_slug(self):
        usr = User.objects._create_user(username='asd', email='asd@asd.com', password='zaza1234')
        pr = Project.objects.create(title='test', color='black', user=usr)
        self.assertEqual(pr.slug, 'test-asd')

    def test_check_amount_of_projects(self):
        ProjectFactory.create_batch(5, user=self.user)
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 5)

    def test_amount_of_project_all_project(self):
        ProjectFactory.create_batch(5, user=self.user)
        ProjectFactory.create_batch(2, user=self.user2)
        self.assertEqual(Project.objects.count(), 7)

    def test_amount_of_project_for_user(self):
        ProjectFactory.create_batch(5, user=self.user)
        ProjectFactory.create_batch(2, user=self.user2)
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['object_list']), 5)


class ProjectTestCaseDeleteView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = UserFactory()
        cls.pr = ProjectFactory(user=cls.user)
        cls.pr_slug = cls.pr.slug
        cls.url = reverse('tasks:project_delete', args=[cls.pr_slug])

    def test_object_exists(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_object_delete(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

        # object was deleted - check
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Project.objects.filter(slug=self.pr_slug).exists())


class ProjectTestCaseCreateView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form = ProjectCreateForm
        cls.client = Client()
        cls.user = UserFactory()
        cls.form_data = {'title':'Golang','color':'primary'}
        cls.pr = ProjectFactory(user=cls.user)
        cls.url = reverse('tasks:project_create')
        cls.redirect_url = reverse('tasks:project_list')
        cls.redirect_login = '/en/users/login/?next=/en/project-create/'


    def test_user_not_logged(self):
        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_login, status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_published_pr(self):
        self.client.force_login(self.user)
        self.client.post(self.url, self.form_data)
        self.assertEqual(Project.objects.last().title, "Golang")

    def test_create_pr_second(self):
        self.client.force_login(self.user)
        self.client.post(self.url, self.form_data)
        num_of_pr = Project.objects.count()
        pr = Project.objects.get(title=self.form_data['title'])
        self.assertEqual(pr.user, self.user)
        self.assertEqual(pr.title, 'Golang')
        self.assertEqual(num_of_pr, 2)

    def test_create_pr_check_redirect_after_success(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.form_data)
        self.assertRedirects(response, self.redirect_url, status_code=302,
                             target_status_code=200, fetch_redirect_response=True)




class ProjectTestCaseDeleteView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = UserFactory()
        cls.user2 = UserFactory()
        cls.user3 = UserFactory(is_superuser=True, is_admin=True, is_staff=True)
        cls.pr = ProjectFactory(user=cls.user)
        cls.pr_slug = cls.pr.slug
        cls.url = reverse('tasks:project_update', args=[cls.pr_slug])
        cls.form_data = {'title': 'Golang', 'color': 'primary'}


    def test_update_view_for_correct_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_for_wrong_user(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_update_view_user_not_logged(self):
        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/en/users/login/?next=/en/project-update/new-title-for-project-2-username_3/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_update_data_correct_user(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.form_data)
        self.assertRedirects(response, reverse('tasks:project_list'),
                             status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.pr.refresh_from_db()
        self.assertEqual(self.pr.title, 'Golang')

    def test_update_data_superuser(self):
        self.client.force_login(self.user3)
        response = self.client.post(self.url, self.form_data)
        self.assertRedirects(response, reverse('tasks:project_list'),
                             status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.pr.refresh_from_db()
        self.assertEqual(self.pr.title, 'Golang')


class ProjectTestCaseDeleteView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = UserFactory()
        cls.user2 = UserFactory()
        cls.user3 = UserFactory(is_superuser=True, is_admin=True, is_staff=True)
        cls.pr = ProjectFactory(user=cls.user)
        cls.pr_slug = cls.pr.slug
        cls.url = reverse('tasks:project_delete', args=[cls.pr_slug])

    def test_delete_view_user_not_logged(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/en/users/login/?next=/en/project-delete/new-title-for-project-2-username_3', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_delete_view_get_function_with_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Are you sure you want to delete')
        assert 'base.html' in [t.name for t in response.templates]
        assert 'tasks/project_delete.html' in [t.name for t in response.templates]

    def test_delete_project_correct_user(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks:project_list'), status_code=302,target_status_code=200, fetch_redirect_response=True)
        self.assertEqual(Project.objects.count(), 0)

    def test_delete_view_for_wrong_user(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_delete_data_superuser(self):
        self.client.force_login(self.user3)
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('tasks:project_list'),
                             status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertEqual(Project.objects.count(), 0)
