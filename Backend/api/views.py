from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework import generics
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from MLSite.forms import ResumeForm
from .serializers import VacancyListSerailizer, ResumeListSerailizer
from MLSite.models import Vacancy, Resume
from user.models import Profile
from MLSite import getcluster
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    parser_classes = [FormParser, MultiPartParser, JSONParser]



class VacancyAPIView(APIView):
    serializer_class = VacancyListSerailizer
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    def get_queryset(self):
        vacancy = Vacancy.objects.all()
        return vacancy


    def get(self, requset, id):
        project = Vacancy.objects.get(id=id)
        array_data, clusters, labels = getcluster.get_cluster1(project.resume)
        links = getcluster.get_link(array_data, clusters, labels)
        serializer = VacancyListSerailizer(project, many=False)
        print(serializer)
        return JsonResponse({'data':serializer.data,'links': links})


    def post(self, request):
        profile = request.user.profile
        print(profile)
        data = request.data
        new_vacancy = Vacancy.objects.create(cluster=1, resume=data.get('resume'), created_at=timezone.now())
        new_vacancy.save()
        serializer = VacancyListSerailizer(new_vacancy)
        return Response(serializer.data)

    def delete(self, request, id):
        project = Vacancy.objects.get(id=id)
        project.delete()
        return JsonResponse({'message': 'Deleted'})



class ResumeAPIView(APIView):
    serializer_class = ResumeListSerailizer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        resume = Resume.objects.all()
        return resume

    def get(self, requset, id):
        project = Resume.objects.get(id=id)
        array_data, clusters, labels = getcluster.get_cluster1(project.vacancy)
        links = getcluster.get_link(array_data, clusters, labels)
        serializer = VacancyListSerailizer(project, many=False)
        print(serializer)
        return JsonResponse({'data': serializer.data, 'links': links})

    def post(self, request):
        profile = request.user.profile
        data = request.data
        new_resume = Resume.objects.create(cluster=1, vacancy=data.get('vacancy'), created_at=timezone.now(), owner=profile)
        new_resume.save()
        serializer = ResumeListSerailizer(new_resume)
        return Response(serializer.data)

    def delete(self, request, id):
        project = Resume.objects.get(id=id)
        project.delete()
        return JsonResponse({'message': 'Deleted'})

    def put(self, request, id):
        data = request.data
        project = Resume.objects.get(id=id)


@parser_classes([FormParser, MultiPartParser, JSONParser])
@api_view(['POST'])
def login_user(request):
    data = request.data
    user = authenticate(request, username=data.get('username'), password=data.get('password'))
    print(user.username)
    print(user.email)
    if user is not None:
        if user.is_active:
            print(1)
            login(request, user)
            return HttpResponse('Authenticated successfully')


@api_view(['GET', 'POST'])
def getRoutes(request):
    routes = [
        {'GET': 'api/projects'},
        {'GET': 'api/projects/id'},

        {'POST': 'api/users/token'},
        {'POST': 'api/users/token/refresh'},
        {'POST': 'api/'}
    ]

    return Response(routes)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getVacancy(request):
    vacancy = Vacancy.objects.all()
    profile = request.user.profile
    print(profile)
    vacancy1 = profile.vacancy_set.all()
    print(vacancy1)
    serializer = VacancyListSerailizer(vacancy1, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addVacancy(request):
    profile = request.user.profile
    print(profile)
    data = request.data
    new_vacancy = Vacancy.objects.create(cluster=1,
                                         resume=data.get('resume'), created_at=timezone.now(), owner=profile)
    new_vacancy.save()
    serializer = VacancyListSerailizer(new_vacancy)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addResume(request):
    profile = request.user.profile
    print(profile)
    data = request.data
    new_vacancy = Resume.objects.create(cluster=1, vacancy=data.get('vacancy'), created_at=timezone.now(), owner=profile)
    new_vacancy.save()
    serializer = VacancyListSerailizer(new_vacancy)
    return Response(serializer.data)


'''@permission_classes([IsAuthenticated])'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getResume(request):
    projects = Resume.objects.all()
    serializer = ResumeListSerailizer(projects, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def verify_token(request):
    print(request.data.get('token'))
    print('--------------------------------')
    data = {'token': request.data.get('token')}


