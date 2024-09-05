from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Call, Participant, Invitation
from django.contrib.auth.models import User

@login_required
def start_one_to_one_call(request, invitee_id):
    invitee = get_object_or_404(User, pk=invitee_id)
    call = Call.objects.create(host=request.user)
    Participant.objects.create(user=request.user, call=call)
    Participant.objects.create(user=invitee, call=call)
    
    # Create an invitation for the invitee
    Invitation.objects.create(call=call, inviter=request.user, invitee=invitee)
    
    return redirect('call_view', call_id=call.call_id)



def join_call(request, call_id):
    call = get_object_or_404(Call, call_id=call_id)
    return render(request, 'call/join_call.html', {'call': call})





@login_required
def start_group_call(request):
    call = Call.objects.create(host=request.user)
    Participant.objects.create(user=request.user, call=call)
    
    # Create invitations for selected users
    invitee_ids = request.POST.getlist('invitees')
    for invitee_id in invitee_ids:
        invitee = User.objects.get(pk=invitee_id)
        Invitation.objects.create(call=call, inviter=request.user, invitee=invitee)
    
    return redirect('call_view', call_id=call.call_id)


@login_required
def accept_invitation(request, invite_id):
    invitation = get_object_or_404(Invitation, invite_id=invite_id)
    if not invitation.accepted and invitation.invitee == request.user:
        invitation.accepted = True
        invitation.save()
        Participant.objects.create(user=request.user, call=invitation.call)
    
    return redirect('call_view', call_id=invitation.call.call_id)
def call_view(request, call_id):
    call = get_object_or_404(Call, call_id=call_id)
    return render(request, 'call/call.html', {'call': call})