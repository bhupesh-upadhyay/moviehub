from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, UserSerializer
from .services import UserService
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .tokens import email_verification_token
from .models import User
from django.contrib.auth import get_user_model

class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = UserService.create_user(serializer.validated_data)
            # serializer.save() -> this is now handled by service
            output = UserSerializer(user) # for output serializer
            return Response(output.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    # /api/users/verify-email/<uid>/<token>/
    def get(self, request, uid, token):
        User = get_user_model()
        try:
            # decode user id
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"error": "Invalid verification link"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if email_verification_token.check_token(user, token):
            if user.is_verified:
                return Response(
                    {"message": "Email already verified"},
                    status=status.HTTP_200_OK
                )
            user.save(update_fields=["is_verified", "is_active"])
            
            return Response(
                {"message": "Email verified successfully"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"error": "Invalid or expired token"},
            status=status.HTTP_400_BAD_REQUEST
        )
        