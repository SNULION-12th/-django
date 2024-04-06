from rest_framework import serializers

from account.request_serializers import SignInRequestSerializer


class TagListRequestSerialiizer(serializers.Serializer):
    content = serializers.CharField()
