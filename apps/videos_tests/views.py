from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Lesson, UserLessonProgress, Question
from .serializers import LessonSerializer

class LessonDetailView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, lesson_id):
        lesson = Lesson.objects.get(id=lesson_id)
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)

    def post(self, request, lesson_id):
        user = request.user
        lesson = Lesson.objects.get(id=lesson_id)
        progress, created = UserLessonProgress.objects.get_or_create(user=user, lesson=lesson)
        
        if progress.is_completed:
            return Response({"message": "Урок уже завершен."})

        # Проверка ответов
        answers = request.data.get('answers', {})
        questions = lesson.questions.all()
        correct_count = 0

        for question in questions:
            user_answer = answers.get(str(question.id))
            if user_answer == question.correct_option:
                correct_count += 1

        # Подсчет результата
        score = (correct_count / questions.count()) * 100
        progress.score = score
        progress.attempts += 1

        if score >= 80:
            progress.is_completed = True
            next_lesson = Lesson.objects.filter(subject=lesson.subject, order=lesson.order + 1).first()
            next_lesson_access = next_lesson is not None
        else:
            next_lesson_access = False

        progress.save()

        return Response({
            "message": "Результаты теста сохранены.",
            "score": score,
            "next_lesson_access": next_lesson_access
        })