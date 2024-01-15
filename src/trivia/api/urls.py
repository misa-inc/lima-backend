from django.urls import path
from .views import *


urlpatterns = [
    # trivia VIEWS    
    path('create-trivia/', CreateTriviaView.as_view(), name='create_trivia'),
    path('trivia-delete/', TriviaDeleteView.as_view(), name='trivia_delete'),
    path('trivia/<int:id>/update/', TriviaUpdateView.as_view(), name='trivia_update'),
    path('trivia/vote/', VoteOnTrivia, name='vote_trivia'),
    path('user/voted/trivia/', user_voted_trivia, name='user_voted_trivia'),
    path("report/trivia/", report_trivia, name="report_trivia"),
    path('user/reported/trivia/', user_reported_trivia, name='user_reported_trivia'),
    path("save/trivia/", save_trivia, name="save_trivia"),
    path('user/saved/trivia/', user_saved_trivia, name='user_saved_trivia'),
    path('user/<str:username>/trivias/', ListTriviaOfUser, name='users_trivias'), 
    path('user/<str:username>/trivia/<int:s_id>/', DetailTriviaOfUser.as_view(), name='users_trivia_detail'),
    # quiz VIEWS    
    path('create-quiz/', CreateQuizView.as_view(), name='create_quiz'),
    path('quiz-delete/', QuizDeleteView.as_view(), name='quiz_delete'),
    path('quiz/<int:id>/update/', QuizUpdateView.as_view(), name='quiz_update'),
    path('user/<str:username>/quizzes/', ListQuizOfTrivia, name='users_quizzes'), 
    # comment VIEWS
    path('create-comment/', CreateCommentView.as_view(), name='create_comment'),
    path('comment-delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('comment/<int:id>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/vote/', VoteOnComment, name='vote_comment'),
    path('user/voted/comment/', user_voted_comment, name='user_voted_comment'),
    path("report/comment/", report_comment, name="report_comment"),
    path('user/reported/comment/', user_reported_comment, name='user_reported_comment'),
    path("save/comment/", save_comment, name="save_comment"),
    path('user/saved/comment/', user_saved_comment, name='user_saved_comment'),
    path('user/<str:username>/comments/', ListCommentsOfUser.as_view(), name='users-comments'),
    path('user/<str:username>/comments/<int:s_id>/', DetailCommentsOfUser.as_view(), name='users-comments-detail'), 
    path('trivias/<int:s_id>/popular-comments/', ListPopularCommentsOfTrivia.as_view(), name='popular-trivia-comments'),
    path('trivias/<int:s_id>/old-comments/', ListOldCommentsOfTrivia.as_view(), name='old-trivia-comments'),
    path('trivias/<int:s_id>/new-comments/', ListNewCommentsOfTrivia.as_view(), name='new-trivia-comments'),
    path('trivias/<int:s_id>/comments/<int:c_id>/', DetailCommentsOfTrivia.as_view(), name='trivia-comments-detail'),
]
