from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Roles for users
class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"


# Workflow definitions
class Workflow(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class WorkflowStep(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name="steps")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.workflow.name} - {self.name}"


class WorkflowTransition(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    from_step = models.ForeignKey(
        WorkflowStep,
        on_delete=models.CASCADE,
        related_name="transitions"  # <-- add this
    )
    to_step = models.ForeignKey(WorkflowStep, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    allowed_roles = models.ManyToManyField(Role)

    def __str__(self):
        return self.name



from django.db import models
from django.utils import timezone

class WorkflowInstance(models.Model):
    workflow = models.ForeignKey('Workflow', on_delete=models.CASCADE)
    started_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    current_step = models.ForeignKey(
        'WorkflowStep',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # ✅ ADD THIS FIELD
    started_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # If creating a new instance and no current_step, set it to the first step
        if not self.pk and not self.current_step:
            first_step = self.workflow.steps.order_by('id').first()
            self.current_step = first_step

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.workflow.name} instance by {self.started_by}"



class WorkflowAction(models.Model):
    instance = models.ForeignKey(
        WorkflowInstance,
        on_delete=models.CASCADE,
        related_name="actions"
    )
    from_step = models.ForeignKey(
        WorkflowStep,
        on_delete=models.SET_NULL,
        null=True,
        related_name="actions_from"
    )
    to_step = models.ForeignKey(
        WorkflowStep,
        on_delete=models.SET_NULL,
        null=True,
        related_name="actions_to"
    )
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    performed_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.instance} | {self.from_step} → {self.to_step}"
