from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('account', views.UserAccountViewSet)
router.register('allUser', views.AllUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.UserRegistrationSerializerViewSet.as_view(), name='register'),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('logout/', views.UserLogoutApiView.as_view(), name='logout'),
]
