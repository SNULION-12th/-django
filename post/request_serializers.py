from rest_framework import serializers

from account.request_serializers import SignInRequestSerializer

#✏️serializer의 내부 기능을 통해 DB에 저장가능한 형태로 바꾸어줌.
class PostListRequestSerializer(serializers.Serializer):
    author = SignInRequestSerializer()
    title = serializers.CharField()
    content = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())


class PostDetailRequestSerializer(serializers.Serializer):
    author = SignInRequestSerializer()
    title = serializers.CharField()
    content = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())