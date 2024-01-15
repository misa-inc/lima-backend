from django.urls import path

from .views import (
    VerifyTwoStepPassword, ChangeTwoStepPassword, CreateTwoStepPassword,
    DeleteAccount, RegisterView, ResendRegisterEmailView, VerifyEmail, 
    LoginAPIView, ResendLoginEmailView, VerifyLoginEmail, ResetPasswordAPIView,
    ResendResetPasswordView, VerifyResetEmail, SetNewPasswordAPIView,
    LogoutAPIView, accept_decline_friend_request, block_user, UserBlocked,
    UserFriends, befriend_user, user_befriended_user, ChangePassword,
    UserUpdateView, UserDetailView, UserDeleteView, UpdateUserView,
)
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
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),    
    path(
        "user/update/<username>/", UserUpdateView.as_view(), name="user-update"
    ),
    path(
        "user/delete/<username>/", UserDeleteView.as_view(), name="user-delete"
    ),
    path("user/detail/<username>/", UpdateUserView.as_view(), name="user-detail"),
    path("user/retrieve/<username>/", UserDetailView.as_view(), name="user-detail"),
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
