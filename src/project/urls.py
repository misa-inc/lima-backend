from django.urls import path, include

app_name = "project"

urlpatterns = [
    path('api/', include("project.api.urls"))
]   
