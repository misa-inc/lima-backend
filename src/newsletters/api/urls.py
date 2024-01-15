from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path

router = DefaultRouter()
router.register(r'',views.NewslettersViewSet)
urlpatterns = router.urls

urlpatterns += [
    path('newsletter-detail/<str:name>', views.NewsletterDetailView, name='newsletter-detail'),
    path('newsletter-update/<str:name>', views.NewsletterUpdateView, name='newsletter-update'),
    path('newsletter-delete/<str:name>', views.NewsletterDeleteView, name='newsletter-delete'),
    path('list-user-created-newsletter', views.ListUserCreatedNewletter, name='list-user-created-newsletter'),
    path('list-user-subscribed-newsletter', views.ListUserSubscribedNewletter, name='list-user-subscribed-newsletter'),
    path('newsletter/<str:name>/articles', views.ListArticlesOfNewsletter, name='list-newsletter-articles'),
    path('user/creator/newsletter', views.user_creator_newsletter, name='user_creator_newsletter'),
    path('user/joined/newsletter', views.user_joined_newsletter, name='user_joined_newsletter'),
    path('join/newsletter', views.join_newsletter, name='join_newsletter'),
    path('create-article', views.CreateArticleView, name='create-article'),
    path('article-detail/<str:name>', views.ArticleDetailView, name='article-detail'),
    path('article-update/<str:name>', views.ArticleUpdateView, name='article-update'),
    path('article-delete/<str:name>', views.ArticleDeleteView, name='article-delete')
]
