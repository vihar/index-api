from index.db.models import User
from rest_framework import serializers



class IndexUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"