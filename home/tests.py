from django.test import TestCase


# ------------ VIEWS TESTING ------------

class HomeViewTestCase(TestCase):
    """
    Test case for testing home views.
    """

    def test_home_render(self):
        """
        Tests that the home page is rendered properly
        """

        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'home/index.html', 'base.html'
            )

    def test_about_render(self):
        """
        Tests that the home page is rendered properly
        """

        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'home/about.html', 'base.html'
            )
