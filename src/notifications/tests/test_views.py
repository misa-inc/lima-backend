from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.http import response
from django.urls import reverse, resolve

from block.models import Post, Block
from notifications.models import Notification
from core.models import User

class TestNotificationView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.u1 = User.objects.create_user(
            email="testx34@gmail.com",
            username="tesvt", phone="08156912531", password="tesct123")
        
        self.u2 = User.objects.create_user(
            email="test2356@gmail.com",
            username="tesrt", phone="08156912540", password="test166723")

        self.block1 = Block.objects.create(
            name="first block",
            creator=self.u1
        )
        
        self.post1 = Post.objects.create(
            title="first post",
            author=self.u1,
            block=self.block1,
        )
      
        
        self.client.force_authenticate(user=self.u1)

    #def test_notification_list(self):
    #    url= reverse("notification-list")
    #    response = self.client.get(url, format="json")
    #    self.assertEqual(response.status_code, status.HTTP_200_OK)
    #    self.assertEqual(response.data["data"]["noti_count"], None)


    #def test_notification_seen(self):
    #    url= reverse("notification-seen")
    #    response = self.client.get(url, format="json")
    #    self.assertEqual(response.data, {'user_seen':True})
    #    self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    #def test_notification_delete(self):
    #    url= reverse("notification-seen")
    #    Notification.objects.create(
    #          notification_type='R',
    #            post=self.post1,
    #            to_user=self.u1,
    #            from_user=self.u2
    #    )
    #    response = self.client.post(url, {"notify_id":1})
    #    self.assertEqual(response.status_code,status.HTTP_200_OK)
    #    self.assertEqual(response.data, {'notification_deleted':True})
