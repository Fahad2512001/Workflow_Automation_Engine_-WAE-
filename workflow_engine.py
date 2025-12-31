# core/services/workflow_engine.py
from django.core.exceptions import PermissionDenied
from core.models import WorkflowInstance, WorkflowStep, WorkflowTransition, WorkflowAction, UserRole, Role

class WorkflowEngine:
    def __init__(self, instance: WorkflowInstance, user):
        self.instance = instance
        self.user = user

    def get_allowed_transitions(self):
        """
        Return a queryset of WorkflowTransition objects
        that the current user is allowed to perform from the current step.
        """
        # Get user's roles
        user_roles = Role.objects.filter(userrole__user=self.user)

        # Only consider transitions from the current step
        transitions = WorkflowTransition.objects.filter(
            workflow=self.instance.workflow,
            from_step=self.instance.current_step
        ).distinct()

        # Filter by allowed roles
        allowed = transitions.filter(allowed_roles__in=user_roles).distinct()
        return allowed

    def perform_transition(self, to_step: WorkflowStep, comment=""):
        """
        Perform a transition to `to_step` if allowed.
        """
        allowed = self.get_allowed_transitions()
        try:
            transition = allowed.get(to_step=to_step)
        except WorkflowTransition.DoesNotExist:
            raise PermissionDenied("You do not have permission to perform this transition.")

        # Record action
        WorkflowAction.objects.create(
            instance=self.instance,
            from_step=self.instance.current_step,
            to_step=to_step,
            performed_by=self.user,
            comment=comment
        )

        # Update instance current step
        self.instance.current_step = to_step
        self.instance.save()
