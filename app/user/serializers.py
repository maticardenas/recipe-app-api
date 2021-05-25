from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

class UserSerializer(serializers.ModelSerializer):
    """ Serializer for the users object """

    class Meta:
        model = get_user_model()
        fields = ("email", "password", "name")
        extra_kwargs = {
            "password": {
                "write_only": True, # We only want password to create new objects, not retrieving
                "min_length": 5,
                "style": {"input_type": "password"} # Don't show password while writing it
            }
        }

    # We need it because we need to call the create method of the model as
    # we need to store the password as hash.
    def create(self, validated_data):
        """ Creates and returns a new user """
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """ Serializer for the user authentication object """
    email = serializers.CharField()
    password = serializers.CharField(
        style = {"input_type": "password"},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """ Validate and authenticate the user """
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password
        )

        if not user:
            msg = ("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code="authentication")

        attrs["user"] = user
        return attrs



