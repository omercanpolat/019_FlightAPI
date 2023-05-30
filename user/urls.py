from django.urls import path, include
from .views import RegisterView

# '/user/':
urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('register/', RegisterView.as_view()),
]

# ---------- Router ----------
from rest_framework.routers import DefaultRouter
from .views import UserCreateView, UserView
router = DefaultRouter()
router.register('create', UserCreateView) # permissions.AllowAny
router.register('', UserView) # permissions.IsAdminUser
urlpatterns += router.urls