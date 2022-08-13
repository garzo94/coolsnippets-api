
from django.forms import ValidationError
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from codify.models import Language, Topic, Subtopic, Snipped
from codify.serializers import LanguageSerializer, TopicSerializer, SubtopicSerializer, SnippedSerializer, SnippedSerializerPost, GetLanguagesSerializer, GetSubTopicSerializer
from rest_framework import  permissions, status
from rest_framework.views import APIView
from codify.permissions import IsOwnerPermissions
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination


###### Get and Post programing Language #######
@api_view(['GET', 'POST'])
@permission_classes([IsOwnerPermissions,])
def language(request):

    if request.method == 'GET':

        languages = Language.objects.filter(user=request.user)
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data)



    if request.method == 'POST':
        #making user language name is Capitalized ########
        if  not isinstance(request.data, dict) :
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
        if  not isinstance(request.data, dict) :
            request.data._mutable = True
            request.data['name'] = request.data['name'].capitalize()
            request.data._mutable = False
        ###########

        lang = get_object_or_404(Language, pk=pk, user=request.user)
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
          #### making suer topic is capitalized
        if  not isinstance(request.data, dict) :
            request.data._mutable = True
            request.data['name'] = request.data['name'].capitalize()
            request.data._mutable = False
        ###########
        lang = Language.objects.get(id=pkLanguage, user=request.user)
        topic = get_object_or_404(Topic,id=pkTopic, language=lang)
        serializer = SubtopicSerializer(data=request.data)
        print(lang)

        if serializer.is_valid():
            serializer.save(topic=topic)#aditional data comes from models
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

### read snippets ###

class SnippetRead(APIView,PageNumberPagination):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pkLanguage=None, pkTopic=None, pkSubtopic=None):

        if pkSubtopic is not None and pkTopic is not None:
            lang = Language.objects.get(user=request.user, pk=pkLanguage)
            top = Topic.objects.get(language=lang, pk=pkTopic)
            sub = Subtopic.objects.get(topic=top,pk=pkSubtopic)
            snippets = Snipped.objects.filter(user=request.user.id, language=lang, topic=top, subtopic=sub)#.id if error  'id' expected a number but got <django.contrib.auth.models.AnonymousUser object at 0x048C7E90>
            results = self.paginate_queryset(snippets,request,view=self)
            serializer = SnippedSerializer(results, many=True)
            return Response(serializer.data)

        if pkTopic is not None:
            lang = Language.objects.get(user=request.user, pk=pkLanguage)
            top = Topic.objects.get(language=lang, pk=pkTopic)
            snippets = Snipped.objects.filter(user=request.user.id, language=lang, topic=top)#.id if error  'id' expected a number but got <django.contrib.auth.models.AnonymousUser object at 0x048C7E90>
            results = self.paginate_queryset(snippets,request,view=self)
            serializer = SnippedSerializer(results, many=True)
            return Response(serializer.data)

        if pkLanguage == 'all':
            print('heeeeeeey')
            snippets = Snipped.objects.filter(user=request.user.id)#.id if error  'id' expected a number but got <django.contrib.auth.models.AnonymousUser object at 0x048C7E90>
            results = self.paginate_queryset(snippets,request,view=self)
            serializer = SnippedSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)
        elif pkLanguage != 'all':
            lang = Language.objects.get(user=request.user, pk=pkLanguage)
            snippets = Snipped.objects.filter(user=request.user.id, language=lang)#.id if error  'id' expected a number but got <django.contrib.auth.models.AnonymousUser object at 0x048C7E90>
            results = self.paginate_queryset(snippets,request,view=self)
            serializer = SnippedSerializer(results, many=True)
            return Response(serializer.data)



### create snippets ###
class SnippetPost(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pkLanguage, pkTopic=None, pkSubtopic=None):

        serializer = SnippedSerializerPost(data=request.data)
        language = Language.objects.get(user= request.user, id = pkLanguage) # to do this I have to check my models fields


        if pkSubtopic is not None:
            topic = Topic.objects.get(language=language, id=pkTopic)
            subtopic = Subtopic.objects.get(topic=topic, id=pkSubtopic)
            if serializer.is_valid():
                serializer.save(user = request.user, language =language, topic=topic, subtopic=subtopic)
                return Response(serializer.data)
        if pkTopic is not None:
            topic = Topic.objects.get(language=language, id=pkTopic)
            if serializer.is_valid():
                serializer.save(user = request.user, language =language, topic=topic,)
                return Response(serializer.data)


        elif serializer.is_valid():
            print(request.data,'mi dataaaaa')
            serializer.save(user = request.user, language =language)
            return Response(serializer.data)
        else:
            print(serializer, 'serializeeeer')
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetUpdateDelete(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request,pk,pkLang=None,pkTop=None,pkSubt=None):
        snippet = Snipped.objects.get(pk=pk, user=request.user)

        if pkLang is not None and pkTop is not None and pkSubt is not None:
            language = Language.objects.get(pk=pkLang, user=request.user)
            topic = Topic.objects.get(pk=pkTop, language=language)
            subtopic = Subtopic.objects.get(pk=pkSubt, subtopic=subtopic)

            serializer = SnippedSerializer(snippet,data=request.data, language=language, topic=topic, subtopic=subtopic, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)

        if pkLang is not None and pkTop is not None:
            language = Language.objects.get(pk=pkLang, user=request.user)
            topic = Topic.objects.get(pk=pkTop, language=language)

            serializer = SnippedSerializer(snippet,data=request.data, language=language, topic=topic,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)

        if pkLang is not None:
            language = Language.objects.get(pk=pkLang, user=request.user)
            serializer = SnippedSerializer(snippet,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save(language=language)
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


class GetLanguages(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):

            languages = Language.objects.filter(user=request.user)
            serializer = GetLanguagesSerializer(languages, many=True)


            return Response(serializer.data)
class GetSubtopics(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,language,topic):

            language = Language.objects.get(user=request.user.id, id=language)
            topic = Topic.objects.get(language=language,id=topic)
            subtopic = Subtopic.objects.filter(topic=topic)
            serializer = GetSubTopicSerializer(subtopic, many=True)


            return Response(serializer.data)

class GetSnnipet(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,pk):
            snnipet = Snipped.objects.get(user=request.user.id, pk=pk)
            serializer = SnippedSerializer(snnipet, many=False)
            return Response(serializer.data)

















