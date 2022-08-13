from django.urls import path


# from watchlist_app.api import views #importing views from api folder
from codify.views import language, topic, subtopic, SnippetRead, SnippetPost, SnippetUpdateDelete, GetLanguages,GetSubtopics,GetSnnipet

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

urlpatterns=[
    path('language/', language, name='language'),
    path('topic/<int:pk>/',topic, name='topic' ),
    path('subtopic/<int:pkLanguage>/<int:pkTopic>/',subtopic, name='subtopic' ),
    ### get snippet filter list
    path('snippet-list/<str:pkLanguage>/', SnippetRead.as_view(), name='snippets-get'),
    path('snippet-list/<str:pkLanguage>/<str:pkTopic>/', SnippetRead.as_view(), name='snippets-get'),
    path('snippet-list/<str:pkLanguage>/<str:pkTopic>/<str:pkSubtopic>/', SnippetRead.as_view(), name='snippets-get'),
    #### get subtopics
    path('get-subtopics/<str:language>/<str:topic>/', GetSubtopics.as_view(), name='subtopic-get'),
    #### get one Snipet
    path('get-snippet/<int:pk>/', GetSnnipet.as_view(), name='subtopic-get'),
    #### create-Snipeet
    path('snippet/<int:pkLanguage>/<int:pkTopic>/<int:pkSubtopic>/', SnippetPost.as_view(), name='snippet-create'),
    path('snippet/<int:pkLanguage>/<int:pkTopic>/', SnippetPost.as_view(), name='snippet-create'),
    path('snippet/<int:pkLanguage>/', SnippetPost.as_view(), name='snippet-create'),
    ### Update-delete
    path('snippet-updatedelete/<int:pk>/', SnippetUpdateDelete.as_view(), name='snippet-delete-update'),
    path('snippet-updatedelete/<int:pk>/<int:pkLang>/', SnippetUpdateDelete.as_view(), name='snippet-delete-update'),
    path('snippet-updatedelete/<int:pk>/<int:pkLang>/<int:pkTop>', SnippetUpdateDelete.as_view(), name='snippet-delete-update'),
    path('snippet-updatedelete/<int:pk>/<int:pkLang>/<int:pkTop>/<int:pkSubt>/', SnippetUpdateDelete.as_view(), name='snippet-delete-update'),
    ### get languages
    path('get-languages/', GetLanguages.as_view(), name='get-languages'),
    #### get twitter-data


    ]
# router.register('language-topic-subtopic', LanguageTopicSubtopicMV, basename='language-topic-subtopic')



# urlpatterns = router.urls