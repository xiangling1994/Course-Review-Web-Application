from django.shortcuts import render
from django.shortcuts import redirect
from .models import addcourse
from .forms import PostForm, CommentForm
from django.shortcuts import render, get_object_or_404,render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import requires_csrf_token


# Create your views here.
def course_list(request):
    adds = addcourse.objects.order_by('courseid')
    return render(request, 'viewcourse/course_list.html', {'adds':adds})

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
    post = get_object_or_404(addcourse, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.published_date = timezone.now()
            comment.save()
            return redirect('viewcourse/course_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'viewcourse/new_comment.html', {'form': form})

def deliver(request):
    dada = "dadada"
    return render(request, 'viewcourse/course_list.html', {'dada': dada,})


@requires_csrf_token
def loginview(request):
    c = {}
    return render_to_response('login.html',c)

def auth_and_login(request, onsuccess='/', onfail='/login/'):
    user = authenticate(username=request.POST['email'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        return redirect(onsuccess)
    else:
        return redirect(onfail)


def sign_up_in(request):
    post = request.POST
    if  post=={}:
        return redirect("/signup/")
    if not user_exists(post['email']):
        user = create_user(username=post['email'], email=post['email'], password=post['password'])
        return redirect("/")
    else:
        return auth_and_login(request)


def create_user(username, email, password):
    user = User(username=username, email=email)
    user.set_password(password)
    user.save()
    return user

def user_exists(username):
    user_count = User.objects.filter(username=username).count()
    if user_count == 0:
        return False
    return True
