from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, UserProfileForm
from django.core.signing import Signer, BadSignature
from .models import UserProfile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserProfile

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserProfile

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_step_count_api(request):
    steps = request.data.get('step_count')
    if steps is not None and str(steps).isdigit():
        profile = UserProfile.objects.get(user=request.user)
        profile.step_count = int(steps)
        profile.save()
        return Response({'status': 'success', 'steps_updated': profile.step_count}, status=200)
    return Response({'status': 'error', 'message': 'Invalid step count'}, status=400)

update_step_count_api.renderer_classes = [JSONRenderer]  # Force JSON responses for this view

# Register view with email verification
def register_view(request):
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            email = user_form.cleaned_data['email']
            
            # Check if email already exists
            if get_user_model().objects.filter(email=email).exists():
                messages.error(request, "This email is already registered.")
                return redirect('register')  # Redirect back to the registration page
            
            # Proceed with user registration
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.is_active = False  # User is not active until email is verified
            user.save()

            # Create user profile and link to the user
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # Email verification
            signer = Signer()
            token = signer.sign(user.email)

            verification_url = request.build_absolute_uri(
                reverse('verify_email') + f'?token={token}'
            )

            # Send email asynchronously (considering the async flag)
            send_mail(
                subject='Confirm Your Email – Health & Fitness App',
                message=f'Hi {user.username},\n\nPlease verify your email by clicking the link below:\n\n{verification_url}\n\nThanks!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return render(request, "users/verify_notice.html", {"email": user.email})
    else:
        user_form = RegisterForm()
        profile_form = UserProfileForm()

    return render(request, "users/register.html", {
        "user_form": user_form,
        "profile_form": profile_form
    })

# Email confirmation view
def verify_email(request):
    # Retrieve the token from the query parameter
    token = request.GET.get('token')

    if not token:
        return render(request, 'users/invalid_token.html')

    signer = Signer()

    try:
        email = signer.unsign(token)
        user = User.objects.get(email=email)
        
        if user.is_active:
            messages.success(request, "Your email is already verified.")
            return redirect('login')
        
        user.is_active = True
        user.save()

        login(request, user)

        # Send final welcome email
        send_mail(
            subject='🎉 Welcome to Health & Fitness App!',
            message='Your email has been verified. You can now start using all features!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return render(request, 'users/email_verified.html')

    except (BadSignature, User.DoesNotExist):
        return render(request, 'users/invalid_token.html', {'error': 'Invalid or expired token.'})

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:  # If user is valid
            login(request, user)  # Log the user in
            messages.success(request, "Successfully logged in!")
            
            # Redirect to the page the user was trying to access before login
            next_url = request.GET.get('next', 'result')  # Default to 'dashboard' if no 'next' param
            return redirect(next_url)
        else:
            # If authentication fails, show an error message
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # Redirect back to login page

    return render(request, 'users/login.html')

# Logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Profile view

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    bmi = None
    step_count = profile.step_count

    if request.method == 'POST':
        # Handle BMI calculation
        height = float(request.POST.get('height')) / 100  # Convert cm to meters
        weight = float(request.POST.get('weight'))
        bmi = weight / (height ** 2)

        # Handle step count update
        if 'step_count' in request.POST:
            step_count = int(request.POST.get('step_count'))
            profile.step_count = step_count
            profile.save()

    return render(request, 'users/profile.html', {'profile': profile, 'bmi': bmi, 'step_count': step_count})

# Dashboard view
@login_required
def dashboard_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'dashboard.html', {'profile': profile})  # or any relevant template

# Home view
def home_view(request):
    return render(request, 'home.html')
def about_view(request):
    return render(request, 'users/about.html')
def carrer_view(request):
    return render(request, 'users/careers.html')

def press_view(request):
    return render(request, 'users/press.html')



# Notify user signup using Supabase (example feature)
from .supabase_client import supabase

@login_required
def notify_user_signup(request):
    email = request.user.email  # Get email from logged-in user

    data = {
        "email": email,
        "message": "Welcome to your fitness coach platform!"
    }

    # Insert notification data into Supabase
    supabase.table("notifications").insert(data).execute()

    return render(request, 'users/email_sent.html')

def loader_view(request):
    return render(request, 'users/loader.html')
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserProfile


@login_required
def edit_profile(request):
    # Get the logged-in user's profile
    user_profile = UserProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        # If form is submitted, process it
        user_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')  # Redirect to the profile page after saving
        else:
            messages.error(request, "There was an error updating your profile. Please try again.")
    else:
        # Display current profile in the form
        user_form = UserProfileForm(instance=user_profile)

    return render(request, 'users/edit_profile.html', {'user_form': user_form})

# View to display the list of all blogs
def blogs_list(request):
    return render(request, 'users/blog.html')

# View to display the full blog post details
def blog_detail(request, slug):
    # Example hardcoded blogs data (in real-world, you would fetch from a database)
    blogs_data = {
        'ai-and-fitness': {
            'title': 'AI and Fitness: A Perfect Match',
            'image': 'blog1.jpg',
            'full_content': 'This is the full content about AI and fitness, explaining how AI is transforming personalized training, injury prevention, and more...'
        },
        'tech-wellness': {
            'title': 'How Tech is Changing Wellness Trends',
            'image': 'blog2.jpg',
            'full_content': 'In this blog, we explore the impact of tech innovations on wellness, covering everything from fitness trackers to wellness apps...'
        },
        'fitness-journey': {
            'title': 'Transform Your Fitness Journey',
            'image': 'blog3.jpeg',
            'full_content': 'A guide to setting realistic fitness goals and using AI-powered coaching apps to stay on track with your fitness journey...'
        },
    }

    # Get the blog data based on slug
    blog = blogs_data.get(slug, None)

    if blog:
        return render(request, 'users/blog_detail.html', {
            'blog_title': blog['title'],
            'blog_image': blog['image'],
            'blog_full_content': blog['full_content']
        })
    else:
        # If blog not found, return a 404 or other appropriate response
        return render(request, '404.html')  # 404 page or custom error page



def contact_view(request):
    return render(request, 'users/contactus.html')
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage
from django.core.mail import send_mail
from django.conf import settings

def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message')

        # Save to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message_text
        )

        # Optional: Send email to admin
        send_mail(
            subject=f'New Contact Message from {name}',
            message=message_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=True
        )

        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('contact')
    return redirect('contact')

