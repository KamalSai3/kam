from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import User, Quiz, Question, Option, Submission, Answer
from .serializers import (
    UserSerializer, QuizSerializer, QuestionSerializer,
    OptionSerializer, SubmissionSerializer, AnswerSerializer
)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


class IsFaculty(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'faculty'

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsFaculty()]
        return [permissions.IsAuthenticated()]

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsFaculty]

class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [IsFaculty]

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsStudent()]
        return [permissions.IsAuthenticated()]
    

    def create(self, request, *args, **kwargs):
        user = request.user
        quiz_id = request.data.get('quiz')

        # 🛑 Check: has student already submitted this quiz?
        if Submission.objects.filter(student=user, quiz_id=quiz_id).exists():
            return Response({'error': 'You have already submitted this quiz.'}, status=400)

        # ✅ Create the submission
        submission = Submission.objects.create(student=user, quiz_id=quiz_id)

        # ⬇️ Collect answers from request
        answers_data = request.data.get('answers', [])
        total_score = 0
        max_score = 0

        for answer in answers_data:
            question_id = answer['question']
            student_answer = answer['student_answer']
            question = Question.objects.get(id=question_id)

            # 📝 Save the answer
            Answer.objects.create(
                submission=submission,
                question=question,
                student_answer=student_answer
            )

            # ✅ Grading logic
            if question.question_type == 'mcq':
                correct = question.correct_answer.strip().lower()
                submitted = student_answer.strip().lower()
                if correct == submitted:
                    total_score += 1  # 1 mark per correct mcq
                max_score += 1

        # 💯 Save score (subjective grading comes later)
        submission.score = total_score
        submission.save()

        return Response({
            'message': 'Submission successful.',
            'submission_id': submission.id,
            'score': total_score,
            'max_score': max_score
        }, status=201)
    
        def update(self, request, *args, **kwargs):
            response = super().update(request, *args, **kwargs)

        # ✅ After updating marks, recalculate submission score
        answer = self.get_object()
        submission = answer.submission
        mcq_score = 0
        manual_score = 0

        for ans in submission.answers.all():
            if ans.question.question_type == 'mcq':
                correct = ans.question.correct_answer.strip().lower()
                student = ans.student_answer.strip().lower()
                if correct == student:
                    mcq_score += 1
            else:
                manual_score += ans.marks_awarded or 0

        submission.score = mcq_score + manual_score
        submission.save()

        return response

    



class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsFaculty()]
        return [permissions.IsAuthenticated()]


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    role = request.data.get('role')  # 'student' or 'faculty'

    if not role or role not in ['student', 'faculty']:
        return Response({'error': 'Role must be student or faculty'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=400)

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        role=role
    )
    refresh = RefreshToken.for_user(user)
    return Response({
        'user': UserSerializer(user).data,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })


