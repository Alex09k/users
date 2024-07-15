from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.authtoken.models import Token

from users.serializers import MyUserSerialiser, MyUserListSerialiser
from users.models import MyUser

from django.shortcuts import get_object_or_404


class UserRegistrationView(APIView):
    """ Класс для регистрации пользователя."""

    def post(self, request):
        """
        Эта функция создает нового пользователя
        в системе. Она принимает запрос с данными пользователя,
        сериализирует их, проверяет валидность, сохраняет в базу
        данных, устанавливает пароль и возвращает ответ с созданным
        пользователем или ошибкой валидации.
        """
        serializer = MyUserSerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = MyUser.objects.get(username=request.data["username"])
            user.set_password(request.data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAuthenticationView(APIView):
    """ Класс для аунтификации пользователя."""

    def post(self, request):
        """
        Функция аутентификации пользователя.
        Она принимает запрос с именем пользователя
        и паролем, проверяет их валидность, и если они корректны,
        возвращает токен для доступа к системе
        """
        user = get_object_or_404(MyUser, username=request.data['username'])
        if not user.check_password(request.data["password"]):
            return Response({"detal": "Not Found"},
                            status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class UserListView(APIView):
    """ Класс для получения списка пользователей."""

    def get(self, request):
        """
        Функция get для получения списка всех пользователей в системе.
        Она получает список всех пользователей из базы данных,
        сериализирует его и возвращает ответ с данными в формате JSON
        """
        users = MyUser.objects.all()
        serializer = MyUserListSerialiser(users, many=True)
        return Response(serializer.data)


class UserDetail(APIView):
    """ Класс для изменения пользователя."""
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def patch(self, request, pk):
        """
        Функция patch для обновления данных пользователя.
        Она получает запрос с идентификатором пользователя (pk)
        проверяет, является ли пользователь, делающий запрос,
        владельцем профиля, и пользователь имеет право на это.
        Если данные валидны, то они сохраняются, иначе возвращается ошибка
        """
        user = get_object_or_404(MyUser, pk=pk)
        if user != request.user:
            return Response({"error":
                             "You do not have permission to view this user"},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = MyUserSerialiser(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Функция delete для удаления пользователя по идентификатору (pk).
        Она получает запрос с идентификатором пользователя, проверяет,
        является ли пользователь, делающий запрос, владельцем профиля,
        и если да, то удаляет пользователя из базы данных.
        Если пользователь не имеет права на удаление, то возвращается
        ошибка с кодом 403. Если удаление прошло успешно, то возвращается ответ
        с сообщением об успешном удалении и кодом 204
        """
        user = get_object_or_404(MyUser, pk=pk)
        if user != request.user:
            return Response({"error":
                             "You do not have permission to view this user"},
                            status=status.HTTP_403_FORBIDDEN)
        user.delete()
        return Response({f"{user.username} deleted successfully."},
                        status=status.HTTP_204_NO_CONTENT)
