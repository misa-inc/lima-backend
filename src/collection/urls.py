from django.urls import path, include

app_name = "collection"

urlpatterns = [
    path('api/', include("collection.api.urls"))
]   
