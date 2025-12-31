from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import WorkflowInstance, WorkflowStep, UserRole, WorkflowTransition
from .services.workflow_engine import WorkflowEngine
from django.http import HttpResponse

@login_required
def dashboard(request):
    user = request.user

    # 1️⃣ Get user's role names
    roles = list(UserRole.objects.filter(user=user).values_list('role__name', flat=True))

    # 2️⃣ Get all workflow instances where current step has transitions allowed for user's role
    instances = WorkflowInstance.objects.filter(current_step__isnull=False)

    workflow_data = []

    for instance in instances:
        # Allowed transitions for this user
        allowed_transitions = instance.current_step.transitions.filter(
            allowed_roles__name__in=roles
        )

        workflow_data.append({
            'instance': instance,
            'allowed_transitions': allowed_transitions
        })

    context = {
        'user': user,
        'workflow_data': workflow_data,
        'roles': roles,
    }

    return render(request, 'core/dashboard.html', context)

@login_required
def perform_transition(request, instance_id, transition_id):
    instance = get_object_or_404(WorkflowInstance, id=instance_id)
    transition = get_object_or_404(WorkflowTransition, id=transition_id)

    # Optional: Check if user has permission
    user_roles = UserRole.objects.filter(user=request.user).values_list('role', flat=True)
    if not transition.allowed_roles.filter(id__in=user_roles).exists():
        raise PermissionDenied("You are not allowed to perform this transition.")

    # Perform transition
    instance.current_step = transition.to_step
    instance.save()
    return redirect('dashboard')

@login_required
def workflow_instance_detail(request, instance_id):
    instance = get_object_or_404(WorkflowInstance, id=instance_id)
    return HttpResponse(
        f"Workflow: {instance.workflow.name}<br>"
        f"Current Step: {instance.current_step}<br>"
        f"Started by: {instance.started_by}"
    )

@login_required
def user_profile(request):
    return render(request, 'core/user_profile.html', {'user': request.user})
