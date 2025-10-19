from django.utils import timezone

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import GrammarTopic, GrammarQuestion, GrammarResult
from .serializers import (
    GrammarTopicSerializer,
    GrammarQuestionSerializer,
    GrammarResultSerializer,
)
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()

# ✅ Get all topics
class GrammarTopicListView(generics.ListAPIView):
    queryset = GrammarTopic.objects.all()
    serializer_class = GrammarTopicSerializer
    permission_classes = [permissions.IsAuthenticated]


# ✅ Get questions for a specific topic
class GrammarQuestionByTopicView(generics.RetrieveAPIView):
    queryset = GrammarTopic.objects.all()
    serializer_class = GrammarTopicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        topic = self.get_object()
        questions = GrammarQuestion.objects.filter(topic=topic)
        serializer = GrammarQuestionSerializer(questions, many=True)
        return Response(serializer.data)
        # This ensures we return the actual questions list,
        # not just topic info


# ✅ Submit answers and calculate score
class GrammarSubmitView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        topic_id = request.data.get('topic_id')
        user_answers = request.data.get('answers', {})  # e.g., {"1": "Tashkent", "2": "Tokyo"}

        if not topic_id or not isinstance(user_answers, dict):
            return Response(
                {"error": "Invalid input. Provide 'topic_id' and 'answers' as object."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            topic = GrammarTopic.objects.prefetch_related('questions').get(id=topic_id)
        except GrammarTopic.DoesNotExist:
            return Response({"error": "Topic not found."}, status=status.HTTP_404_NOT_FOUND)

        questions = list(topic.questions.all())
        total = len(questions)
        if total == 0:
            return Response({"error": "No questions defined for this topic."}, status=status.HTTP_400_BAD_REQUEST)

        correct = 0
        for question in questions:
            user_answer = user_answers.get(str(question.id))  # e.g., "Tashkent"
            if user_answer:
                # Get the correct answer TEXT (not letter)
                correct_answer_text = question.correct_answer  # Uses your @property
                if user_answer.strip().lower() == correct_answer_text.strip().lower():
                    correct += 1

        # Save result
        GrammarResult.objects.create(
            student=request.user,
            topic=topic,
            score=correct,
            total_questions=total,
            created_at=timezone.now()
        )

        return Response({
            "topic": topic.name,
            "score": correct,
            "total": total,
            "percentage": f"{round((correct / total) * 100)}%",
        })

# ✅ (Optional) List all questions (for testing or admin)
class GrammarQuestionListView(generics.ListAPIView):
    serializer_class = GrammarQuestionSerializer
    queryset = GrammarQuestion.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        topic_id = self.request.query_params.get("topic")
        if topic_id:
            return self.queryset.filter(topic_id=topic_id)
        return self.queryset
