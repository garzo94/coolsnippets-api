from ast import Is
from django.forms import ValidationError
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from codify.models import Language, Topic, Subtopic, Snipped, Twitter
from codify.serializers import LanguageSerializer, TopicSerializer, SubtopicSerializer
from rest_framework import viewsets, permissions, filters
from codify.permissions import IsOwnerPermissions


###### Get and Post programing Language #######
@api_view(['GET', 'POST'])
@permission_classes([IsOwnerPermissions,])
def language(request,):

    if request.method == 'GET':

        languages = Language.objects.filter(user=request.user)
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data)



    if request.method == 'POST':

        serializer = LanguageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
###### Post a topic related to user programing language #####
@api_view(['POST'])
@permission_classes([IsOwnerPermissions,])
def topic(request,pk):

    if request.method == 'POST':
        lang = Language.objects.filter(id=pk, user=request.user)
        serializer = TopicSerializer(data=request.data)
        print(lang.values())

        if serializer.is_valid():
            serializer.save(language=lang)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# class LanguageTopicSubtopicMV(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = LanguageSerializer
#     queryset =  Language.objects.all()

#     def get_queryset(self): #return categories that belogn to the current login user
#         return self.request.user.language.all()

#     def perform_create(self, serializer): #when a categorie is created we are adding created_by = the current user
#         serializer.save(user=self.request.user)



