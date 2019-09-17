from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate
from django.utils.translation import ugettext_lazy as _

class TestHomePage(TestCase):

    def test_uses_en_language(self):
        activate('en')
        response = self.client.get(reverse("tasks:base_view"))
        self.assertTemplateUsed(response, "base.html")

    def test_uses_ru_language(self):
        activate('ru')
        response = self.client.get(reverse("tasks:base_view"))
        self.assertTemplateUsed(response, "base.html")

    def test_translate_by_default(self):
        self.assertEqual(_('translate this'), 'Translate This')

    def test_translate_by_en(self):
        activate('en')
        self.assertEqual(_('translate this'), 'Translate This')

    def test_translate_ru(self):
        activate('ru')
        self.assertEqual(_('translate this'), 'Переведи это')