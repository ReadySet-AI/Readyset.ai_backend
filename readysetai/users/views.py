from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import ActivateUserSerializer


class ActivateUserView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ActivateUserSerializer

    def post(self, request):
        serializer = ActivateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User activated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
