# coding=utf-8
from django.shortcuts import redirect


def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "Пользователь не найден"
            return render_to_response('login.html', args)
    else:
        return render_to_response('login.html', args)


def logout(request):
    auth.logout(request)
    return redirect('/')


# def register(request):
#     args = {}  # создали пустой словарь
#     args.update(csrf(request))  #
#     args['form'] = UserCreationForm()
#     if request.POST:
#         new_user_form = UserCreationForm(request.POST)
#         if new_user_form.is_valid():
#             new_user_form.save()
#             new_user = auth.authenticate(username=new_user_form.cleaned_data['username'],
#                                          password=new_user_form.cleaned_data['password2'])
#             auth.login(request, new_user)
#             return redirect('/')
#         else:
#             args['form'] = new_user_form
#     return render_to_response('register.html', args)

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from forms import *
from models import *
from django.template import RequestContext
from django.core.mail import send_mail
import hashlib, datetime, random
from django.utils import timezone
from django.contrib.auth.models import User


def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = RegistrationForm()
    if request.POST:
        form = RegistrationForm(request.POST)
        args['form'] = form
        if form.is_valid():
            form.save()  # save user to database if form is valid

            status = form.cleaned_data['status']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt + email).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            # Get user by username
            user = User.objects.get(username=username)

            # Create and save user profile
            new_profile = UserProfile(user=user, activation_key=activation_key,
                                      key_expires=key_expires)
            new_profile.save()

            # Send email with activation key
            email_subject = 'Подтверждение регистрации'
            email_body = "Hey %s %s, thanks for signing up. To activate your account, click this link within \
                                48hours http://127.0.0.1:8082/login/%s" % (status, username, activation_key)

            send_mail(email_subject, email_body, 'fortests.logunovskiy@yandex.ru',
                      [email], fail_silently=False)

            # return HttpResponseRedirect('/auth/register_success')
            return redirect('/auth/register_success')
        else:
            args['form'] = RegistrationForm()

    return render_to_response('register.html', args, context_instance=RequestContext(request))


def register_success(request):
        return render_to_response('register_success.html')


def register_confirm(request, activation_key):

    # check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect('/')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    # check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires > timezone.now():

        return render_to_response('user_profile/confirm_expired.html')

    # if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('login.html')


