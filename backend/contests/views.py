from rest_framework import generics
from .models import Contest, Participation
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from permissions import IsOwnerOrAdmin
from .serializers import ContestListSerializer, ContestSignupSerializer
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

class ContestSignupAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, pk):
        contest = get_object_or_404(Contest, pk=pk)
        serializer = ContestSignupSerializer(data={}, context={'contest': contest, 'request': request})
        
        if serializer.is_valid():
            # Create participation
            Participation.objects.create(contest=contest, user=request.user)
            return Response({
                'message': 'ثبت نام در مسابقه با موفقیت انجام شد'
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    