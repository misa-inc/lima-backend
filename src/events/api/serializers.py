from rest_framework import serializers
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

from events.models import *

from account.api.serializers import UserSerializer


class EventSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField(default=[])

    class Meta:
        model = Event
        fields = '__all__'


class EventAttendeesSerializer(serializers.ModelSerializer):
    guests=UserSerializer(many=True, read_only=True)
    class Meta:
        model = Event
        fields = ('id', 'title','guests')

class JoinSerailizer(serializers.Serializer):
    code_adhesion=serializers.CharField(max_length=100)


class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = "__all__"


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = "__all__"


class AcknowledgementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acknowledgement
        fields = "__all__"


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = "__all__"
