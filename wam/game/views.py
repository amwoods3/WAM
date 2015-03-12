from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf

from forms import UploadFileForm, UserRegisterForm, UserLoginForm
from game.models import UserLogin, UserAiTable, UserStats
from config import FILE_PATH

# f is file object, n is user_name/title_of_file
def handle_uploaded_file(f, n):
    with open(FILE_PATH + 'wam/ais/' + n + '.py', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
            
def logged_in(request):
    if 'member_id' in request.session:
        return True
    return False

# Create your views here.
def index(request):
    c = {'user_logged_in': logged_in(request)}
    if logged_in(request):
        loggin_user_name = UserLogin.objects.get(pk=request.session['member_id']).user_name
        c['user_name'] = loggin_user_name
    
    return render(request, 'game/index.html', c)

def upload_file(request):
    c = {'user_logged_in': logged_in(request)}
    if logged_in(request):
        loggin_user_name = UserLogin.objects.get(pk=request.session['member_id']).user_name
        c['user_name'] = loggin_user_name
        
    else:
        return HttpResponseRedirect('/game')
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            c['form'] = form
            # check to see if the ai title exists
            check_ai_title = UserAiTable.objects.filter(user_ai_title=request.POST['ai_title'])
            if check_ai_title:
                c['error_message'] = 'This ai title already exists'
                c.update(csrf(request))
                return render(request, 'game/upload.html', c)
            
            # save the uploaded file
            post = request.POST
            files = request.FILES
            get_user_name = UserLogin.objects.get(pk=request.session['member_id']).user_name
            
            import string
            import random; random.seed()
            ai_title = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(30))
            handle_uploaded_file(files['ai_code'],
                                 get_user_name + '/' + ai_title)

            # save the file path into the database
            ai = UserAiTable(user_id=request.session['member_id'], user_ai_title=post['ai_title'], user_ai_gen_title=ai_title)
            ai.save()
            c['error_message'] = 'File uploaded successfuly'

            # save the stats table with 0
            stats = UserStats(user_id=request.session['member_id'], user_ai_title=post['ai_title'], user_ai_wins = 0, user_ai_losses = 0, user_ai_draws = 0)
            stats.save()
            return render(request, 'game/upload.html', c)
    else:
        form = UploadFileForm()
    c['form'] = form
    c.update(csrf(request))
    return render(request, 'game/upload.html', c)

def register(request):
    c = {'user_logged_in': logged_in(request)}
    if logged_in(request):
         return HttpResponseRedirect('/game/logout')
     
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        c['form'] = form
        if form.is_valid():
            post = request.POST
            # check if the user exists in the database
            check_user_exists = UserLogin.objects.filter(user_name=post['user_name'])
            if check_user_exists:
                c['error_message'] = "This user name already exists."
                c.update(csrf(request))
                return render(request, 'game/register.html', c)

            # check size of user name
            if len(post['user_name']) < 5:
                c['error_message'] = "Your username must be longer than 5 characters."
                c.update(csrf(request))
                return render(request, 'game/register.html', c)

            # check size of password
            if len(post['password']) < 5:
                c['error_message'] = "Your password must be longer than 5 characters."
                c.update(csrf(request))
                return render(request, 'game/register.html', c)

            # check if passwords match -- for the form
            if post['password'] != post['re_password']:
                c['error_message'] = "Your passwords do not match"
                c.update(csrf(request))
                return render(request, 'game/register.html', c)

            # registeration successful
            import os
            os.system('mkdir %swam/ais/' % (FILE_PATH) + post['user_name'])
            user = UserLogin(user_name=post['user_name'], password=post['password'], email=post['email'])
            user.save()
            return HttpResponseRedirect('/game/login')
    else:
        form = UserRegisterForm()
    c = {'form': form}
    c.update(csrf(request))
    return render(request, 'game/register.html', c)
    
def login(request):
    c = {'user_logged_in': logged_in(request)}
    if logged_in(request):
         return HttpResponseRedirect('/game/logout')
     
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            check_user_exists = UserLogin.objects.filter(user_name=request.POST['user_name'])
            if not check_user_exists:
                form = UserLoginForm()
                c['form'] = form
                c['error_message'] = "This user name does not exists."
                c.update(csrf(request))
                return render(request, 'game/login.html', c)
            
            m = UserLogin.objects.get(user_name=request.POST['user_name'])
            if m.password == request.POST['password']:
                request.session['member_id'] = m.id
                request.session.modified = True
                return  HttpResponseRedirect('/game')
            else:
                c = {'form': form,
                     'error_message': "Your username and password didn't match."}
                c.update(csrf(request))
                return render_to_response('game/login.html', c)
    else:
        form = UserLoginForm()
    c['form'] = form
    c.update(csrf(request))
    return render(request, 'game/login.html', c)

def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    request.session.flush()
    return HttpResponseRedirect("/game")
