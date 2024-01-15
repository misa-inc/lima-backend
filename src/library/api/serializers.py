from django.contrib.auth import get_user_model # If used custom user model
from rest_framework import serializers
from library.models import *
from account.models import *


class AuthorSerializer(serializers.ModelSerializer):
   class Meta:
      model    = Author
      fields   = '__all__'

class BookSerializer(serializers.ModelSerializer):

   author_name    = serializers.ReadOnlyField(source='author.name')
   category_name  = serializers.ReadOnlyField(source='category.name')
   comment_text   = serializers.ReadOnlyField(source='comment.body')

   class Meta:
      model    = Book
      fields   = ('id', 'name', 'file', 'language', 'pages', 'descreption', 'added_date', 'author', 'category', 'author_name', 'category_name', 'comment_text')

class CategorySerializer(serializers.ModelSerializer):
   class Meta:
      model    = Category
      fields   = '__all__'

class CommentSerializer(serializers.ModelSerializer):
   username    = serializers.ReadOnlyField(source='user.username')
   
   class Meta:
      model   = Comment
      fields  = ('id', 'book', 'user', 'rating', 'username', 'body', 'created_on')
