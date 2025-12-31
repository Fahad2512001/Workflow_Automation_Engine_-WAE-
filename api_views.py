from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from core.models import WorkflowInstance, WorkflowStep
from core.services.workflow_engine import WorkflowEngine
from .serializers import WorkflowTransitionSerializer, WorkflowActionSerializer

class AllowedTransitionsView(APIView):
    def get(self, request, instance_id):
        instance = get_object_or_404(WorkflowInstance, id=instance_id)
        engine = WorkflowEngine(instance, request.user)
        transitions = engine.get_allowed_transitions()
        serializer = WorkflowTransitionSerializer(transitions, many=True)
        return Response(serializer.data)


class PerformTransitionView(APIView):
    def post(self, request, instance_id, step_id):
        instance = get_object_or_404(WorkflowInstance, id=instance_id)
        to_step = get_object_or_404(WorkflowStep, id=step_id)
        engine = WorkflowEngine(instance, request.user)

        try:
            engine.perform_transition(to_step)
            return Response({"status": "success", "message": "Transition performed."})
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
