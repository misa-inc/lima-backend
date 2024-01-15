from django.test import TestCase
from page.models import Page
from post.models import Post
from account.models import User
# Create your tests here.
import logging


class TestPageModel(TestCase):

    def setUp(self):
        self.u1 = User.objects.create_user(
            email="twerv@gmail.com",
            username="vew123", password="t6n795123")
        
        self.u2 = User.objects.create_user(
            email="tveryt2@gmail.com",
            username="cev223", password="t4f5123")
        self.u3 = User.objects.create_user(
            email="t56hu3@gmail.com",
            username="beft32", password="t1231s23")

        self.page1 = Page.objects.create(
            name="first page",
            creator=self.u1
        )
        
        

