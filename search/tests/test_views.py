from django.test import TestCase
from django.urls import reverse


class TestSearchLanding(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.brand = "inQueerstigate"
        cls.url = reverse("search-landing")

    def test_get_landing(self):
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "search/landing.html")
        self.assertContains(resp, self.brand)
