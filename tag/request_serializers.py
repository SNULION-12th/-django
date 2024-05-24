from rest_framework import serializers


class TagListRequestSerialiizer(serializers.Serializer):
    content = serializers.CharField()
