from index.db.models import User
from rest_framework.response import Response
from rest_framework import viewsets


from  index.api.serializers.plat import IndexUserSerializer


class IndexUserViewset(viewsets.ModelViewSet):
    serializer_class = IndexUserSerializer
    queryset = User.objects.all()

    def list(self, request):
        level_users = User.objects.all()
        serializer = IndexUserSerializer(level_users, many=True)
        return Response(serializer.data)