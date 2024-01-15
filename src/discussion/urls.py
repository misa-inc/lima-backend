from django.urls import path, include

app_name = "discussion"

urlpatterns = [
    path('api/', include("discussion.api.urls"))
]   
