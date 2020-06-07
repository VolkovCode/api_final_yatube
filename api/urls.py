from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FollowViewSet, GroupViewSet
from rest_framework.authtoken import views
    
router = DefaultRouter()
router.register('posts', PostViewSet, basename="posts")
router.register(r"posts/(?P<post_id>\d+)/comments", CommentViewSet, basename="comments") 
router.register("follow", FollowViewSet, basename="follow")
router.register("group", GroupViewSet, basename="group") 

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
