from django.contrib import admin
from .models import (
    Role,
    UserRole,
    Workflow,
    WorkflowStep,
    WorkflowTransition,
    WorkflowInstance,
    WorkflowAction,
)

admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(Workflow)
admin.site.register(WorkflowStep)
admin.site.register(WorkflowTransition)
admin.site.register(WorkflowInstance)
admin.site.register(WorkflowAction)
