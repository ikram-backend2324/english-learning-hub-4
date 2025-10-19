from rest_framework import generics, status
from rest_framework.response import Response
from .models import SynonymTopic, SynonymPair, SynonymResult
from .serializers import SynonymTopicSerializer, SynonymPairSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class SynonymSubmitView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        topic_id = request.data.get('topic_id')
        user_answers = request.data.get('answers', {})  # e.g., {"happy": "joyful", "sad": "unhappy"}

        if not topic_id or not isinstance(user_answers, dict):
            return Response(
                {"error": "Invalid input. Provide 'topic_id' and 'answers' as object."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            topic = SynonymTopic.objects.get(id=topic_id)
        except SynonymTopic.DoesNotExist:
            return Response({"error": "Topic not found."}, status=404)

        # Get all correct pairs for this topic
        correct_pairs = dict(topic.pairs.values_list('word', 'synonym'))
        total = len(correct_pairs)
        if total == 0:
            return Response({"error": "No synonym pairs defined for this topic."}, status=400)

        # Grade answers
        correct = 0
        for word, user_synonym in user_answers.items():
            if word in correct_pairs:
                correct_synonym = correct_pairs[word].strip().lower()
                if user_synonym.strip().lower() == correct_synonym:
                    correct += 1

        percentage = round((correct / total) * 100, 2)

        # ✅ Save result to database
        SynonymResult.objects.create(
            student=request.user,
            topic=topic,
            score=correct,
            total=total,
            percentage=percentage
        )

        return Response({
            "topic": topic.name,
            "score": correct,
            "total": total,
            "percentage": f"{percentage}%",
        })

class SynonymTopicListView(generics.ListAPIView):
    queryset = SynonymTopic.objects.all()
    serializer_class = SynonymTopicSerializer

class SynonymPairByTopicView(generics.ListAPIView):
    serializer_class = SynonymPairSerializer

    def get_queryset(self):
        topic_id = self.request.query_params.get('topic_id')
        if topic_id and topic_id.isdigit():
            return SynonymPair.objects.filter(topic_id=topic_id)
        return SynonymPair.objects.none()


class SynonymSubmitView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]  # 👈 Require authentication

    def post(self, request, *args, **kwargs):
        topic_id = request.data.get('topic_id')
        user_answers = request.data.get('answers', {})

        if not topic_id or not isinstance(user_answers, dict):
            return Response(
                {"error": "Invalid input. Provide 'topic_id' and 'answers'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get correct pairs for this topic
        correct_pairs = SynonymPair.objects.filter(topic_id=topic_id)
        correct_dict = {pair.word: pair.synonym for pair in correct_pairs}

        if not correct_dict:
            return Response({"error": "No pairs found for this topic."}, status=404)

        total = len(correct_dict)
        correct = 0
        results = {}

        for word, user_syn in user_answers.items():
            correct_syn = correct_dict.get(word)
            is_correct = (correct_syn and user_syn == correct_syn)
            results[word] = {
                'user_answer': user_syn,
                'correct_answer': correct_syn,
                'is_correct': is_correct
            }
            if is_correct:
                correct += 1

        percentage = round((correct / total) * 100)

        # ✅ SAVE TO DATABASE
        try:
            topic = SynonymTopic.objects.get(id=topic_id)
            SynonymResult.objects.create(
                student=request.user,
                topic=topic,
                score=correct,
                total=total,
                percentage=percentage
            )
        except Exception as e:
            print(f"Failed to save result: {e}")

        return Response({
            "topic": topic.name,
            "score": correct,
            "total": total,
            "percentage": f"{percentage}%",
            "results": results
        })