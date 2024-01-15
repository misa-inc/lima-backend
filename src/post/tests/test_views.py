from block.models import Post, Comment, Block, Text, Vote
from core.models import User
from notifications.models import Notification

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from django.http import response
from django.urls import reverse, resolve

import json


class TestPostView(APITestCase):
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

        self.block1 = Block.objects.create(
            name="anan",
            creator=self.u1
        )
        
        self.post1 = Post.objects.create(
            title="first ghst",
            author=self.u1,
            block=self.block1,
        )
        self.post2 = Post.objects.create(
            title="first nmost",
            author=self.u1,
            block=self.block1,
            parent=self.post1
        )
        self.vote1 = Vote.objects.create(
            voter=self.u2,
            value=1,
            post=self.post1,
            comment=None
        )
        self.vote2 = Vote.objects.create(
            voter=self.u2,
            value=-1,
            post=self.post2,
            comment=None
        )
        
        self.text1 = Text.objects.create(
            text="gbow"
        )
        self.text2 = Text.objects.create(
            text="vbow"
        )
        self.comment1 = Comment.objects.create(
            author=self.u1,
            post=self.post1,
            text=self.text1
        )
        self.comment2 = Comment.objects.create(
            author=self.u1,
            post=self.post1,
            text=self.text2,
            parent_comment=self.comment1
        )
        self.vote3 = Vote.objects.create(
            voter=self.u3,
            value=-1,
            post=None,
            comment=self.comment1            
        )
        self.vote4 = Vote.objects.create(
            voter=self.u2,
            value=1,
            post=None,
            comment=self.comment2            
        )

        self.response = self.client.get("posts/all/", format="json")
        self.assertEqual(self.post1.title, "first ghst")

    def test_post_list(self):
        self.client.force_authenticate(user=self.u1)
        url = reverse("townsquare")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_post(self):#
        self.client.force_authenticate(user=self.u1)
        data = {"title": "adding from here"}
        url = reverse("create_post", kwargs={"block_name": "anan"})
        res = self.client.post(url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_save_post(self):
        self.client.force_authenticate(user=self.u1)
        url = reverse("save_post")
        response = self.client.post(url, {"pk": 1})
        self.assertEqual(response.data, {"saved": True})
        response = self.client.post(url, {"pk": 1})
        self.assertEqual(response.data, {"saved": False})

    def test_saved_list(self):
        self.client.force_authenticate(user=self.u1)
        url = reverse("users_saved_post")
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_report_post(self):
        self.client.force_authenticate(user=self.u1)
        url = reverse("report_post")
        response = self.client.post(url, {"pk": 1})
        self.assertEqual(response.data, {"report": True})
        response = self.client.post(url, {"pk": 1})
        self.assertEqual(response.data, {"report": False})

    def test_user_post(self):
        self.client.force_authenticate(user=self.u1)
        url = reverse("users_posts", kwargs={"username": "vw123"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_post_detail(self):
        self.client.force_authenticate(user=self.u1)
        url = reverse("users_post_detail", kwargs={"username": "vw123", "p_id": 1})
        response = self.client.get(url)

    def test_block_post(self):
        self.client.force_authenticate(user=self.u1)
        url = reverse("blocks_posts", kwargs={"b_name": "anan"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_block_post_detail(self):
        self.client.force_authenticate(user=self.u1)
        url = reverse("blocks_post_detail", kwargs={"b_name": "anan", "p_id": 1})
        response = self.client.get(url)
   
    def test_delete_post(self):
        self.client.force_authenticate(user=self.u1)
        url = reverse("post-delete", kwargs={"pk": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

