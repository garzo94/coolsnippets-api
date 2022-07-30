from rest_framework import serializers
from codify.models import Language, Topic, Subtopic, Snipped, Twitter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

class SubtopicSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Subtopic
        fields = "__all__"

class TopicSerializer(serializers.ModelSerializer):
    subtopics = SubtopicSerializer(many=True, read_only=True)
    class Meta:
        model =  Topic
        fields = ['id', 'name','subtopics']
        read_only_fields = ['id']

class LanguageSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    class Meta:
        model = Language
        fields = ['id','name','topics']
        read_only_fields = ['id']

