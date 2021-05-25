from django.contrib.auth import get_user_model
from rest_framework import serializers


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



