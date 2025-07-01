from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('quizzes', QuizViewSet)
router.register('questions', QuestionViewSet)
router.register('options', OptionViewSet)
router.register('submissions', SubmissionViewSet)
router.register('answers', AnswerViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/top-scores/', top_scores),
]
