from django.contrib.auth import get_user_model
from django.test import TestCase

from blog.models import Blog

# Create your tests here.


class BlogTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(phone="98912888888")
        self.blog = Blog.objects.create(
            author=self.user, 
            title='title-test-1',
            body='title-test-1', 
            summary="summary-test-1",
            special=True,
            status='p',
            visits=1,
        )

    def test_str_method(self):
        self.assertEquals(str(self.blog), f"{self.user.first_name} {self.blog.title}")
        self.assertNotEqual(str(self.blog), f"{self.user.first_name}")

    def test_fields_blog_model(self):
        self.assertEquals(f"{self.blog.title}", "title-test-1")
        self.assertTrue(self.blog.special, True)
        self.assertNotEquals(self.blog.status, 'd')

    def test_is_generate_slug(self):
        self.assertIsNotNone(self.blog.slug)

    def test_the_profile_of_the_author_of_the_blog(self):
        self.assertEquals(self.blog.author.phone, "98912888888")
        self.assertNotEquals(self.blog.author.phone, "99999999999")

