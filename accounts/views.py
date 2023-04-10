"""
    Views for user
"""
from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from accounts import serializers
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

User = get_user_model()


# Create your views here.
class UserRegistration(APIView):
    """Register new user"""
    serializer_class = serializers.RegistrationSerializer

    @swagger_auto_schema(
        request_body=serializer_class,
    )
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                'email': serializer.data['email'],
                'msg': "Created Successfully",
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class UserDetailUpdate(APIView):
    """Get user detail or update for authorized user"""
    serializer_class = serializers.UserSerializer

    def get(self, request, format=None):
        # get user details for authorized user
        user = request.user
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=serializer_class,
    )
    def put(self, request, format=None):
        # update user details for authorized user
        user = request.user
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class ChangePassword(APIView):
    """change user password for authorized user"""
    serializer_class = serializers.ChangePasswordSerializer

    @swagger_auto_schema(
        request_body=serializer_class,
    )
    def post(self, request, format=None):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({'msg': 'Unauthorized User'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'msg': 'Password updated successfully.'
        }, status=status.HTTP_200_OK)


"""
    Admin APIs
"""


@permission_classes([IsAdminUser])
class GetAllUsers(APIView):
    """Get All user by admin user"""
    serializer_class = serializers.UserSerializer

    def get(self, request, format=None):
        users = User.objects.filter()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([IsAdminUser])
class DeleteUser(APIView):
    """Delete a user by admin user"""
    serializer_class = serializers.UserSerializer

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response({
            'msg': 'deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
