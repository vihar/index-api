
from django.urls import path


from .views.authentication import signup_view, login_view

from .views.plat import IndexUserViewset
# Create your urls here.

urlpatterns = [
      path(
        "signin/",
        login_view,
        name="signin",
    ),
    path(
        "signin/",
        login_view,
        name="signin",
    ),
    path(
        "signup/",
        signup_view,
        name="signup",
    ),
     path(
        "users/<int:pk>/",
        IndexUserViewset.as_view(
            {"get": "retrieve", "put": "partial_update", "delete": "destroy"}
        ),
        name="level-users-detail",
    ),
]