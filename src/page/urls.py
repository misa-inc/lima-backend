from django.urls import path, include

app_name = "page"

urlpatterns = [
    path('api/', include("page.api.urls"))
]   
