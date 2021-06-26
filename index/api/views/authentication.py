# accounts.utils
import datetime
import jwt
import uuid

from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from allauth.utils import generate_unique_username
from rest_framework.views import APIView
from rest_framework import viewsets

from django.views.decorators.csrf import ensure_csrf_cookie
from django.http.response import Http404
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail


from index.api.serializers.users import UserSerializer
from index.db.models import User


def generate_access_token(user):

    access_token_payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=10080),
        "iat": datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(
        access_token_payload, settings.SECRET_KEY, algorithm="HS256"
    )
    return access_token


# token versions
def generate_refresh_token(user):
    refresh_token_payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
        "iat": datetime.datetime.utcnow(),
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.REFRESH_TOKEN_SECRET, algorithm="HS256"
    )

    return refresh_token


# @ensure_csrf_cookie


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")
    response = Response()

    email = request.data.get("email")
    if (email is None) or (password is None):
        raise exceptions.AuthenticationFailed("email and password required")
    user = User.objects.get(email=email)
    if user is None:
        raise exceptions.AuthenticationFailed("user not found")
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed("wrong password")

    serialized_user = UserSerializer(user).data

    # settings last active for the user
    user.last_active = timezone.now()
    user.save()
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
  

    response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)
    response.data = {
        "access_token": access_token,
        "user": serialized_user,
    }

    return response


# accounts.authentication


@api_view(["POST"])
@permission_classes([AllowAny])
def signup_view(request):

    first_name = request.data.get("first_name", "")
    last_name = request.data.get("last_name", "")

    email = request.data.get("email")
    password = request.data.get("password")

    random_string = uuid.uuid4().hex

    if (email is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            "please provide email or phone number to signup"
        )
    response = Response()

    # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#exists

    if User.objects.filter(email=email).exists():
        raise exceptions.AuthenticationFailed("user already exists")

    username = generate_unique_username([email])
    user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        mobile_number=random_string,
    )
    user.set_password(password)
    user.save()
    serialized_user = UserSerializer(user).data
    # https://stackoverflow.com/questions/31237042/whats-the-difference-between-select-related-and-prefetch-related-in-django-orm

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)
    response.data = {
        "access_token": access_token,
        "user": serialized_user,
    }

    return response



# class ForgotPasswordView(APIView):
#     permission_classes = [
#         AllowAny,
#     ]

#     def post(self, request):
#         email = request.data.get("email")
#         tenant = request.data.get("tenant")
#         if User.objects.get(email=email, tenant=tenant).exists():
#             user = User.objects.get(email=email, tenant=tenant)
#             reset_token = user.token
#             subject = f"Password Reset Request from {user}"
#             message = f"""
#             Hey there,
#             Please reset your password by clicking on the link below: https://*.gradvine.com/reset-password/{reset_token}
#             Regards,
#             Team Level
#             """
#             send_mail(
#                 subject,
#                 message,
#                 "team@level.so",
#                 [email],
#                 fail_silently=False,
#             )
#             return Response({"message": "success"}, status=200)
#         else:
#             return Response({"message": "success"}, status=200)


"""
class ResetPasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        token = request.data.get("token")
        password = request.data.get("password")
        try:
            user = User.objects.get(token=token)
            user.set_password(password)
            user.save()
            return Response({"message": "success"}, status=200)
        except Exception as e:
            print(e)
            return Response({"message": "failed"}, status=400)

"""