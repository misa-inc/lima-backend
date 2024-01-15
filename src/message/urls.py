from django.urls import path, include

app_name = "message"

urlpatterns = [
    path('api/', include("message.api.urls"))
]