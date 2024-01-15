from django.urls import path, include

app_name = "newsletters"

urlpatterns = [
    path('api/', include("newsletters.api.urls"))
]