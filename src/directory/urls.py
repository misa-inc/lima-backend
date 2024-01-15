from django.urls import path, include

app_name = "directory"

urlpatterns = [
    path('api/', include("directory.api.urls"))
]   
