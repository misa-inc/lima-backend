from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase
from rest_framework import status

import json

from blog.models import Blog
from blog.api import serializers

# Create your tests here.


class BlogViewsTest(APITestCase):

    def setUp(self) -> None:
        self.user1 = get_user_model().objects.create_superuser(
            phone="989101608150",
            first_name="first-name-test-1",
            last_name="last-name-test-1",
        )
        self.refresh_for_user1 = RefreshToken.for_user(self.user1)

        self.user2 = get_user_model().objects.create_user(
            phone="989101608151",
            first_name="first-name-test-2",
            last_name="last-name-test-2",
            author=True,
        )
        self.refresh_for_user2 = RefreshToken.for_user(self.user2)

        self.user3 = get_user_model().objects.create_user(
            phone="989101608152",
            first_name="first-name-test-3",
            last_name="last-name-test-3",
        )
        self.refresh_for_user3 = RefreshToken.for_user(self.user3)

        self.blog1 = Blog.objects.create(
            author=self.user1,
            title="title-test-1",
            body="body-test-1",
            summary="summary-test-1",
            special=True,
            status="p",
            visits=1,
        )
        self.blog1.category.add(self.category)

        self.blog2 = Blog.objects.create(
            author=self.user2,
            title="title-test-2",
            body="body-test-2",
            summary="summary-test-2",
            special=True,
            status="p",
            visits=1,
        )
        self.blog2.category.add(self.category)

        self.valid_data = {
            "title": "valid-title-test-1",
            "body": "valid-body-test-1",
            "summary": "valid-summary-test-1",
            "special": True,
            "category": [
                self.category.pk,
            ],
            "status": "p",
        }
        self.updated_data = {
            "title": "update-title-test-1",
            "body": "update-body-test-1",
            "summary": "update-summary-test-1",
            "special": True,
            "category": [
                self.category.pk,
            ],
            "status": "p",
        }

    def test_blogs_list(self):
        response = self.client.get(reverse("blog:api:list"))
        blogs = Blog.objects.publish()
        serializer = serializers.BlogsListSerializer(blogs, many=True)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(serializer.data, response.data)

    def test_search_blogs_list(self):
        response = self.client.get(reverse("blog:api:list") + "?search=test")
        content = json.loads(response.content)
        self.assertEquals(len(content), 2)

        response = self.client.get(reverse("blog:api:list") + "?search=1234")
        content = json.loads(response.content)
        self.assertNotEquals(len(content), 1)

    def test_blog_create_with_user1(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user1.access_token}"
        )

        serializer = serializers.BlogCreateSerializer(data=self.valid_data)
        serializer.is_valid(raise_exception=True)
        response = self.client.post(
            path=reverse("blog:api:create"),
            data=serializer.data,
        )
        content = json.loads(response.content)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(content.get("status"), self.valid_data.get("status"))
        self.assertTrue(content.get("special"))

    def test_blog_create_with_user2(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user2.access_token}"
        )

        serializer = serializers.BlogCreateSerializer(data=self.valid_data)
        serializer.is_valid(raise_exception=True)
        response = self.client.post(
            path=reverse("blog:api:create"),
            data=serializer.data,
        )
        content = json.loads(response.content)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(content.get("status"), "d")
        self.assertFalse(content.get("special"))

    def test_blog_create_with_user3(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user3.access_token}"
        )

        serializer = serializers.BlogCreateSerializer(data=self.valid_data)
        serializer.is_valid(raise_exception=True)
        response = self.client.post(
            path=reverse("blog:api:create"),
            data=serializer.data,
        )

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_blog_like(self):
        path = reverse("blog:api:like", args=[self.blog1.pk])
        response = self.client.get(path=path)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user2.access_token}"
        )
        response = self.client.get(path=path)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertQuerysetEqual(self.user2.blogs_like.all(), [self.blog1])

        response = self.client.get(path=path)
        self.assertQuerysetEqual(self.user2.blogs_like.all(), [])

    def test_blog_detail(self):
        path = reverse("blog:api:detail", kwargs={"slug": self.blog1.slug})
        response = self.client.get(path=path)
        blog = Blog.objects.publish().get(slug=self.blog1.slug)
        serializer = serializers.BlogDetailUpdateDeleteSerializer(blog)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

        path = reverse("blog:api:detail", kwargs={"slug": "test"})
        response = self.client.get(path=path)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_blog_update_with_user1(self):
        path = reverse("blog:api:detail", kwargs={"slug": self.blog1.slug})

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user1.access_token}"
        )
        response = self.client.put(
            path=path,
            data=self.updated_data,
        )
        content = json.loads(response.content)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(content.get("title"), self.updated_data.get("title"))

    def test_blog_update_with_user2(self):
        path = reverse("blog:api:detail", kwargs={"slug": self.blog1.slug})
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user2.access_token}"
        )
        response = self.client.put(
            path=path,
            data=self.updated_data,
        )

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        path = reverse("blog:api:detail", kwargs={"slug": self.blog2.slug})
        response = self.client.put(
            path=path,
            data=self.updated_data,
        )
        content = json.loads(response.content)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(content.get("status"), "d")

    def test_blog_update_with_user3(self):
        path = reverse("blog:api:detail", kwargs={"slug": self.blog1.slug})
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user3.access_token}"
        )
        response = self.client.put(
            path=path,
            data=self.updated_data,
        )
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        path = reverse("blog:api:detail", kwargs={"slug": self.blog2.slug})
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user3.access_token}"
        )
        response = self.client.put(
            path=path,
            data=self.updated_data,
        )
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_blog_delete_with_user1(self):
        path = reverse("blog:api:detail", kwargs={"slug": self.blog1.slug})

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user1.access_token}"
        )
        response = self.client.delete(
            path=path,
        )
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_blog_delete_with_user2(self):
        path = reverse("blog:api:detail", kwargs={"slug": self.blog1.slug})

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user2.access_token}"
        )
        response = self.client.delete(
            path=path,
        )
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_blog_delete_with_user3(self):
        path = reverse("blog:api:detail", kwargs={"slug": self.blog1.slug})

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user3.access_token}"
        )
        response = self.client.delete(
            path=path,
        )
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
