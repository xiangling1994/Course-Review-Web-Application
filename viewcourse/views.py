from django.shortcuts import render
from django.shortcuts import redirect

from .models import addcourse, comment, user
from .forms import PostForm, CommentForm, UserForm
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
    return render(request, 'viewcourse/course_detail.html', {'detail':detail})

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
    return render(request, 'viewcourse/new_comment.html', {'form': form})



def regist(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            #get form data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #add them to the database
            user.objects.create(username= username, password=password)
            response = redirect('course_list')
            response.set_cookie('username',username,3600)
            return response
    else:
        form = UserForm()
    return render(request, 'viewcourse/regist.html',{'form':form})


def login(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
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
        form = UserForm()
    return render(request, 'viewcourse/login.html',{'form':form})


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
