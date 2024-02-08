from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import Site, Collector , Contact
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication
from .serializers import SiteSerializer, CollectorSerializer, ContactSerializer

# Create your views here.

class SiteCreateView(APIView):
    """
    View to create a new Site instance.
    """
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated,]

    def post(self, request, format=None):
        serializer = SiteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CollectorListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Collector.objects.all()

    def get(self, request, format=None):
        collectors = self.get_queryset()
        serializer = CollectorSerializer(collectors, many=True)
        return Response(serializer.data)

class ContactListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Contact.objects.all()
    
    def get(self, request, format=None):
        contacts = self.get_queryset()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)