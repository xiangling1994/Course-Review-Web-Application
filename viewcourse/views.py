from django.shortcuts import render
from django.shortcuts import redirect

from .models import course, comment, account, professor
from .forms import PostForm, CommentForm, AccountForm, LoginForm, RatingFormHelpfulness, RatingFormClarity, RatingFormEasiness, RatingFormTextbook, SearchForm, DeleteForm
from django.shortcuts import render, get_object_or_404
from datetime import timedelta as tdelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password



# Create your views here.
def course_list(request):
    courses = course.objects.order_by('courseid')
    if request.method == 'GET':
        render_search = SearchForm(request.GET)
        if render_search.is_valid():
            input = render_search.cleaned_data['search_handle']
            input =input.lower()
            courses  = course.objects.all()
            displaycourse=[]
            for x in courses:
                if input in x.courseid.lower():
                    displaycourse.append(x)
            courses = displaycourse
        else:
            courses = course.objects.order_by('courseid')
    return render(request, 'viewcourse/course_list.html', {'courses':courses})


def course_detail(request, pk):
    username = request.session.get('account_un', None)
    detail = get_object_or_404(course, pk=pk)
    if request.method == 'GET':
        render_delete = DeleteForm(request.GET)
        if render_delete.is_valid():
            comment.objects.filter(id = render_delete.cleaned_data['delete_handle']).delete()
    return render(request, 'viewcourse/course_detail.html', {'detail':detail, 'username': username})


def course_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('course_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'viewcourse/post_edit.html', {'form': form})

def comment_new(request, pk):
    c = get_object_or_404(course, pk=pk)
    username = request.session.get('account_un', None)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.course = c
            comment.user = username
            comment.published_date = timezone.now()
            comment.save()
            return redirect('course_detail', pk=c.pk)
    else:
        form = CommentForm()
    return render(request, 'viewcourse/new_comment.html', {'form': form, 'username':username})


def rating(request, pk, profid):
    c = get_object_or_404(course, pk=pk)
    #course_id = course.courseid
    current_professor = c.professors.all().filter(id=profid)

    #retrieve current overall rating for the professor
    overall_rating_db = current_professor[0].rating

    #retireve current criteria ratings values from the database
    helpfulness_db_val = current_professor[0].helpfulness
    clarity_db_val = current_professor[0].clarity
    easiness_db_val = current_professor[0].easiness
    textbook_db_val = current_professor[0].textbook
    times = current_professor[0].ratetimes
    #helpfulness_average_new = 0

    if request.method == "POST":
        form_helpfulness = RatingFormHelpfulness(request.POST)
        form_clarity = RatingFormClarity(request.POST)
        form_easiness = RatingFormEasiness(request.POST)
        form_textbook = RatingFormTextbook(request.POST)
        if form_helpfulness.is_valid() and form_clarity.is_valid() and form_easiness.is_valid() and form_textbook.is_valid():

            #create a key for the user
            username = request.session.get('account_un', None)
            key = username + current_professor[0].course.courseid + current_professor[0].full_name
            #check if the user voted before by searching sessions
            voted = request.session.get(key, None)
            if voted:
                return redirect('course_detail', pk=c.pk)
            else:
                request.session[key] = 1

            #retrieve radio button selections
            rating_value_helpfulness = form_helpfulness.cleaned_data['rating_field_helpfulness']
            rating_value_clarity = form_clarity.cleaned_data['rating_field_clarity']
            rating_value_easiness = form_easiness.cleaned_data['rating_field_easiness']
            rating_value_textbook = form_textbook.cleaned_data['rating_field_textbook']

            #compute new rating value by getting the average of the sum for each of them
            helpfulness_average_new = (float(rating_value_helpfulness) + float(helpfulness_db_val) * times) / (times + 1)
            clarity_average_new = (float(rating_value_clarity) + float(clarity_db_val) * times) / (times + 1)
            easiness_average_new = (float(rating_value_easiness) + float(easiness_db_val) * times) / (times + 1)
            textbook_average_new = (float(rating_value_textbook) + float(textbook_db_val) * times) / (times + 1)

            #save new values to the database
            professor.objects. filter(course=current_professor[0].course).update(helpfulness=helpfulness_average_new)
            professor.objects. filter(course=current_professor[0].course).update(clarity=clarity_average_new)
            professor.objects. filter(course=current_professor[0].course).update(easiness=easiness_average_new)
            professor.objects. filter(course=current_professor[0].course).update(textbook=textbook_average_new)
            professor.objects. filter(course=current_professor[0].course).update(ratetimes=times + 1)

            #compute criteria average
            criteria_average = (helpfulness_average_new + clarity_average_new + easiness_average_new + textbook_average_new) / 4.0

            # compute new overall rating
            overall_rating_new = criteria_average

            #save new overall rating value to the database
            professor.objects. filter(course=current_professor[0].course).update(rating=overall_rating_new)

            return redirect('course_detail', pk=c.pk)
    else:
        form_helpfulness = RatingFormHelpfulness()
        form_clarity = RatingFormClarity()
        form_easiness = RatingFormEasiness()
        form_textbook = RatingFormTextbook()
    context = {
        'form_helpfulness':form_helpfulness,
        'form_clarity':form_clarity,
        'form_textbook':form_textbook,
        'form_easiness':form_easiness,
        'current_professor':current_professor[0],
    }
    return render(request, 'viewcourse/rating.html', context)


def regist(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            #get form data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            #encrypt the password and add them to the database
            password = make_password(password, None, 'pbkdf2_sha256')
            new_account = account.objects.create(username= username, password=password, email = email)
            response = redirect('course_list')
            response.set_cookie('username',username,3600)
            request.session['account_un'] = new_account.username
            request.session['aid'] = new_account.id
            return response
    else:
        form = AccountForm()
    return render(request, 'viewcourse/regist.html',{'form':form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            #retrieve data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #compare with forms
            acc = account.objects.filter(username=username)
            if acc:
                a = acc[0]
                passwd = a.password
                b = check_password(password, passwd)
                if b:
                    #success
                    response = redirect('course_list')
                    #add cookie and session
                    response.set_cookie('username',username,3600)
                    request.session['account_un'] = a.username
                    request.session['aid'] = a.id
                    return response
                else:
                    #fail
                    return redirect('login')
            else:
                #fail
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'viewcourse/login.html',{'form':form})


def index(request):
    aid = request.session.get('aid', None)
    a = account.objects.get(id=aid)
    return render(request, 'viewcourse/index.html' ,{'a':a})


def logout(request):
    response = redirect('login')
    #clear cookie and session
    response.delete_cookie('username')
    try:
        del request.session['account_un']
        del request.session['aid']
    except KeyError:
        pass
    return response
