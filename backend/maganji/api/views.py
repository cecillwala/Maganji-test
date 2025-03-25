from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.utils import IntegrityError
from django.middleware.csrf import get_token
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt

from .models import *
# Create your views here.

@api_view(['GET','POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == "POST":
        print(request.data)
        user = authenticate(
            request,
            username=request.data.get("phoneNo"),
            password=request.data.get("password")
        )
        if user is not None:
            login(request, user)
            return Response({"message":"Login successful"}, status=200)
        elif user is None:
            return Response({"message":"Invalid password/username"}, status=401)
    logout(request)
    return Response({"message":"login"}, status=200)


@api_view(['GET','POST'])
@permission_classes([AllowAny])
def signup_view(request):
    if request.method == "POST":  
            print(request.data)
            try:
                user = User.objects.create(
                    first_name=request.data.get("firstName").strip(),
                    last_name=request.data.get("lastName").strip(),
                    phone_no=request.data.get("phoneNo"),
                    national_id=request.data.get("nationalID"),
                    email = request.data.get("email")
                )
                user.set_password(f'{request.data.get("password")}')
                user.save()
                login(request, user)
                return Response({"message":"Registration successful"}, status=200)
            except IntegrityError:
                return Response({"message":"User already exists"}, status=401)
    return Response({"message":"signup"}, status=200)
