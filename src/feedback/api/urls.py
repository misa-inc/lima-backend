from django.urls import path

from .views import *

urlpatterns = [
    # FEEDBACK VIEWS    
    path('create-feedback/', CreateFeedbackView.as_view(), name='create_feedback'),
    path('feedback-create/', FeedbackCreateView.as_view(), name='feedback_create'),
    path('feedback-delete/', FeedbackDeleteView.as_view(), name='feedback_delete'),
    path('feedback/<int:id>/update/', FeedbackUpdateView.as_view(), name='feedback_update'),
    path('feedback/vote/', VoteOnFeedback, name='vote_feedback'),
    path('u/voted/feedback/', user_voted_feedback, name='user_voted_feedback'),
    path('retrieve/feedback/<int:pk>/', RetrieveFeedback.as_view(), name='retrieve_feedback'),
    path("report/feedback/", report_feedback, name="report_feedback"),
    path('u/reported/feedback/', user_reported_feedback, name='user_reported_feedback'),
    path('u/<str:username>/feedbacks/', ListFeedbacksOfUser, name='users_feedbacks'), 
    path('u/<str:username>/feedbacks/<int:p_id>/', DetailFeedbackOfUser.as_view(), name='users_feedback_detail'),
    # COMMENT VIEWS
    path('create-comment/', CreateCommentView.as_view(), name='create_comment'),
    path('comment-delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('comment/<int:id>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/vote/', VoteOnComment, name='vote_comment'),
    path('u/voted/comment/', user_voted_comment, name='user_voted_comment'),
    path("report/comment/", report_comment, name="report_comment"),
    path('u/reported/comment/', user_reported_comment, name='user_reported_comment'), 
    path('u/<str:username>/comments/', ListCommentsOfUser.as_view(), name='users-comments'),
    path('u/<str:username>/comments/<int:c_id>/', DetailCommentsOfUser.as_view(), name='users-comments-detail'), 
    path('feedback/<int:p_id>/popular-comments/', ListPopularCommentsOfFeedback.as_view(), name='popular-feedback-comments'),
    path('feedback/<int:p_id>/old-comments/', ListOldCommentsOfFeedback.as_view(), name='old-feedback-comments'),
    path('feedback/<int:p_id>/new-comments/', ListNewCommentsOfFeedback.as_view(), name='new-feedback-comments'),
    path('feedback/<int:p_id>/comments/<int:c_id>/', DetailCommentsOfFeedback.as_view(), name='feedback-comments-detail'),
]
