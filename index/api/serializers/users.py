from rest_framework import serializers
from index.db.models import User, UserProfileDetail


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "token",
        )

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileDetail
        fields = "__all__"


class UserWithProfileSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()
    class Meta:
        model = User
        fields = ['username', 'email', 'user_profile']