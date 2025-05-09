from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    re_password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["email", "first_name", "last_name", "password", "re_password"]

    def validate(self, data):
        if data["password"] != data["re_password"]:
            raise serializers.ValidationError("passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop("re_password")
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ["id", "first_name", "last_name", "email"]
