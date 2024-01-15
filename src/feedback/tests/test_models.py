from django.test import TestCase
from block.models import Post, Comment, Block, Text, Vote
from core.models import User
# Create your tests here.
import logging

class TestBlockModel(TestCase):

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

        self.block1 = Block.objects.create(
            name="first block",
            creator=self.u1
        )
        
        self.post1 = Post.objects.create(
            title="first post",
            author=self.u1,
            block=self.block1,
        )
        self.post2 = Post.objects.create(
            title="first post",
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
            text="woow"
        )
        self.text2 = Text.objects.create(
            text="wpow"
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

    def test_save_count(self):
        self.post1.saved.add(self.u1)
        self.comment2.saved.add(self.u1)
        self.assertEqual(self.post1.saved_count,1)
        self.assertEqual(self.comment2.saved_count,1)
        self.assertNotEqual(self.post1.saved_count,31)
        self.assertNotEqual(self.comment1.saved_count,31)
    
    def test_comment_str(self):
        self.assertEqual(str(self.comment1),"woow")

