from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path

router = DefaultRouter()
router.register(r'',NewslettersViewSet)
urlpatterns = router.urls

urlpatterns += [
    path('newsletter-detail/<str:name>', NewsletterDetailView.as_view(), name='newsletter-detail'),
    path('newsletter-update/<str:name>', NewsletterUpdateView.as_view(), name='newsletter-update'),
    path('newsletter-delete/<str:name>', NewsletterDeleteView.as_view(), name='newsletter-delete'),
    path('list-user-created-newsletter', ListUserCreatedNewletter.as_view(), name='list-user-created-newsletter'),
    path('list-user-subscribed-newsletter', ListUserSubscribedNewletter.as_view(), name='list-user-subscribed-newsletter'),
    path('newsletter/<str:name>/articles', ListArticlesOfNewsletter, name='list-newsletter-articles'),
    path('user/creator/newsletter', user_creator_newsletter, name='user_creator_newsletter'),
    path('user/joined/newsletter', user_joined_newsletter, name='user_joined_newsletter'),
    path('join/newsletter', join_newsletter, name='join_newsletter'),
    path('newsletter/create-article', CreateArticleView.as_view(), name='create-article'),
    path('newsletter/article-detail/<str:name>', ArticleDetailView.as_view(), name='article-detail'),
    path('newsletter/article-update/<str:name>', ArticleUpdateView.as_view(), name='article-update'),
    path('newsletter/article-delete/<str:name>', ArticleDeleteView.as_view(), name='article-delete')
]
