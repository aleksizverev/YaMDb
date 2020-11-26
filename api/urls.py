from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (ReviewViewSet, create_user, get_token, UserViewSet,
                    CategoryViewSet, GenreViewSet,
                    TitleViewSet, CommentViewSet)

router = DefaultRouter()
router.register(r'^titles/(?P<title_id>[^/.]+)/reviews',
                ReviewViewSet, basename='reviews')

router.register(r'users', UserViewSet, basename='username')
router.register('genres', GenreViewSet, 'genres')
router.register('titles', TitleViewSet, 'titles')
router.register(r'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>['
                '^/.]+)/comments',
                CommentViewSet, basename='comments')
router.register('categories', CategoryViewSet, basename='categories')

auth_urlpatterns = [
    path('email/', create_user, name='create_user'),
    path('token/', get_token, name='get_token'),
]

urlpatterns = [
    path('v1/auth/', include(auth_urlpatterns)),
    path('v1/', include((router.urls, 'api'))),
]
