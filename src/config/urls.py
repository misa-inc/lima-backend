from django.urls import path, include
from django.contrib import admin

from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView
)

from decouple import config

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('message/', include('message.urls', namespace='message')),
    path('feedback/', include('feedback.urls', namespace='feedback')),
    path('discussion/', include('discussion.urls', namespace='discussion')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('collection/', include('collection.urls', namespace='collection')),
    path('directory/', include('directory.urls', namespace='directory')),
    path('events/', include('events.urls', namespace='events')),
    path('project/', include('project.urls', namespace='project')),
    path('library/', include('library.urls', namespace='library')),
    path('trivia/', include('trivia.urls', namespace='trivia')),
    path('newsletters/', include('newsletters.urls', namespace='newsletters')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    path('page/', include('page.urls', namespace='page')),
    path('post/', include('post.urls', namespace='post')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]


if config("DEBUG", default=False, cast=bool):
    from django.conf.urls.static import static
    from django.conf import settings

    # add root static files
    urlpatterns = urlpatterns + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    # add media static files
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
