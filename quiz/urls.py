from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, QuizViewSet, QuestionViewSet,
    OptionViewSet, SubmissionViewSet, AnswerViewSet
)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import register


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'options', OptionViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = [
    path('auth/register/', register, name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
