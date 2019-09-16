import sys
sys.path.append("..")

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.test import TestCase, Client

from todo_api.tests.factories_users import UserFactory
from todo_api.users.forms import CustomAuthenticationForm, CustomUserCreationForm

User = get_user_model()


class CreateUpdateDeleteUserTestCase(TestCase):

    def setUp(self):
        self.user = User.objects._create_user(email = 'asd@gmail.com', username='asd', password='12121212')
        self.user.set_password('121212')
        self.user.save()

    def test_create_user_valid_active(self):
        self.user.is_active = True
        self.user.save()
        self.assertTrue(self.user.is_active)

    def test_new_user_email_normalized(self):
        email = 'test@GMAIL.COM'
        user = get_user_model().objects._create_user(email, '12121212')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        ''' creating user with no email raises error '''
        with self.assertRaises(ValueError):
            get_user_model().objects._create_user(None, '12121212')

    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser('test@gmail.com', 'zaza1234')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class UsersTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = UserFactory()
        cls.url = reverse('users:login')
        cls.logout = reverse('users:logout')

    def test_current_user_is_anonymous(self):
        response = self.client.get(self.url)
        curr_user = response.context["user"]
        self.assertEqual(curr_user, AnonymousUser())

    def test_login_url_accessible_by_name(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_login_user(self):
        self.user.is_active = True
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.get('/')
        curr_user = response.wsgi_request.user
        self.assertEqual(curr_user, self.user)

    def test_logout_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.logout)
        self.assertEqual(response.status_code, 302)


class UserAuthenticationFormTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory(username='testing', email='testing@gmail.com', password=12121212)
        self.form = CustomAuthenticationForm

    def test_form_invalid_password(self):
        form = self.form(data={'username': 'testing@gmail.com', 'password':112223344})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEquals(form.errors['password'][0], 'Invalid password.')

    def test_form_valid_username(self):
        form = self.form(data={'username':'testing@gmail.com', 'password':12121212})
        self.assertTrue(form.is_valid())


class UserCreationFormTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory(username='testing', email='testing@gmail.com')
        self.form = CustomUserCreationForm

    def test_form_is_valid_full_info(self):
        form = self.form(data = {'username':'test', 'email':'test@test.com', 'password1':'123123123', 'password2':'123123123'})
        self.assertTrue(form.is_valid())

    def test_form_is_invalid_no_username(self):
        form = self.form(data = {'email':'test@test.com', 'password1':'123123123', 'password2':'123123123'})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEquals(form.errors['username'][0], 'This field is required.')

    def test_form_invalid_username(self):
        form = self.form(data = {'email':'test@test.com', 'password1':'123123123', 'password2':'123123123', 'username':'testing'})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEquals(form.errors['username'][0], 'User with this name already exist.')

    def test_form_differend_passwords(self):
        form = self.form(data={'email': 'test@test.com', 'password1': '123123123', 'password2': '12121212', 'username': 'test'})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEquals(form.errors['password2'][0], 'Your passwords don\'t match.')

    def test_form_invalid_email(self):
        form = self.form(data = {'email':'testing@gmail.com', 'password1':'123123123', 'password2':'123123123', 'username':'test'})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEquals(form.errors['email'][0], 'User with email testing@gmail.com already exists.')

    def test_form_invalid_email_forget_sign(self):
        form = self.form(data = {'email':'testing#test.com', 'password1':'123123123', 'password2':'123123123', 'username':'test'})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEquals(form.errors['email'][0], 'Missed the @ symbol in the email address.')

    def test_form_invalid_email_forget_dot(self):
        form = self.form(data = {'email':'testing@test,com', 'password1':'123123123', 'password2':'123123123', 'username':'test'})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEquals(form.errors['email'][0], 'Missed the . symbol in the email address.')