from django.urls import path, include

app_name = "feedback"


urlpatterns = [
    path("api/", include("feedback.api.urls"))
]   
