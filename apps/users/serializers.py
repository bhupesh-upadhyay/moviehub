from rest_framework import serializers
from .models import User


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