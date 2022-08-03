from django.urls import path, include

# from watchlist_app.api import views #importing views from api folder
from codify.views import language, topic, subtopic, SnippetRead, SnippetPost, SnippetUpdateDelete, TwitterData

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

urlpatterns=[
    path('language/', language, name='language'),
    path('topic/<int:pk>/',topic, name='topic' ),
    path('subtopic/<int:pkLanguage>/<int:pkTopic>/',subtopic, name='subtopic' ),
    path('snippet-list/', SnippetRead.as_view(), name='snippet'),
    path('snippet/<int:pkLanguage>/<int:pkTopic>/<int:pkSubtopic>/', SnippetPost.as_view(), name='snippet'),
    path('snippet-updatedelete/<int:pk>/', SnippetUpdateDelete.as_view(), name='snippet'),
    path('twitter-data/', TwitterData.as_view(), name='twitter'),

    ]
# router.register('language-topic-subtopic', LanguageTopicSubtopicMV, basename='language-topic-subtopic')



# urlpatterns = router.urls