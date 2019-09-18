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

    def test_published_pr(self):
        self.client.force_login(self.user)
        self.client.post(self.url, self.form_data)
        self.assertEqual(Project.objects.last().title, "Golang")

    def test_create_pr_second(self):
        self.client.force_login(self.user)
        self.client.post(self.url, self.form_data)

        num_of_blogs = Project.objects.count()
        pr = Project.objects.get(title=self.form_data['title'])





# class BookUpdateTest(TestCase):
#     def test_update_book(self):
#         book = Book.objects.create(title='The Catcher in the Rye')
#
#         response = self.client.post(
#             reverse('book-update', kwargs={'pk': book.id}),
#             {'author': 'J.D. Salinger'})
#
#         self.assertEqual(response.status_code, 200)
#
#         book.refresh_from_db()
#         self.assertEqual(book.author, 'J.D. Salinger')


# class BookUpdateTest(TestCase):
#     def test_update_book(self):
#         book = Book.objects.create(title='The Catcher in the Rye')
#
#         response = self.client.post(
#             reverse('book-update', kwargs={'pk': book.id}),
#             {'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger'})
#
#         self.assertEqual(response.status_code, 302)
#
#         book.refresh_from_db()
#         self.assertEqual(book.author, 'J.D. Salinger')