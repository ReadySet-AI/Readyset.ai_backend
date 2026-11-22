from django.urls import path
from users.views import ActivateUserView

urlpatterns = [
    path(
        "activate/",
        ActivateUserView.as_view(),
        name="activate-user",
    ),
]
