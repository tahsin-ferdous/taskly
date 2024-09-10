from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponse
from rest_framework import viewsets
from . models import UserAccount
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny


from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from . serializers import UserAccountSerializer, UserLoginSerializer, UserRegistrationSerializer, AllUserSerializer
# Create your views here.


class UserAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [AllowAny] 
    
class UserRegistrationSerializerViewSet(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny] 
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.is_active = True
            user.save()

            return Response({'message': 'User registered successfully'})
        return Response(serializer.errors)

class UserLoginApiView(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        serializer = UserLoginSerializer(data=self.request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                print(token, _)
                login(request, user)
                return Response({'token': token.key, 'user_id' : user.id})
            else:
                return Response({'error': 'Invalid Credentials'})
        return Response(serializer.errors)
    
class UserLogoutApiView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny] 
    def get(self, request):
        if request.user.auth_token:
            request.user.auth_token.delete()
        logout(request)
        return redirect('login')

class AllUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AllUserSerializer
    permission_classes = [AllowAny] 