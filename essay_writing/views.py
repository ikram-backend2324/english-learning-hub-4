from rest_framework import generics, status
from rest_framework.response import Response
from .models import EssayTopic, EssaySubmission
from .serializers import EssayTopicSerializer, EssaySubmissionSerializer

class EssayTopicListView(generics.ListAPIView):
    queryset = EssayTopic.objects.all()
    serializer_class = EssayTopicSerializer

class EssaySubmitView(generics.CreateAPIView):
    serializer_class = EssaySubmissionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Validate word count
        essay_text = serializer.validated_data['essay_text']
        word_count = len(essay_text.split())
        topic = serializer.validated_data['topic']

        if word_count < topic.word_count_min or word_count > topic.word_count_max:
            return Response({
                "error": f"Word count must be between {topic.word_count_min} and {topic.word_count_max}. Your essay has {word_count} words."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Save submission
        submission = serializer.save()

        return Response({
            "message": "Essay submitted successfully!",
            "submission_id": submission.id,
            "topic": topic.name,
            "student_name": submission.student_name,
            "word_count": word_count,
            "submitted_at": submission.submitted_at
        }, status=status.HTTP_201_CREATED)

class EssayTopicDetailView(generics.RetrieveAPIView):
    queryset = EssayTopic.objects.all()
    serializer_class = EssayTopicSerializer
    lookup_field = 'pk'
