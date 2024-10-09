from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer, UpdateSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method='post',
    request_body=UserSerializer,
    responses={201: 'User Created Successfully', 400: 'Bad Request'}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='put',
    request_body=UpdateSerializer,
    responses={200: 'User Updated Successfully', 400: 'Bad Request'}
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_view(request):
    user = request.user
    serializer = UpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    request_body=LoginSerializer,
    responses={200: 'Login Successful', 400: 'Bad Request'}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'message': 'Login successful.'
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    responses={200: 'Logout Successful', 400: 'Bad Request'}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh = request.data.get('refresh')
        if not refresh:
            return Response({"message": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh)
        token.blacklist()
        return Response({"message": "User logged out successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": "Invalid token or token already blacklisted."}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh Token')
        }
    ),
    responses={200: 'Token Refreshed Successfully', 400: 'Bad Request'}
)
@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any user to refresh tokens, even if their access token expired
def refresh_view(request):
    try:
        refresh = request.data.get('refresh')
        if not refresh:
            return Response({"message": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh)
        return Response({
            'access': str(token.access_token),
            'refresh': str(token),
            'message': 'Token refreshed successfully.'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
