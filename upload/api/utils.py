import io
import os
from googleapiclient.http import MediaIoBaseUpload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
]
SIZE_FILE = 1048576  # 1 МБ, квота на бесплатном сервере не резиновая


def validate(data, name):
    if data is None or name is None:
        return Response({'Ошибка': 'Поля name и data обязательны'}, status=HTTP_400_BAD_REQUEST)
    if len(data) > SIZE_FILE or len(name) > SIZE_FILE:
        return Response({'Ошибка': 'Превышен размер в 1МБ'}, status=HTTP_400_BAD_REQUEST)
    return None


def drive_init(credentials_path: str, token_path: str) -> build:
    """
    Инициализация драйвера
    :param credentials_path: путь к файлу credentials.json
    :param token_path: путь к файлу token.json
    :return: Объект гугл драйвера
    """
    credentials = None
    # Проверка/перезапись токена доступа
    if os.path.exists(token_path):
        credentials = Credentials.from_authorized_user_file(token_path, SCOPES)
        if credentials.expired:
            credentials.refresh(Request())
            with open(token_path, 'w') as token:
                token.write(credentials.to_json())
    # В случае отсутствия создаёт токен доступа
    else:
        auth_flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        credentials = auth_flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(credentials.to_json())
    return build('drive', 'v3', credentials=credentials)


def create_file(drive, name: str, data: str, folder_name: str = 'for_nova') -> str:
    """
    Создание файла в нужной папке
    :param drive: Объект драйвера из drive_init
    :param name: Имя файла
    :param data: Содержимое файла
    :param folder_name: Папка для загрузки
    :return: id созданного файла в гугле
    """
    # Поиск папки folder_name
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
    results = drive.files().list(q=query, fields='nextPageToken, files(id, name)').execute()
    folder_id = None
    for file in results.get('files', []):
        if file.get('name') == folder_name:
            folder_id = file.get('id')
            break
    # Если не было folder_name - создаём
    if not folder_id:
        folder = drive.files().create(
            body={'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}).execute()
        folder_id = folder.get('id')
    file_metadata = {
        'name': name,
        'mimeType': 'text/plain',
        'parents': [folder_id]
    }
    # Создание файла
    media = MediaIoBaseUpload(io.BytesIO(data.encode("utf-8")), mimetype='text/plain', resumable=True)
    file = drive.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')
