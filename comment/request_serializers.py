from rest_framework import serializers


class ComentListRequestSerializer(serializers.Serializer):
    post = serializers.IntegerField()
    content = serializers.CharField()


class ComentDetailRequestSerializer(serializers.Serializer):
    content = serializers.CharField()
