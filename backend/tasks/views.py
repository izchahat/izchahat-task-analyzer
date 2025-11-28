from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AnalyzeRequestSerializer
from .scoring import analyze_tasks

class AnalyzeTasksAPIView(APIView):
    def post(self, request):
        serializer = AnalyzeRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        tasks = data["tasks"]
        weights = data.get("weights")

        result = analyze_tasks(tasks, weights)

        top3 = [
            {"id": t["id"], "title": t["title"], "score": t["score"], "reason": t["explanation"]}
            for t in result["top_3"]
        ]

        return Response({
            "scored_tasks": result["scored_tasks"],
            "top_3": top3,
            "issues": result["issues"]
        })

    def get(self, request):
        return Response({
            "message": "Use POST /api/tasks/analyze/ with task list"
        })
