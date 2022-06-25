from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
    TokenObtainSlidingView, TokenRefreshSlidingView
)




urlpatterns = [
    path('', views.getRoutes),
    path('vacancy/', views.getVacancy),
    path('resume/', views.getResume),
    path('onevacancy/<str:id>', views.VacancyAPIView.as_view(), name='onevacancy'),
    path('oneresume/<str:id>', views.ResumeAPIView.as_view(), name='oneresume'),
    path('deletevacancy/<str:id>', views.VacancyAPIView.as_view(), name='delete'),
    path('addvacancy/', views.addVacancy, name='vacancy'),
    path('addresume/', views.ResumeAPIView.as_view(), name='resume'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/ver/', TokenRefreshSlidingView.as_view(), name='token_verify'),
    path('token/verifi/', TokenObtainSlidingView.as_view(), name='token_verify'),
    path('token/Verify/', views.verify_token, name='token_verify'),
    path('login/', views.login_user, name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
]