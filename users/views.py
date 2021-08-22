from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST)
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdminOrDenied, PutNotAllowed
from .serializers import (AdminSerializer, EmailConfirmationCodeSerializer,
                          EmailSerializer, UserSerializer)

User = get_user_model()


class CustomViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrDenied, PutNotAllowed]
    queryset = User.objects.all()
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['username', ]

    def get_serializer_class(self):
        if self.request.user.is_staff or self.request.user.is_admin:
            return AdminSerializer
        return UserSerializer

    @action(methods=['GET', 'PATCH'], detail=False,
            permission_classes=[permissions.IsAuthenticated],
            url_path='me', url_name='users_me')
    def get_update_user(self, request):
        user = get_object_or_404(User, email=request.user.email)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def generate_code(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username_from_email = email.split('@')[0]
    # We don't set username as required field in User model
    # but Users API use username lookup. Better assign
    # to part of email, later users can change it if necessary
    user = User.objects.get_or_create(email=email)[0]
    if user.username is None:
        user.username = username_from_email
        user.save()
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Confirmation code',
        f'Confirmation code for your account: {confirmation_code}',
        EMAIL_HOST_USER,
        [user.email]
    )
    return Response(status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = EmailConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data['email']
    user = User.objects.get(email=email)
    token = RefreshToken.for_user(user).access_token
    return Response({'token': str(token)}, status=HTTP_201_CREATED)
