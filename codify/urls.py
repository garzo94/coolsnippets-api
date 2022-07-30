from django.urls import path, include
# from watchlist_app.api import views #importing views from api folder
from codify.views import language, topic

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

urlpatterns=[
    path('language-list/', language, name='language'),
    path('language-topics/<int:pk>/',topic, name='topic' )
    ]
# router.register('language-topic-subtopic', LanguageTopicSubtopicMV, basename='language-topic-subtopic')


# urlpatterns = router.urls