from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.CharField()
    username = serializers.CharField()

class UserDetailSerializer(serializers.Serializer):
    id = serializers.CharField()
    username = serializers.CharField()

class UserUpdateSerializer(serializers.Serializer):
    id = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
