from django.urls import path, include

app_name = "trivia"

urlpatterns = [
    path('api/', include("trivia.api.urls"))
]   
