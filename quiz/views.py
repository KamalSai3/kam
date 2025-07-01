from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Max

from .models import Quiz, Question, Option, Submission, Answer, User
from .serializers import *

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        quiz_id = self.request.data.get("quiz")
        quiz = Quiz.objects.get(id=quiz_id)
        student = self.request.user
        print("== SUBMITTING ==")
        print("Quiz ID:", quiz.id)
        print("Student:", student.username)
        # Check if already submitted
        if Submission.objects.filter(quiz=quiz, student=student).exists():
            raise serializers.ValidationError("You have already submitted this quiz.")

        submission = serializer.save(student=student, quiz=quiz)

        answers_data = self.request.data.get('answers', [])
        total_score = 0

        for ans in answers_data:
            question_id = ans.get('question')
            question = Question.objects.get(id=question_id)
            student_answer = ans.get('student_answer')

            answer = Answer.objects.create(
                submission=submission,
                question=question,
                student_answer=student_answer
            )

            # Auto-grade only MCQ
            if question.question_type == 'mcq':
                if student_answer.strip().lower() == question.correct_answer.strip().lower():
                    answer.marks_awarded = 1  # You can customize this weight
                    total_score += 1
                else:
                    answer.marks_awarded = 0
                answer.save()

        submission.score = total_score
        submission.save()



class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def top_scores(request):
    top_scores = Submission.objects.values('quiz').annotate(top_score=Max('score'))
    return Response(top_scores)