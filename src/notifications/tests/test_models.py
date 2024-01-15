from rest_framework.test import APITestCase
from notifications.models import Notification
from core.models import User
from block.models import Post, Block


class TestNotiModel(APITestCase):

    def setUp(self):
        self.u1 = User.objects.create_user(
            email="test@gmail.com",
            username="test", phone="08156912577", password="test5123")
        
        self.u2 = User.objects.create_user(
            email="test2@gmail.com",
            username="tes223", phone="08156912597", password="test123")
        self.u3 = User.objects.create_user(
            email="test3@gmail.com",
            username="tes32", phone="08156912507", password="test1s23")

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

    def test_message_str(self):
        notifications = Notification.objects.create(
              notification_type='R',
                post=self.post1,
                to=self.u2,
                creator=self.u1
        )
        self.assertEqual(str(notifications),f'From: {self.u1} - To: {self.u2}')