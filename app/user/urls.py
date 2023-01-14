from rest_framework.routers import DefaultRouter
from django.urls import path, include
from user import views

router = DefaultRouter()
router.register("users/lastplayed", views.UserPlaySessionViewSet)
router.register("users", views.UserViewSet)

app_name = "user"

urlpatterns = [
    path('', include(router.urls)),
    path('token/', views.CreateTokenView.as_view(), name='token')
]
