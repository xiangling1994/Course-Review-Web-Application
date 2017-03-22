from django.shortcuts import render
from django.shortcuts import redirect

from .models import addcourse, comment, user, professor, ratingCriteria
from .forms import PostForm, CommentForm, UserForm, LoginForm, RatingFormHelpfulness, RatingFormClarity, RatingFormEasiness, RatingFormTextbook
from django.shortcuts import render, get_object_or_404
from datetime import timedelta as tdelta
from django.utils import timezone



# Create your views here.
def course_list(request):
    adds = addcourse.objects.order_by('courseid')
    username = request.COOKIES.get('username','')
    return render(request, 'viewcourse/course_list.html', {'adds':adds, 'username':username})

def course_detail(request, pk):
    detail = get_object_or_404(addcourse, pk=pk)
    username = request.COOKIES.get('username','')
    return render(request, 'viewcourse/course_detail.html', {'detail':detail, 'username':username})

def course_new(request):
    username = request.COOKIES.get('username','')
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('course_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'viewcourse/post_edit.html', {'form': form, 'username':username})

def comment_new(request, pk):
    course = get_object_or_404(addcourse, pk=pk)
    username = request.COOKIES.get('username','')
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.course = course
            comment.user = username
            comment.published_date = timezone.now()
            comment.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CommentForm()
    return render(request, 'viewcourse/new_comment.html', {'form': form, 'username':username})


def rating(request, pk, profid):
    username = request.COOKIES.get('username','')
    course = get_object_or_404(addcourse, pk=pk)
    #course_id = course.courseid
    current_professor = course.professors.all().filter(id=profid)
    criterias = course.criterias.all().filter(prof=current_professor[0])

    #retrieve current overall rating for the professor
    overall_rating_db = current_professor[0].rating

    #retireve current criteria ratings values from the database
    helpfulness_db_val = criterias[0].helpfulness
    clarity_db_val = criterias[0].clarity
    easiness_db_val = criterias[0].easiness
    textbook_db_val = criterias[0].textbook
    times = criterias[0].ratetimes
    #helpfulness_average_new = 0

    if request.method == "POST":
        form_helpfulness = RatingFormHelpfulness(request.POST)
        form_clarity = RatingFormClarity(request.POST)
        form_easiness = RatingFormEasiness(request.POST)
        form_textbook = RatingFormTextbook(request.POST)
        if form_helpfulness.is_valid() and form_clarity.is_valid() and form_easiness.is_valid() and form_textbook.is_valid():

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
            ratingCriteria.objects. filter(course=criterias[0].course, prof=criterias[0].prof).update(helpfulness=helpfulness_average_new)
            ratingCriteria.objects. filter(course=criterias[0].course, prof=criterias[0].prof).update(clarity=clarity_average_new)
            ratingCriteria.objects. filter(course=criterias[0].course, prof=criterias[0].prof).update(easiness=easiness_average_new)
            ratingCriteria.objects. filter(course=criterias[0].course, prof=criterias[0].prof).update(textbook=textbook_average_new)
            ratingCriteria.objects. filter(course=criterias[0].course, prof=criterias[0].prof).update(ratetimes=times + 1)

            #compute criteria average
            criteria_average = (helpfulness_average_new + clarity_average_new + easiness_average_new + textbook_average_new) / 4.0

            # compute new overall rating
            overall_rating_new = criteria_average

            #save new overall rating value to the database
            professor.objects. filter(course=criterias[0].course, full_name=current_professor[0].full_name).update(rating=overall_rating_new)

            return redirect('course_detail', pk=course.pk)
    else:
        form_helpfulness = RatingFormHelpfulness()
        form_clarity = RatingFormClarity()
        form_easiness = RatingFormEasiness()
        form_textbook = RatingFormTextbook()
    criteria = criterias[0]
    context = {
        'criteria':criteria,
        'form_helpfulness':form_helpfulness,
        'form_clarity':form_clarity,
        'form_textbook':form_textbook,
        'form_easiness':form_easiness,
        'current_professor':current_professor,
        'username':username
    }
    return render(request, 'viewcourse/rating.html', context)


def regist(request):
    username = request.COOKIES.get('username','')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            #get form data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            #add them to the database
            user.objects.create(username= username, password=password, email = email)
            response = redirect('course_list')
            response.set_cookie('username',username,3600)
            return response
    else:
        form = UserForm()
    return render(request, 'viewcourse/regist.html',{'form':form, 'username':username})


def login(request):
    username = request.COOKIES.get('username','')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            #retrieve data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #compare with forms
            u = user.objects.filter(username__exact = username, password__exact = password)
            if u:
                #success
                response = redirect('index')
                #add cookie
                response.set_cookie('username',username,3600)
                return response
            else:
                #fail
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'viewcourse/login.html',{'form':form, 'username':username})


def index(request):
    username = request.COOKIES.get('username','')
    return render(request, 'viewcourse/index.html' ,{'username':username})


def logout(request):
    response = redirect('login')
    #clear cookie
    response.delete_cookie('username')
    return response


def getCookie(request):
    username = request.COOKIES.get('username', '')
    return username
