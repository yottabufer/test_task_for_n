from django.urls import path
from .views import CreateFileOnGoogleDriveView

urlpatterns = [
    path("upload/", CreateFileOnGoogleDriveView.as_view(), name="file-upload"),
]
