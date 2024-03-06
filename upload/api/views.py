import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from googleapiclient.errors import HttpError
from rest_framework.permissions import AllowAny
from .utils import create_file, drive_init, validate


class CreateFileOnGoogleDriveView(APIView):
    """
    API для создания файла в Гугл-Диск
    """
    # Доступ для всех
    permission_classes = [AllowAny, ]

    def post(self, request):
        # Получаем credentials, token и создаём драйвер
        credentials_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json')
        token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'token.json')
        drive = drive_init(credentials_path, token_path)
        # Получение информации из POST запроса
        file_name = self.request.data.get('name')
        file_data = self.request.data.get('data')
        # Чуть-чуть валидации на заполнение данных
        validate(file_data, file_name)
        try:
            create_file(drive, file_name, file_data)
            return Response({'Прекрасно': 'Файл создан успешно'})
        except HttpError as error:
            return Response({'Ошибка': f'{error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
