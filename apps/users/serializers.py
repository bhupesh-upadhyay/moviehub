from rest_framework import serializers
from .models import User, UserProfile
from django.contrib.auth import authenticate



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    """
    Django login compares hashed password with stored hashed password.
    In-correct: User.objects.create(...) -> This does NOT hash the password & user creation logic, it gets stored as plain text.
    blindly gets called 
    correct: User.objects.create_user(...) -> it does all that & create_user() is defined inside Django’s UserManager.
    
    """
    # def create(self, validated_data):
    #     user = User.objects.create_user(
    #         email=validated_data["email"],
    #         username=validated_data["username"],
    #         password=validated_data["password"],
    #     )
    #     return user
    

# Output serializer Format outgoing data (Output)    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username"]
        
"""
Analogy:
For login we should NOT use ModelSerializer. Instead use a plain: serializers.Serializer
Because login is not creating or updating a model — it’s just validating credentials.
ModelSerializer automatically adds model validations, including: UniqueValidator
Because your User model likely has:email = models.EmailField(unique=True)
DRF automatically attaches this validator: Ensure email is unique
But you were trying to log in, not create a user.


ModelSerializer
Use when your serializer is directly tied to a model.
DRF automatically provide:
create()
update()
model field mapping
model validators (unique, required, etc.)
example RegisterSerializer
UserSerializer
ProfileSerializer

Serializer
Use when the serializer represents an operation, not a model.
example: Login
Password reset
Email verification
Search filters
OTP verification
Upload tokens
These represent actions, not model objects.

"Is this serializer representing a database object?"
If YES → ModelSerializer
If NO → Serializer
"""

class LoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
        
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        """
        authenticate()--
        checks password hash
        loads user
        respects authentication backends
        """
        user = authenticate(username=email, password=password)
        
        if not user:
            raise serializers.ValidationError("Invalid Credentials")
        
        if not user.is_verified:
            raise serializers.ValidationError("Email is not verified")
        
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")
        
        data['user'] = user
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.email', read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id', 'bio', 'avatar', 'date_of_birth', 'created_at', 'updated_at', 'username', 'email']
        read_only_fields = ['id', 'created_at', 'updated_at']