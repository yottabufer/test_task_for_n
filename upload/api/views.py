import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from googleapiclient.errors import HttpError
from rest_framework.permissions import AllowAny
from .utils import create_file, drive_init


class CreateFileOnGoogleDriveView(APIView):
    """
    API для создания файла в Гугл-Диск
    """
    # Доступ для всех
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        # Получаем credentials, token и создаём драйвер
        credentials_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "credentials.json")
        token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token.json")
        drive = drive_init(credentials_path, token_path)
        # Получение информации из POST запроса
        file_name = request.data.get('name')
        file_content = request.data.get('data')
        # Чуть-чуть валидации на заполнение данных
        if not file_name or not file_content:
            return Response({'Ошибка': 'Поля name, data обязательны'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            create_file(drive, file_name, file_content)
            return Response({'Прекрасно': 'Файл создан успешно'})
        except HttpError as error:
            return Response({'Ошибка': f'{error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
