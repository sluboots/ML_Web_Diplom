from django.shortcuts import render, redirect
from .models import Resume, Vacancy
from django .views.generic import ListView, CreateView
from django.contrib.auth import login, logout
from .forms import UserRegisterForm, UserLoginForm, VacancyForm, ResumeForm
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .getcluster import get_cluster

from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework.decorators import api_view
from .serializers import VacancyListSerailizer, ResumeListSerailizer, UserSerializer, MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)




class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerailizer
    permission_classes = [IsAuthenticated]
# class VacancyList(generics.GenericAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#     queryset = Vacancy.objects.all().order_by('created_at')
#     serializer_class = VacancyListSerailizer
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
# class VacancyDetail(generics.RetrieveDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#     queryset = Vacancy.objects.all()
#     serializer_class = VacancyListSerailizer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all().order_by()
    serializer_class = ResumeListSerailizer
    permission_classes = [IsAuthenticated]


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


def user_logout(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm
    return render(request, 'ML/register.html', {"form": form})

def user_login(request):
 if request.method == "POST":
     form = UserLoginForm(data=request.POST)
     if form.is_valid():
         user = form.get_user()
         login(request, user)
         return redirect('home')
 else:
     form = UserLoginForm()
 return render(request, 'ML/login.html', {'form': form})


def view_user_vacancy(request):
    vacancy = Vacancy.objects.all()
    context = {'vacancy': vacancy}
    return render(request, 'ML/view_user_vacancy.html', context)

def view_user_resume(request):
    resume = Resume.objects.all()
    context = {'resume': resume}
    return render(request, 'ML/view_user_resume.html', context)

@login_required(login_url='login')
def FindResume(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = profile
            post.created_at = timezone.now()
            post.cluster = get_cluster(post.vacancy)
            post.save()
            return redirect('home')
    else:
        form = ResumeForm()
    return render(request, 'ML/find_resume.html', {'form': form})

@login_required(login_url='login')
def FindVacancy(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = profile
            post.created_at = timezone.now()
            post.cluster = get_cluster(post.resume)
            post.save()
            return redirect('home')
    else:
        form = VacancyForm()
    return render(request, 'ML/find_vacancy.html', {'form': form})

'''class FindVacany(LoginRequiredMixin, CreateView):

    form_class = VacancyForm
    template_name = 'ML/find_vacancy.html'
    raise_exception = True

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(FindVacany, self).form_valid(form)'''

def index(requests):
    return render(requests, 'ML/index.html')


# Create your views here.
