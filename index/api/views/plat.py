from index.db.models import User, UserProfileDetail
from rest_framework.response import Response
from rest_framework import viewsets


from  index.api.serializers.plat import IndexUserSerializer
from index.api.serializers.users import UserProfileSerializer


class IndexUserViewset(viewsets.ModelViewSet):
    serializer_class = IndexUserSerializer
    queryset = User.objects.all()

    def list(self, request):
        users = User.objects.all()
        serializer = IndexUserSerializer(users, many=True)
        return Response(serializer.data)


class UserProfileViewset(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfileDetail.objects.all()

    def list(self, request):
        user_profule = UserProfileDetail.objects.all()
        serializer = UserProfileSerializer(user_profule, many=True)
        return Response(serializer.data)