from user.models import User

from rest_framework import serializers

from common.date_utils import calculate_age, valid_age
import datetime


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = User
        fields = ("id", "email", "password", "username", "birthdate", "image")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""

        return User.objects.create_user(**validated_data)

    def validate_birthdate(self, value):
        """Validate the birthdate of the user"""
        if not value:
            raise serializers.ValidationError(
                "The field birthdate cannot be blank.")
        elif (isinstance(value, datetime.date)):
            age = calculate_age(value)
            if age >= valid_age:
                return value

        raise serializers.ValidationError(
            "The user must have 18 years old or older")


class UserDetailSerializer(UserSerializer):
    """Serializer for the user object"""
    class Meta:
        model = User
        fields = ("email", "username", "birthdate", "image")


class UserPlaySessionSerializer(serializers.ModelSerializer):
    """Serializer for the user and play session object"""
    last_played_session = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ("email", "username", "birthdate", "last_played_session")

    def to_representation(self, instance):
        """Obtain the last user played game from PlaySession"""
        representation = super().to_representation(instance)

        last_played_session = representation.get("last_played_session")
        if last_played_session and len(last_played_session) > 0:
            representation['last_played_session'] = last_played_session[-1]
        else:
            representation['last_played_session'] = ""
        return representation


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()

    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)
