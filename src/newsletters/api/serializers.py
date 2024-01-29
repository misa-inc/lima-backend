from rest_framework import serializers
from newsletters.models import Newsletter, Article
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

class NewsletterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Newsletter
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField(default=[])

    class Meta:
        model = Article
        fields = '__all__'
