from django.shortcuts import render, get_object_or_404
from .forms import CommentForm
from .models import Post
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Обробка додавання коментаря
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # Створюємо, але поки не зберігаємо в базу
            comment.post = post  # Прив'язуємо до поточного поста
            comment.author = request.user  # Прив'язуємо до того, хто зараз залогінений
            comment.save()  # Тепер зберігаємо!
            return redirect('post_detail', pk=post.pk)  # Перезавантажуємо сторінку
    else:
        form = CommentForm()  # Якщо це просто перегляд сторінки - показуємо порожню форму

    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Одразу робимо вхід після реєстрації
            return redirect('post_list') # Перекидаємо на головну
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def api_posts(request):
    # Дістаємо всі пости, але беремо тільки їхні ID, заголовки та текст
    posts = list(Post.objects.values('id', 'title', 'content'))
    return JsonResponse({'posts': posts})