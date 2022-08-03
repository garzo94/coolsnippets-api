from ast import Is, Sub
from django.forms import ValidationError
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from codify.models import Language, Topic, Subtopic, Snipped, Twitter
from codify.serializers import LanguageSerializer, TopicSerializer, SubtopicSerializer, SnippedSerializer, SnippedSerializerPost, TwitterSerializer
from rest_framework import generics, permissions,mixins, status, filters, authentication
from rest_framework.views import APIView
from codify.permissions import IsOwnerPermissions
from codify.custome_renderes import JPEGRenderer, PNGRenderer


###### Get and Post programing Language #######
@api_view(['GET', 'POST'])
@permission_classes([IsOwnerPermissions,])
def language(request,):

    if request.method == 'GET':

        languages = Language.objects.filter(user=request.user)
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data)



    if request.method == 'POST':
        #making user language name is Capitalized ########
        request.data._mutable = True
        request.data['name'] = request.data['name'].capitalize()
        request.data._mutable = False
        ###########
        serializer = LanguageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)#asociando prgraming language al usuario, user viene de mi data en models
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
###### create a topic related to programing language of user #####
@api_view(['POST'])
@permission_classes([IsOwnerPermissions,])
def topic(request,pk):

    if request.method == 'POST':
        #### making suer topic is capitalized
        request.data._mutable = True
        request.data['name'] = request.data['name'].capitalize()
        request.data._mutable = False
        ###########
        lang = Language.objects.get(id=pk, user=request.user)
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(language=lang)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    ###### Post a subtopic related to programing language of user #####
@api_view(['POST'])
@permission_classes([IsOwnerPermissions,])
def subtopic(request,pkLanguage, pkTopic):

    if request.method == 'POST':
         #### making suer sustopic is capitalized
        request.data._mutable = True
        request.data['name'] = request.data['name'].capitalize()
        request.data._mutable = False
        ###########
        lang = Language.objects.get(id=pkLanguage, user=request.user)
        topic = Topic.objects.get(id=pkTopic, language=lang)
        serializer = SubtopicSerializer(data=request.data)
        print(lang)

        if serializer.is_valid():
            serializer.save(topic=topic)#aditional data comes from models
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

### read snippets ###

class SnippetRead(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        snippets = Snipped.objects.filter(user=request.user.id)#.id if error  'id' expected a number but got <django.contrib.auth.models.AnonymousUser object at 0x048C7E90>
        serializer = SnippedSerializer(snippets, many=True)

        return Response(serializer.data)

### create snippets ###
class SnippetPost(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pkLanguage, pkTopic, pkSubtopic):
        print(request.data, 'mi pinche data')
        serializer = SnippedSerializerPost(data=request.data)
        language = Language.objects.get(user= request.user, id = pkLanguage) # to do this I have to check my models fields
        topic = Topic.objects.get(language=language, id=pkTopic)
        subtopic = Subtopic.objects.get(topic=topic, id=pkSubtopic)
        if serializer.is_valid():
            serializer.save(user = request.user, language =language, topic=topic, subtopic=subtopic)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class SnippetUpdateDelete(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request,pk):
        snippet = Snipped.objects.get(pk=pk, user=request.user)
        serializer = SnippedSerializer(snippet,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    def delete(self, request, pk):
        snippet = Snipped.objects.filter(pk=pk, user=request.user)
        if snippet.exists():
            snippet.delete()
            return Response({'status':'Snipet succesfully deleted!'})
        else:
            return Response({'status':'Snippet does not exists.'})

class SnippetGetImage(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes =[JPEGRenderer]

    def get(self, request,pk):
        renderer_classes =[JPEGRenderer]
        queryset = Snipped.objects.get(id=pk,user=request.user).image
        return Response(queryset,content_type='image/jpg')


class TwitterData(APIView):
     permission_classes = [permissions.IsAuthenticated]
     def get(self,request):
        try:
         twitter = Twitter.objects.get(user=request.user)
         serializer = TwitterSerializer(twitter)
         return Response(serializer.data)
        except:
            return Response(status.HTTP_404_NOT_FOUND)

     def post(self, request):
        data = request.data

        serializer = TwitterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
     def put(self, request):
        twitter = Twitter.objects.get(user=request.user)
        serializer = TwitterSerializer(twitter,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)






