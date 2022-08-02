from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.serializers import EmailSerializer, TokenSerializer

from .models import User


@api_view(['POST'])
def send_confirmation_code(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    email = serializer.validated_data['email']
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username'],
        email=email
    )
    print(user.id)
    confirmation_code = default_token_generator.make_token(user)
    User.objects.filter(id=user.id).update(
        confirmation_code=make_password(
            confirmation_code, salt=None, hasher='default'
        )
    )
    send_mail(
        'Ваш код подтверждения для Yamdb',
        f'Ваш код подтверждения {confirmation_code}',
        'yamdb@yamdb.com',
        [email],
        fail_silently=False,
    )
    return Response(
        serializer.data, status=status.HTTP_200_OK
    )


@api_view(['POST'])
def send_auth_token(request):

    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.data.get('username')
    )
    confirmation_code = serializer.data.get('confirmation_code')
    if default_token_generator.check_token(user, confirmation_code):
        token = str(AccessToken.for_user(user))
        return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
    return Response({'confirmation_code': 'Неверный код'},
                    status=status.HTTP_400_BAD_REQUEST)