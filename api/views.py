import uuid

from django.conf import settings as conf_settings
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets, filters, mixins
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitlesFilter
from .models import Category, Review, User, Title, Genre
from .permissions import (UserAdministrator,
                          UserAdministratorOrReadOnly,
                          OwnerAdministratorOrModeratorOrReadOnly)
from .serializers import (ReviewSerializer, CommentSerializer,
                          UserSerializer, CategorySerializer,
                          TitleReadOperationsSerializer,
                          TitleWriteOperationsSerializer,
                          GenreSerializer, UserCreationSerializer,
                          UserTokenSerializer)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          OwnerAdministratorOrModeratorOrReadOnly]

    def get_queryset(self):
        """Getting a query of comments of a review via related_name.
        Or of an exact comment, if comment_id is provided"""
        review_id = self.kwargs.get('review_id')
        title = self.kwargs.get('title_id')
        review = get_object_or_404(Review, pk=review_id, title=title)

        return review.comments.all()

    def perform_create(self, serializer):
        """Added author saving for comment creation via API """
        title = self.kwargs.get('title_id')
        review_id = get_object_or_404(Review, pk=self.kwargs.get(
            'review_id'), title=title)

        serializer.save(author=self.request.user,
                        review_id=review_id)


class ReviewViewSet(viewsets.ModelViewSet):
    """A slightly modified ViewSet for Review model"""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          OwnerAdministratorOrModeratorOrReadOnly]
    queryset = Review.objects.all()

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return Review.objects.filter(title=title).all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    serializer = UserCreationSerializer(data=request.POST)
    serializer.is_valid(raise_exception=True)
    user_email = serializer.validated_data['email']
    confirmation_code = uuid.uuid4().hex

    user, _ = User.objects.get_or_create(email=user_email)
    user.username = user_email
    user.confirmation_code = confirmation_code
    user.save()

    send_mail(
        conf_settings.MESSAGE_THEME,
        f'Your activation code is {confirmation_code}',
        conf_settings.MESSAGE_SENDER,
        [user_email],
        fail_silently=False
    )

    return Response(
        {'response': 'We send you email with confirmation code'},
        status=status.HTTP_201_CREATED,
        content_type='application/json'
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = UserTokenSerializer(data=request.POST)
    serializer.is_valid(raise_exception=True)
    user_email = serializer.validated_data['email']
    confirmation_code = serializer.validated_data['confirmation_code']

    try:
        user = User.objects.get(
            username=user_email,
            confirmation_code=confirmation_code
        )
    except(User.DoesNotExist):
        user = None

    if user is None:
        response_text = 'User with this email and confirmation code not found'
        return Response({'response': response_text, 'token': ''},
                        status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json'
                        )

    user.save()

    refresh = RefreshToken.for_user(user)
    return Response({'response': '', 'token': str(refresh.access_token)},
                    status=status.HTTP_200_OK,
                    content_type='application/json'
                    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserAdministrator]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'

    @action(detail=False, permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @me.mapping.patch
    def patch_me(self, request):
        serializer = self.serializer_class(
            request.user, request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly,
                          UserAdministratorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly,
                          UserAdministratorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(Avg('review__score'))
    filter_class = TitlesFilter
    permission_classes = [IsAuthenticatedOrReadOnly,
                          UserAdministratorOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleReadOperationsSerializer
        return TitleWriteOperationsSerializer
