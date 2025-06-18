from rest_framework import generics
from .models import Contest
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from permissions import IsOwnerOrAdmin
from .serializers import ContestListSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

class ContestsCreateAPIView(generics.CreateAPIView):
    queryset = Contest.objects.all()
    # serializer_class = ContestCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class ContestsListAPIVIEW(generics.ListAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class ContestsDetailAPIView(generics.RetrieveAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestListSerializer

class ContestsDeleteAPIView(generics.DestroyAPIView):
    queryset = Contest.objects.all()
    # serializer_class = PostSerializer
    permission_classes = [IsOwnerOrAdmin]
    authentication_classes = [JWTAuthentication]
    