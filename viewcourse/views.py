from django.shortcuts import render
from django.shortcuts import redirect
from .models import addcourse
from .forms import PostForm
from django.shortcuts import render, get_object_or_404

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

def deliver(request):
    dada = "dadada"
    return render(request, 'viewcourse/course_list.html', {'dada': dada,})
