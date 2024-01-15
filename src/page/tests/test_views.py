from page.models import Page
from account.models import User
from notifications.models import Notification

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from django.http import response
from django.urls import reverse, resolve

import json


class TestPageView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.u1 = User.objects.create_user(
            email="twev@gmail.com",
            username="vw123", password="t6n5123")
        
        self.u2 = User.objects.create_user(
            email="tvry2@gmail.com",
            username="ev223", password="t4f523")
        self.u3 = User.objects.create_user(
            email="t5u3@gmail.com",
            username="bet32", password="t12313")

        self.page1 = Page.objects.create(
            name="anan",
            creator=self.u1
        )

    def test_page_post(self):
        self.client.force_authenticate(user=self.u1)
        url = reverse("pages_posts", kwargs={"group_name": "anan"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_page_post_detail(self):
        self.client.force_authenticate(user=self.u1)
        url = reverse("pages_post_detail", kwargs={"group_name": "anan", "p_id": 1})
        response = self.client.get(url)
   