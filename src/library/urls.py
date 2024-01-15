from django.urls import path, include

app_name = "library"

urlpatterns = [
    path('api/', include("library.api.urls"))
]