from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate,login, logout
from django.middleware.csrf import get_token

class UserRegistrationView(APIView):
    permission_classes=[AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class UserLoginView(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"message": "Username/email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)

            return Response(
                {"message": "user logged in Succesfully"},
                status = status.HTTP_200_OK
            )

        return Response(
            {"message" : "username or password incorrect"},
            status = status.HTTP_401_UNAUTHORIZED
        )

class UserLogoutView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        logout(request)

        return Response(
            {"message": "logout"},
            status=status.HTTP_200_OK
        )

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        })


class CsrfTokenView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"csrfToken": get_token(request)})
