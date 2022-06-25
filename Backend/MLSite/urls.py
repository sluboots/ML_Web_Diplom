from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import *


router = routers.DefaultRouter()
router.register(r'vacancy', VacancyViewSet)
router.register(r'resume', ResumeViewSet)
router.register(r'users', UserViewSet)


urlpatterns = [
    #path('', views.index, name='index'),
    path('', index, name='home'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('find_vacancy/', FindVacancy, name='find_vacancy'),
    path('find_resume/', FindResume, name='find_resume'),
    path('view_all_vacancy/', view_user_vacancy, name='view_vacancy'),
    path('view_all_resume/', view_user_resume, name='view_resume'),
    path('apii/', include(router.urls)),
    # path('vacancy/', VacancyList.as_view()),
    # path('vacancy/<int:pk>/', VacancyDetail.as_view()),
    # path('users/', UserList.as_view()),
    # path('users/<int:pk>/', UserDetail.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('newlogin/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('newlogin/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('newregister/', RegisterView.as_view(), name='auth_register'),
    path('logou/', LogoutView.as_view(), name='auth-logout'),

]