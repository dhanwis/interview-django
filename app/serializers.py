from rest_framework import serializers
from .models import AUser

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = AUser
        fields = ["email", "username", "password", "dob", "phone",]

    def create(self, validated_data):
        user = AUser.objects.create_user(**validated_data)
        return user