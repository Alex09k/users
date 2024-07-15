from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import MyUser


class MyUserSerialiser(serializers.ModelSerializer):
    """Сериализатор для регистрации."""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=MyUser.objects.all())]
    )

    class Meta:
        model = MyUser
        fields = ["id", "username", "password", "email"]


class MyUserListSerialiser(serializers.ModelSerializer):
    """Сериализатор для получения списка users."""

    class Meta:
        model = MyUser
        fields = ["id", "username", "email"]
