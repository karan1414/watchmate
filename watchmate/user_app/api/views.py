from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user_app import models
from user_app.api.serializers import UserRegistrationSerializer

# from rest_framework_simplejwt.tokens import RefreshToken



@api_view(["POST",])
def logout_view(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(["POST",])
def registration_view(request):

    if request.method == "POST":
        serializer = UserRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()

            data['response'] = "Registration successful !"
            data['username'] = user.username
            data['email'] = user.email

            token = Token.objects.get(user=user).key
            data['token'] = token
            # refresh = RefreshToken.for_user(user)
            # data['token'] = {
            #     "refresh": str(refresh),
            #     "access": str(refresh.access_token),
            # }
        else:
            data = serializer.errors
        return Response(data)
        
