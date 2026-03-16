from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle

from .serializers import RegisterSerializer, UserSerializer, LoginSerializer, UserProfileSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from .services import UserService, AuthService
from .tokens import email_verification_token
from .models import User, UserProfile
from .tasks import send_password_reset_email_task

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
            # user.is_verified = True
            # user.is_active = True
            user.save(update_fields=["is_verified", "is_active"])
            
            return Response(
                {"message": "Email verified successfully"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"error": "Invalid or expired token"},
            status=status.HTTP_400_BAD_REQUEST
        )
        
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response(
            {                
                "access":str(refresh.access_token),
                "refresh":str(refresh),
                "user":UserSerializer(user).data
            }
        )
        
        
class ProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """
        request.user.profile
        It prevents errors like:
            UserProfile.DoesNotExist
        Your API becomes self-healing.
        Even if data is inconsistent, the endpoint still works.‘
        """
        
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
    
class ForgotPasswordView(APIView):
    throttle_classes = [AnonRateThrottle]
    def post(self, request):
        serialzer = ForgotPasswordSerializer(data=request.data)
        
        if not serialzer.is_valid():
            return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serialzer.validated_data['email']
        send_password_reset_email_task.delay(email)
        
        return Response({
            'message':"If the email exists, a password reset link has been sent."
        })

class ResetPasswordView(APIView):
    def post(self, request, uid, token):
        serializer = ResetPasswordSerializer(data=request.data)
        # check validation
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error':'Invalid valid link'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not email_verification_token.check_token(user, token):
            Response({'error':'Invalid or Expired token'}, status=status.HTTP_400_BAD_REQUEST)
        
        new_passowrd = serializer.validated_data['password']
        user.set_password(new_passowrd)
        user.save()
        
        return Response({'message':'Password reset successfully'}, status=status.HTTP_400_BAD_REQUEST)
