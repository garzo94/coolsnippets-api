from django.urls import  include, path
app_name='user'

urlpatterns =[
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken'))
]