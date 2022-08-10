from rest_framework import serializers
from codify.models import Language, Topic, Subtopic, Snipped
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

class SubtopicSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Subtopic
        fields = ['id', 'name']

class TopicSerializer(serializers.ModelSerializer):
    subtopics = SubtopicSerializer(many=True, read_only=True)
    class Meta:
        model =  Topic
        fields = ['id', 'name', 'subtopics']
        read_only_fields = ['id']

class LanguageSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(many=True, read_only=True)
    class Meta:
        model = Language
        fields = ['id','name','topic']
        read_only_fields = ['id']


class GetLanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id','name',]
        read_only_fields = ['id']

class GetSubTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtopic
        fields = ['id','name',]
        read_only_fields = ['id']



class SnippedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Snipped
        exclude = ['user']
        depth =1

class SnippedSerializerPost(serializers.ModelSerializer):

    class Meta:
        model = Snipped
        exclude = ['user','language','topic','subtopic']






