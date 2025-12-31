from django.core.exceptions import PermissionDenied
from .models import WorkflowInstance, WorkflowStep, WorkflowTransition, WorkflowAction, UserRole

class WorkflowEngine:
    def __init__(self, instance: WorkflowInstance, user):
        self.instance = instance
        self.user = user

    def get_allowed_transitions(self):
        """
        Return a list of WorkflowTransition objects allowed from current step for this user.
        """
        user_roles = UserRole.objects.filter(user=self.user).values_list('role', flat=True)
        return WorkflowTransition.objects.filter(
            workflow=self.instance.workflow,
            from_step=self.instance.current_step,
            allowed_roles__id__in=user_roles
        ).distinct()

    def perform_transition(self, to_step: WorkflowStep):
        """
        Move workflow instance to next step if allowed for this user.
        Raises PermissionDenied if invalid.
        """
        allowed = self.get_allowed_transitions()
        if not allowed.filter(to_step=to_step).exists():
            raise PermissionDenied("You do not have permission to perform this transition.")

        # Record action
        WorkflowAction.objects.create(
            instance=self.instance,
            performed_by=self.user,
            from_step=self.instance.current_step,
            to_step=to_step
        )

        # Update instance
        self.instance.current_step = to_step
        self.instance.save()
        return self.instance
