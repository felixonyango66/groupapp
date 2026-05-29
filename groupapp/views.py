from django.shortcuts import render, redirect
from .models import Group
from .models import Group, Milestone, GroupPhoto, Announcement, Teaching, Training, Mission, Member, Vision, Feedback, FundingRecord
from .models import Member, FundingRecord, Feedback
from collections import defaultdict
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Sum
from .models import Event
from .models import Notification,Document
from django.core.mail import send_mail
from django.core.mail import send_mail
from django.http import JsonResponse
from .models import PasswordReset
from .models import AIChat

                                                            



def home(request):
    return render(request, 'home.html')


def register_group(request):

    error = ''

    if request.method == 'POST':

        group_name = request.POST['group_name'].strip()
        email = request.POST['email'].strip()
        phone = request.POST['phone'].strip()
        location = request.POST['location'].strip()
        description = request.POST['description'].strip()
        password = request.POST['password'].strip()

        # CHECK IF GROUP ALREADY EXISTS
        existing_group = Group.objects.filter(
            group_name__iexact=group_name
        ).first()

        if existing_group:

            error = 'Group name already exists'

        else:

            # CREATE NEW GROUP WITH HASHED PASSWORD
            Group.objects.create(
                group_name=group_name,
                email=email,
                phone=phone,
                location=location,
                description=description,
                password=make_password(password)
            )

            return redirect('login_group')

    return render(request, 'register_group.html', {
        'error': error
    })


def login_group(request):

    error = ''

    if request.method == 'POST':

        group_name = request.POST['group_name'].strip()
        password = request.POST['password'].strip()

        # FIND GROUP ONLY BY NAME
        group = Group.objects.filter(
            group_name__iexact=group_name
        ).first()

        # CHECK HASHED PASSWORD
        if group and check_password(password, group.password):

            request.session['group_id'] = group.id
            request.session['role'] = 'leader'

            return redirect('dashboard')

        else:
            error = 'Invalid Group Name or Password'

    return render(request, 'login.html', {
        'error': error
    })



from collections import defaultdict
from django.db.models import Sum


def dashboard(request):

    if 'group_id' not in request.session:
        return redirect('login_group')

    group = Group.objects.get(id=request.session['group_id'])

    # ANALYTICS COUNTS
    members_count = Member.objects.filter(group=group).count()

    feedback_count = Feedback.objects.filter(group=group).count()

    milestones_count = Milestone.objects.filter(group=group).count()

    # TOTAL FUNDING
    funding_total = FundingRecord.objects.filter(
        group=group
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    # NOTIFICATIONS COUNT
    notification_count = Notification.objects.filter(
        group=group,
        is_read=False
    ).count()

    # FUNDING GRAPH DATA
    funding_records = FundingRecord.objects.filter(group=group)

    monthly_funding = defaultdict(float)

    for record in funding_records:

        month = record.date.strftime('%b')

        monthly_funding[month] += float(record.amount)

    funding_labels = list(monthly_funding.keys())

    funding_values = list(monthly_funding.values())

    # ROLE SYSTEM
    role = request.session.get('role', 'member')

    return render(request, 'dashboard.html', {

        'group': group,

        'role': role,

        'members_count': members_count,

        'feedback_count': feedback_count,

        'milestones_count': milestones_count,

        'funding_total': funding_total,

        'funding_labels': funding_labels,

        'funding_values': funding_values,

        'notification_count': notification_count,

    })



def milestones(request):

    if 'group_id' not in request.session:
        return redirect('login_group')

    group = Group.objects.get(id=request.session['group_id'])

    if request.method == 'POST':

        title = request.POST['title']
        description = request.POST['description']
        date = request.POST['date']

        Milestone.objects.create(
            group=group,
            title=title,
            description=description,
            date=date
        )

        return redirect('milestones')

    milestones = Milestone.objects.filter(group=group)

    context = {
        'group': group,
        'milestones': milestones
    }

    return render(request, 'milestones.html', context)

def group_photos(request):

    if 'group_id' not in request.session:
        return redirect('login_group')

    group = Group.objects.get(id=request.session['group_id'])

    if request.method == 'POST':

        title = request.POST['title']
        image = request.FILES['image']

        GroupPhoto.objects.create(
            group=group,
            title=title,
            image=image
        )

        return redirect('group_photos')

    photos = GroupPhoto.objects.filter(group=group)

    context = {
        'group': group,
        'photos': photos
    }

    return render(request, 'group_photos.html', context)

def announcements(request):

    if 'group_id' not in request.session:
        return redirect('login_group')

    group = Group.objects.get(id=request.session['group_id'])

    if request.method == 'POST':

        title = request.POST['title']
        message = request.POST['message']

        Announcement.objects.create(
            group=group,
            title=title,
            message=message
        )

        return redirect('announcements')

    announcements = Announcement.objects.filter(
        group=group
    ).order_by('-created_at')

    context = {
        'group': group,
        'announcements': announcements
    }

    return render(request, 'announcements.html', context)


def teaching_platform(request):

    if 'group_id' not in request.session:
        return redirect('login_group')

    group = Group.objects.get(id=request.session['group_id'])

    if request.method == 'POST':

        title = request.POST['title']
        content = request.POST['content']

        uploaded_file = request.FILES.get('file')

        Teaching.objects.create(
            group=group,
            title=title,
            content=content,
            file=uploaded_file
        )

        return redirect('teaching_platform')

    teachings = Teaching.objects.filter(
        group=group
    ).order_by('-created_at')

    context = {
        'group': group,
        'teachings': teachings
    }

    return render(request, 'teaching_platform.html', context)

def training_platform(request):

    if 'group_id' not in request.session:
        return redirect('login_group')

    group = Group.objects.get(id=request.session['group_id'])

    if request.method == 'POST':

        title = request.POST['title']
        description = request.POST['description']
        date = request.POST['date']
        meeting_link = request.POST.get('meeting_link')

        Training.objects.create(
            group=group,
            title=title,
            description=description,
            date=date,
            meeting_link=meeting_link
        )
        Notification.objects.create(
        group=group,
        message=f"New training uploaded: {title}"
        )

        return redirect('training_platform')

    trainings = Training.objects.filter(group=group).order_by('-date')

    return render(request, 'training_platform.html', {
        'group': group,
        'trainings': trainings
    })

def missions(request):

    if 'group_id' not in request.session:
        return redirect('login_group')

    group = Group.objects.get(id=request.session['group_id'])

    if request.method == 'POST':

        title = request.POST['title']
        description = request.POST['description']

        Mission.objects.create(
            group=group,
            title=title,
            description=description
        )

        return redirect('missions')

    missions = Mission.objects.filter(group=group).order_by('-created_at')

    return render(request, 'missions.html', {
        'group': group,
        'missions': missions
    })

from django.core.mail import send_mail
from .models import Notification, Member, Group


from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail

from .models import Group, Member, Notification


def members(request):

    # CHECK LOGIN
    if 'group_id' not in request.session:
        return redirect('login_group')

    # GET GROUP
    group = Group.objects.get(id=request.session['group_id'])

    # GET USER ROLE FROM SESSION
    role = request.session.get('role')

    # ONLY LEADERS CAN ADD MEMBERS
    if request.method == 'POST':

        if role != 'leader':
            return redirect('members')

        full_name = request.POST['full_name']
        email = request.POST.get('email')
        phone = request.POST['phone']
        member_role = request.POST.get('role', 'Member')
        bio = request.POST.get('bio')
        profile_photo = request.FILES.get('profile_photo')

        # CREATE MEMBER
        Member.objects.create(
            group=group,
            full_name=full_name,
            email=email,
            phone=phone,
            role=member_role,
            bio=bio,
            profile_photo=profile_photo
        )

        # NOTIFICATION
        Notification.objects.create(
            group=group,
            message=f"New member added: {full_name}"
        )

        # EMAIL
        try:

            if email:

                send_mail(
                    subject="Welcome to the Group 🎉",

                    message=f"""
Hello {full_name},

You have been successfully added to {group.group_name}.

Role: {member_role}
Phone: {phone}

Welcome aboard!
                    """,

                    from_email="yourgmail@gmail.com",

                    recipient_list=[email],

                    fail_silently=True
                )

        except Exception as e:

            print("EMAIL ERROR:", e)

        return redirect('members')

    # FETCH MEMBERS
    members = Member.objects.filter(
        group=group
    ).order_by('-joined_at')

    return render(request, 'members.html', {

        'group': group,
        'members': members,
        'role': role

    })


# DELETE MEMBER
def delete_member(request, member_id):

    # CHECK LOGIN
    if 'group_id' not in request.session:
        return redirect('login_group')

    # CHECK ROLE
    role = request.session.get('role')

    if role != 'leader':
        return redirect('members')

    # GET GROUP
    group = Group.objects.get(id=request.session['group_id'])

    # GET MEMBER
    member = get_object_or_404(
        Member,
        id=member_id,
        group=group
    )

    # DELETE MEMBER
    member.delete()

    # NOTIFICATION
    Notification.objects.create(
        group=group,
        message=f"Member deleted: {member.full_name}"
    )

    return redirect('members')



def visions(request):

    if 'group_id' not in request.session:
        return redirect('login_group')

    group = Group.objects.get(id=request.session['group_id'])

    if request.method == 'POST':

        title = request.POST['title']
        description = request.POST['description']

        Vision.objects.create(
            group=group,
            title=title,
            description=description
        )

        return redirect('visions')

    visions = Vision.objects.filter(group=group).order_by('-created_at')

    return render(request, 'visions.html', {
        'group': group,
        'visions': visions
    })


def feedbacks(request):

    if 'group_id' not in request.session:
        return redirect('login_group')

    group = Group.objects.get(id=request.session['group_id'])

    if request.method == 'POST':

        full_name = request.POST['full_name']
        message = request.POST['message']

        Feedback.objects.create(
            group=group,
            full_name=full_name,
            message=message
        )

        return redirect('feedbacks')

    feedbacks = Feedback.objects.filter(group=group).order_by('-created_at')

    return render(request, 'feedbacks.html', {
        'group': group,
        'feedbacks': feedbacks
    })


def settings(request):

    if 'group_id' not in request.session:
        return redirect('login_group')

    group = Group.objects.get(id=request.session['group_id'])

    if request.method == 'POST':

        group.email = request.POST['email']
        group.phone = request.POST['phone']
        group.location = request.POST['location']
        group.description = request.POST['description']

        group.save()

        return redirect('settings')

    return render(request, 'settings.html', {
        'group': group
    })


from django.core.mail import send_mail


def funding_records(request):

    if 'group_id' not in request.session:
        return redirect('login_group')

    group = Group.objects.get(id=request.session['group_id'])

    if request.method == 'POST':

        source = request.POST['source']
        amount = request.POST['amount']
        purpose = request.POST['purpose']
        date = request.POST['date']

        # SAVE FUNDING RECORD
        FundingRecord.objects.create(
            group=group,
            source=source,
            amount=amount,
            purpose=purpose,
            date=date
        )

        # 🔔 NOTIFICATION
        Notification.objects.create(
            group=group,
            message=f"Funding received from {source}"
        )

        # ✉️ EMAIL ALERT
        try:
            if group.email:
                send_mail(
                subject="Funding Update 💰",
                message=f"""
Hello {group.group_name},

Your group has received funding.

Source: {source}
Amount: {amount}
Purpose: {purpose}

Regards,
Group Management System
                """,
                from_email="yourgmail@gmail.com",
                recipient_list=[group.email],
                fail_silently=True
            )
        
        except Exception as e:
            print("EMAIL ERROR:", e)

        return redirect('funding_records')

    records = FundingRecord.objects.filter(group=group).order_by('-created_at')

    return render(request, 'funding_records.html', {
        'group': group,
        'records': records
    })



from django.shortcuts import redirect

def logout_group(request):
    request.session.flush()  # clears ALL session data
    return redirect('login_group')

def events(request):

    if 'group_id' not in request.session:
        return redirect('login_group')

    group = Group.objects.get(id=request.session['group_id'])

    if request.method == 'POST':

        title = request.POST['title']
        description = request.POST['description']
        event_date = request.POST['event_date']
        event_time = request.POST['event_time']
        location = request.POST['location']

        Event.objects.create(
            group=group,
            title=title,
            description=description,
            event_date=event_date,
            event_time=event_time,
            location=location
        )
        Notification.objects.create(
        group=group,
        message=f"Meeting scheduled: {title}"
        )

        return redirect('events')

    events = Event.objects.filter(group=group).order_by('event_date')

    return render(request, 'events.html', {
        'group': group,
        'events': events
    })


def notifications(request):

    if 'group_id' not in request.session:
        return redirect('login_group')

    group = Group.objects.get(id=request.session['group_id'])

    notifications = Notification.objects.filter(
        group=group
    ).order_by('-created_at')

    return render(request, 'notifications.html', {
        'group': group,
        'notifications': notifications
    })


def documents(request):

    if 'group_id' not in request.session:
        return redirect('login_group')

    group = Group.objects.get(id=request.session['group_id'])

    if request.method == 'POST':

        title = request.POST['title']
        description = request.POST['description']
        file = request.FILES['file']

        Document.objects.create(
            group=group,
            title=title,
            description=description,
            file=file,
            uploaded_by=group.group_name
        )

        Notification.objects.create(
            group=group,
            message=f"New document uploaded: {title}"
        )

        return redirect('documents')

    documents = Document.objects.filter(group=group).order_by('-created_at')

    return render(request, 'documents.html', {
        'group': group,
        'documents': documents
    })


def request_reset(request):

    if request.method == "POST":

        group_name = request.POST['group_name']

        group = Group.objects.filter(group_name__iexact=group_name).first()

        if group:

            reset = PasswordReset.objects.create(group=group)

            reset_link = f"http://127.0.0.1:8000/reset-password/{reset.token}/"
            try:
                send_mail(
                    subject="Password Reset Request",
                    message=f"Click the link to reset your password: {reset_link}",
                    from_email="yourgmail@gmail.com",
                    recipient_list=[group.email],
                    fail_silently=True
                )
            except Exception as e:
                print("EMAIL ERROR:", e)

            return JsonResponse({"message": "Reset link sent to email"})

        return JsonResponse({"error": "Group not found"})

    return render(request, "request_reset.html")


def reset_password(request, token):

    reset = PasswordReset.objects.filter(token=token).first()

    if not reset:
        return redirect('login_group')

    if request.method == "POST":

        new_password = request.POST['password']

        reset.group.password = new_password
        reset.group.save()

        reset.delete()

        return redirect('login_group')

    return render(request, "reset_password.html")


from django.http import JsonResponse
from django.db.models import Sum
from .models import Member, FundingRecord, Milestone, Group


def ai_assistant(request):

    # 🔐 SESSION CHECK
    if 'group_id' not in request.session:
        return JsonResponse({"response": "Not logged in"})

    # 🔍 GET GROUP SAFELY
    try:
        group = Group.objects.get(id=request.session['group_id'])
    except Group.DoesNotExist:
        return JsonResponse({"response": "Group not found"})

    # 🧠 INPUT MESSAGE
    message = request.GET.get('message', '').lower().strip()

    # 📊 BASIC ANALYTICS
    members_count = Member.objects.filter(group=group).count()
    milestones_count = Milestone.objects.filter(group=group).count()

    funding_total = FundingRecord.objects.filter(group=group).aggregate(
        total=Sum('amount')
    )['total'] or 0

    # 🤖 RESPONSE LOGIC
    response = ""

    # 1. SUMMARY INSIGHT
    if "summary" in message:

        response = (
            f"📊 GROUP SUMMARY\n\n"
            f"👥 Members: {members_count}\n"
            f"🎯 Milestones: {milestones_count}\n"
            f"💰 Total Funding: {funding_total}\n\n"
            f"Overall Status: {'Active' if members_count > 5 else 'Growing'}\n\n"
            f"Recommendation: "
            f"{'Keep engaging members and increase activities.' if members_count < 10 else 'Good engagement, maintain consistency.'}"
        )

    # 2. MEMBERS INSIGHT
    elif "members" in message:

        if members_count < 5:
            response = f"⚠️ You have only {members_count} members. Growth is needed."
        else:
            response = f"👥 Good! You have {members_count} active members."

    # 3. FUNDING INSIGHT
    elif "funding" in message:

        if funding_total < 1000:
            response = f"⚠️ Funding is low ({funding_total}). Consider fundraising activities."
        else:
            response = f"💰 Strong funding base: {funding_total}. Keep it up!"

    # 4. MILESTONE INSIGHT
    elif "milestone" in message:

        if milestones_count == 0:
            response = "🚀 No milestones yet. Start setting group goals."
        else:
            response = f"🏆 You have achieved {milestones_count} milestones. Great progress!"

    # 5. DEFAULT INSIGHT
    else:
        response = (
            f"🤖 SMART INSIGHT\n\n"
            f"👥 Members: {members_count}\n"
            f"🎯 Milestones: {milestones_count}\n"
            f"💰 Funding: {funding_total}\n\n"
            f"Tip: Focus on engagement, training, and consistent group activity."
        )
        AIChat.objects.create(
        group=group,
        message=message,
        response=response
        )

    return JsonResponse({"response": response})


