from rest_framework import serializers
from .models import WorkflowInstance, WorkflowStep, WorkflowTransition, WorkflowAction

class WorkflowStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowStep
        fields = ['id', 'name', 'description']

class WorkflowTransitionSerializer(serializers.ModelSerializer):
    from_step = WorkflowStepSerializer()
    to_step = WorkflowStepSerializer()

    class Meta:
        model = WorkflowTransition
        fields = ['id', 'name', 'from_step', 'to_step']

class WorkflowActionSerializer(serializers.ModelSerializer):
    from_step = WorkflowStepSerializer()
    to_step = WorkflowStepSerializer()

    class Meta:
        model = WorkflowAction
        fields = ['id', 'from_step', 'to_step', 'performed_by', 'performed_at', 'comment']
