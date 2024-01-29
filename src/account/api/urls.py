from django.urls import path

from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("resend-register-code/", ResendRegisterEmailView.as_view(), name="resend-register-code"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("resend-login-code/", ResendLoginEmailView.as_view(), name="resend-login-code"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("reset-password/", ResetPasswordAPIView.as_view(), name="reset-password"),
    path("resend-reset-code/", ResendResetPasswordView.as_view(), name="resend-reset-code"),
    path("set-new-password/", SetNewPasswordAPIView.as_view(), name="set-new-password"),
    path("email-verify/", VerifyEmail.as_view(), name="email-verify"),
    path("email-login-verify/", VerifyLoginEmail.as_view(), name="email-login-verify"),
    path("email-reset-verify/", VerifyResetEmail.as_view(), name="email-reset-verify"),
    path("create/education/", CreateEducationView.as_view(), name="create-education"),
    path("create/experience/", CreateExperienceView.as_view(), name="create-experience"),
    path("create/badge/", CreateBadgeView.as_view(), name="create-badge"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),    
    path(
        "user/update/<username>/", UserUpdateView.as_view(), name="user-update"
    ),
    path(
        "user/delete/<username>/", UserDeleteView.as_view(), name="user-delete"
    ),
    path(
        "experience/update/<id>/", ExperienceUpdateView.as_view(), name="experience-update"
    ),
    path(
        "experience/delete/<id>/", ExperienceDeleteView.as_view(), name="experience-delete"
    ),
    path(
        "education/update/<id>/", EducationUpdateView.as_view(), name="education-update"
    ),
    path(
        "education/delete/<id>/", EducationDeleteView.as_view(), name="education-delete"
    ),
    path(
        "record/update/<id>/", RecordUpdateView.as_view(), name="record-update"
    ),
    path(
        "record/delete/<id>/", RecordDeleteView.as_view(), name="record-delete"
    ),
    path(
        "badge/update/<id>/", BadgeUpdateView.as_view(), name="badge-update"
    ),
    path(
        "badge/delete/<id>/", BadgeDeleteView.as_view(), name="badge-delete"
    ),
    path("user/detail/<username>/", UpdateUserView.as_view(), name="user-detail"),
    path("user/retrieve/<username>/", UserDetailView.as_view(), name="user-detail"),
    path("experience/retrieve/<id>/", ExperienceDetailView.as_view(), name="experience-detail"),
    path("education/retrieve/<id>/", EducationDetailView.as_view(), name="education-detail"),
    path("record/retrieve/<id>/", RecordDetailView.as_view(), name="record-detail"),
    path("badge/retrieve/<id>/", BadgeDetailView.as_view(), name="badge-detail"),
    path("befriend/user/", befriend_user, name="befriend_user"),
    path("block/user/", block_user, name="block_user"),
    path("friends/<username>/", UserFriends.as_view(), name="user_friends"),
    path("blocked/<username>/", UserBlocked.as_view(), name="user_blocked"),
    path("accept/decline/friend/request/", accept_decline_friend_request, name="accept_decline_friend_request"),
    path("user/befriended/user/", user_befriended_user, name="user_befriended_user"),
    path("password/<username>/", ChangePassword.as_view(), name="change_password"),
    path("verify-two-step-password/", VerifyTwoStepPassword.as_view(), name="verify-two-step-password"),
    path("change-two-step-password/", ChangeTwoStepPassword.as_view(), name="change-two-step-password"),
    path("create-two-step-password/", CreateTwoStepPassword.as_view(), name="create-two-step-password"),
    path("delete-account/", DeleteAccount.as_view(), name="delete-account"),
]
