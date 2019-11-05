from django.shortcuts import render

# Create your views here.
from rest_framework import status, routers, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from apap.models import *
from django.core.files import File
import base64


class AuthView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'name': 'hihihihihihihih'}
        return Response(content)


class RegisterView(APIView):
    permission_classes = (AllowAny, )
    def post(self, request):
        data = request.POST
        print('hifbdsakfiudsgfkidsgcbi')
        name = data['name']
        email = data['email']
        password = data['password']
        user = User.objects.create_user(email=email, username=email, password=password)
        Profile.objects.create(user=user, name=name)
        return Response(status=status.HTTP_201_CREATED)


class DoggoSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField('get_photo_url')
    owner_name = serializers.SerializerMethodField('get_owner_name')
    photo_b64 = serializers.SerializerMethodField('get_photo')

    class Meta:
        model = Doggo
        fields = ['name', 'details', 'photo_url', 'gender', 'owner_name', 'photo_b64']

    def get_photo_url(self, obj):
        return obj.photo.url

    def get_owner_name(self, obj):
        return obj.owner.profile.name

    def get_photo(self, obj):
        f = open(obj.photo.path, 'rb')
        image = File(f)
        data = base64.b64encode(image.read())
        f.close()
        return data


@api_view(['GET', 'POST', ])
#@login_required
def get_doggo(request):
    if request.method == 'GET':
        doggos = Doggo.objects.all()

    if request.method == 'POST':
        data = request.POST
        if 'gender' in data:
            gender = int(data['gender'])
        doggos = Doggo.objects.filter(gender=gender)

    serializer = DoggoSerializer(doggos, many=True)
    return Response(serializer.data)


@api_view(['POST', ])
def post_doggo(request):
    user = request.user
    data = request.POST
    name = data['name']
    gender = data['gender']
    detail = data['detail']
    photo = request['photo']
    Doggo.objects.create(name=name, details=detail, gender=gender, owner=user, photo=photo)
    pass
