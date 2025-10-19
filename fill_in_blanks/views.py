from rest_framework import generics, status
from rest_framework.response import Response
from .models import FillInBlankTopic, FillInBlankText, FillInBlankResult
from .serializers import FillInBlankTopicSerializer, FillInBlankTextSerializer
from rest_framework.permissions import IsAuthenticated


class FillInBlankTextByTopicView(generics.ListAPIView):
    serializer_class = FillInBlankTextSerializer

    def get_queryset(self):
        topic_id = self.request.query_params.get('topic_id')
        if not topic_id:
            return FillInBlankText.objects.none()
        return FillInBlankText.objects.filter(topic_id=topic_id)

class FillInBlankTopicListView(generics.ListAPIView):
    queryset = FillInBlankTopic.objects.all()
    serializer_class = FillInBlankTopicSerializer

class FillInBlankTextView(generics.RetrieveAPIView):
    queryset = FillInBlankText.objects.all()
    serializer_class = FillInBlankTextSerializer
    lookup_field = 'pk'


class FillInBlankSubmitView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]  # 👈 Require authenticated user

    def post(self, request, *args, **kwargs):
        text_id = request.data.get('text_id')
        user_answers = request.data.get('answers', [])  # List of strings in order

        if not text_id or not isinstance(user_answers, list):
            return Response(
                {"error": "Invalid input. Provide 'text_id' and 'answers'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            text = FillInBlankText.objects.get(id=text_id)
        except FillInBlankText.DoesNotExist:
            return Response({"error": "Text not found."}, status=404)

        correct_answers = list(text.answers.order_by('blank_index').values_list('correct_answer', flat=True))
        total = len(correct_answers)
        if total == 0:
            return Response({"error": "No blanks defined for this text."}, status=400)

        correct = 0
        results = []

        for i, user_ans in enumerate(user_answers):
            correct_ans = correct_answers[i] if i < len(correct_answers) else None
            is_correct = (correct_ans and user_ans.strip().lower() == correct_ans.strip().lower())
            results.append({
                'index': i,
                'user_answer': user_ans,
                'correct_answer': correct_ans,
                'is_correct': is_correct
            })
            if is_correct:
                correct += 1

        percentage = round((correct / total) * 100)

        # ✅ SAVE THE RESULT TO DATABASE
        FillInBlankResult.objects.create(
            student=request.user,
            fill_in_blank_text=text,
            score=correct,
            total=total,
            percentage=percentage
        )

        return Response({
            "topic": text.topic.name,
            "title": text.title,
            "score": correct,
            "total": total,
            "percentage": f"{percentage}%",
            "results": results
        })