from django.test import TestCase
from django.urls import reverse


class MainPageTest(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
