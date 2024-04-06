from rest_framework import serializers

from account.request_serializers import SignUpRequestSerializer


class TagListRequestSerialiizer(serializers.Serializer):
    author = SignUpRequestSerializer()
    content = serializers.CharField()
