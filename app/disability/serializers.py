from rest_framework import serializers
from .models import *


class AssistiveDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssistiveDevice
        fields = ('id', 'name',)


class DisabilityDetailSerializer(serializers.ModelSerializer):
    assistive_devices = AssistiveDeviceSerializer(read_only=True, many=True)

    class Meta:
        model = DisabiltiyDetail
        fields = ('id', 'name', 'assistive_devices')


class DisabilityQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisabilityQuestion
        fields = ('id', 'name', 'question_type', 'mandatory')
