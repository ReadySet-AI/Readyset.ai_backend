from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from users.models import CustomUser


class ActivateUserSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        data["password"] = data.get("password", "").replace(" ", "")
        data["confirm_password"] = data.get("confirm_password", "").replace(
            " ", ""
        )

        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        try:
            validate_password(data["password"])
            validate_password(data["confirm_password"])
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

        try:
            user_id = force_str(urlsafe_base64_decode(data["uid"]))
            user = CustomUser.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise serializers.ValidationError({"uid": "Link is invalid"})

        if not default_token_generator.check_token(user, data["token"]):
            raise serializers.ValidationError(
                {"token": "Token is invalid or has expired."}
            )

        data['user'] = user

        return data

    def create(self, validated_data):
        password = validated_data.pop("password")

        with transaction.atomic():
            user = validated_data['user']
            user.set_password(password)
            user.is_active = True
            user.save()

        return user
