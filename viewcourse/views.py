from django.shortcuts import render
from django.shortcuts import redirect
import csv

from .models import course, comment, account, professor, vote, judge
from .forms import PostForm, CommentForm, AccountForm, LoginForm
from .forms import RatingFormHelpfulness, RatingFormClarity, RatingFormEasiness, RatingFormTextbook
from .forms import SearchForm, DeleteForm, ChangePasswordForm
from django.shortcuts import render, get_object_or_404
from datetime import timedelta as tdelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password



# Create your views here.

#view to show the course list which is also the home page
def course_list(request):
    #initial courses
    courses = None
    collection = None
    university = ['University']
    subject = ['Subject']
    #retrieve all the course objects
    all_courses = course.objects.all()
    #collect all the universities' names
    for x in all_courses:
        if x.university not in university:
            university.append(x.university)

    if request.method == 'GET':
        #get selector content
        render_search = SearchForm(request.GET)
        university_pick = request.GET.get('university', None)
        subject_pick = request.GET.get('subject', None)
        #if all the fields are filled
        if render_search.is_valid():
            #search the courseid
            input = render_search.cleaned_data['search_handle']
            input = input.lower()
            courses  = course.objects.all()
            displaycourse=[]
            for x in courses:
                if input in x.courseid.lower():
                    displaycourse.append(x)
            #if there is no university selection, list the search result
            if university_pick == 'University':
                courses = displaycourse
            #if there is university selection, choose the course of that university
            else:
                courses = []
                for x in displaycourse:
                    if x.university == university_pick:
                        courses.append(x)
                #collect all the subjects of that university
                selected_courses = []
                for a in all_courses:
                    if a.university == university_pick:
                        selected_courses.append(a)
                for b in selected_courses:
                    if b.subject not in subject:
                        subject.append(b.subject)
        elif university_pick == 'University':
            #if there is no university selection, show nothing
            courses = None
        else:
            #if there is only university selection, collect the subjects
            selected_courses = []
            for a in all_courses:
                if a.university == university_pick:
                    selected_courses.append(a)
            for b in selected_courses:
                if b.subject not in subject:
                    subject.append(b.subject)
            collection = university_pick
            #show no courses if there is no subject selection
            if subject_pick != 'Subject':
                #show the courses of that subject if there is subject selection
                courses = course.objects.order_by('courseid')
                displaycourse = []
                for x in courses:
                    if university_pick == x.university:
                        displaycourse.append(x)
                courses = displaycourse
                courses = []
                for y in displaycourse:
                    if subject_pick in y.subject:
                        courses.append(y)
    context = {
        'courses':courses,
        'university': university,
        'subject': subject,
        'university_pick': university_pick,
        'subject_pick': subject_pick,
        'collection': collection
    }
    return render(request, 'viewcourse/course_list.html', context)


#the view for showing the featured courses
def collection(request):
    #get the parameter universiity
    uni = request.GET['para']
    selected_courses = course.objects.filter(university = uni)
    easy_profs = []
    helpful_profs = []
    #search the whole model and find the target courses
    for a in selected_courses:
        profs = a.professors.all()
        for x in profs:
            if x.easiness >= 4:
                easy_profs.append(x)
            if x.helpfulness >= 4:
                    helpful_profs.append(x)
    return render(request, 'viewcourse/collection.html', {'easy_profs':easy_profs, 'helpful_profs':helpful_profs})


#view to show the course detail
def course_detail(request, pk):
    detail = get_object_or_404(course, pk=pk)
    comments = detail.comments.all()

    return render(request, 'viewcourse/course_detail.html', {'detail':detail})


#view to agree a comment
def agree(request, pk, cid):
    aid = request.session.get('aid', None)
    a = account.objects.get(id=aid)
    account_judges = a.judges.all()

    detail = get_object_or_404(course, pk=pk)
    course_comment = detail.comments.all()
    c = course_comment.get(id = cid)

    #check if the user agree before
    if account_judges:
        for aj in account_judges:
            if aj.commentid == c.id:
                return redirect('course_detail', pk=pk)
    #add new judge model if the user did not
    naj = judge.objects.create(account = a, user = c.user, commentid = c.id)

    #change the agree model
    a = c.agree
    c.agree = a+1
    c.save()
    response = redirect('course_detail', pk = pk)
    return response

#view to disagree a comment
def disagree(request, pk, cid):
    aid = request.session.get('aid', None)
    a = account.objects.get(id=aid)
    account_judges = a.judges.all()

    detail = get_object_or_404(course, pk=pk)
    course_comment = detail.comments.all()
    c = course_comment.get(id = cid)

    #check if the user disagree before
    if account_judges:
        for aj in account_judges:
            if aj.commentid == c.id:
                return redirect('course_detail', pk=pk)
    #add new judge model if the user did not
    naj = judge.objects.create(account = a, user = c.user, commentid = c.id)

    #change the disagree model
    d = c.disagree
    c.disagree = d+1
    c.save()
    response = redirect('course_detail', pk = pk)
    return response


#view to add a new course(not be shown in the template)
def course_new(request):
    #post the form if it is valid
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('course_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'viewcourse/post_edit.html', {'form': form})


#view to create a new comment
def comment_new(request, pk):
    username = request.session.get('account_un', None)
    c = get_object_or_404(course, pk=pk)
    #post the form if it is valid
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
    return render(request, 'viewcourse/new_comment.html', {'form': form})


#view to rate a prof of a course
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

            aid = request.session.get('aid', None)
            a = account.objects.get(id=aid)
            account_votes = a.votes.all()

            #restict users to vote once by checking the vote model
            if account_votes:
                for v in account_votes:
                    if v.prof == current_professor[0].full_name and v.cid == c.courseid:
                        return redirect('course_detail', pk=c.pk)
                new_vote = vote.objects.create(account = a, prof=current_professor[0], cid = c.courseid)
            else:
                new_vote = vote.objects.create(account = a, prof=current_professor[0], cid = c.courseid)

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
            cp = current_professor[0]

            cp.helpfulness = helpfulness_average_new
            cp.clarity = clarity_average_new
            cp.easiness = easiness_average_new
            cp.textbook = textbook_average_new
            cp.ratetimes = times + 1


            #compute criteria average
            criteria_average = (helpfulness_average_new + clarity_average_new + easiness_average_new + textbook_average_new) / 4.0

            # compute new overall rating
            overall_rating_new = criteria_average

            #save new overall rating value to the database
            cp.rating = overall_rating_new
            cp.save()

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
            aobject = account.objects.filter(username = username)
            if aobject is None:
                return redirect('regist')
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
    return render(request, 'viewcourse/regist.html', {'form':form})


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
    return render(request, 'viewcourse/login.html', {'form':form})


#profile page
def index(request):
    aid = request.session.get('aid', None)
    a = account.objects.get(id=aid)

    #load the user's comments and add delete function
    comments = comment.objects.all()
    user_comments = comments.filter(user=a.username)
    if request.method == 'GET':
        render_delete = DeleteForm(request.GET)
        if render_delete.is_valid():
            comment.objects.filter(id = render_delete.cleaned_data['delete_handle']).delete()

    return render(request, 'viewcourse/index.html', {'a':a, 'user_comments':user_comments})


#view to logout
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


#view to change password
def change_password(request):
    aid = request.session.get('aid', None)
    a = account.objects.get(id=aid)
    #change the user model
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            a.password = make_password(password, None, 'pbkdf2_sha256')
            a.save()
            return redirect('index')
        else:
            return redirect('index')
    else:
        form = LoginForm()

    return render(request, 'viewcourse/change_password.html', {'form':form})
