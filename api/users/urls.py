from django.urls import path

from users.views import (UserRegistrationView,
                         UserAuthenticationView,
                         UserListView,
                         UserDetail,
                         )

urlpatterns = [
    path('login/', UserAuthenticationView.as_view()),
    path('signup/', UserRegistrationView.as_view()),
    path('users/', UserListView.as_view()),
    path('users/<int:pk>', UserDetail.as_view()),

]
