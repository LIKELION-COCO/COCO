from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import JsonResponse
import os

def home(request, category_name=None):
    townblog = TownBlog.objects.filter(town=request.user.town).first()
    blog = Blog.objects.filter(townblog=townblog)
    blog = blog.order_by('-created_at')
    
    if category_name:
        blog = blog.filter(category=category_name)

    search_query = request.GET.get('searched', '')
    if search_query:
        blog = blog.filter(Q(title__contains=search_query) | Q(content__contains=search_query))

    paginator = Paginator(blog, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'delivery_blogs': page_obj, 'searched': search_query})


from django.http import JsonResponse

def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blog.update_counter

    # 좋아요 수와 좋아요 상태 업데이트
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            blog.is_liked = blog.likes.filter(user=request.user).exists()
        else:
            blog.is_liked = False
        blog.like_count = blog.likes.count()

        data = {
            'like_count': blog.like_count,
            'is_liked': blog.is_liked,
        }
        return JsonResponse(data)

    # 초기 데이터 추가
    initial_data = {
        'like_count': blog.likes.count(),
        'is_liked': blog.likes.filter(user=request.user).exists() if request.user.is_authenticated else False,
    }

    return render(request, 'detail.html', {'blog': blog, 'initial_data': initial_data})



def new(request, err_message =''):
    print(err_message)
    return render(request,'new.html', {'err_message':err_message})

def create(request):
    if request.method == 'POST':
        if not request.POST.get('title') or not request.POST.get('content'):
            err_message = '제목과 내용을 전부 입력해주세요'
            return JsonResponse({'error': err_message}, status=400)
        townblog = TownBlog.objects.get(town=request.user.town)
        new_blog = Blog()
        new_blog.townblog = townblog
        new_blog.user = request.user 
        new_blog.title = request.POST.get('title')
        new_blog.content = request.POST.get('content')
        new_blog.category = request.POST.get('category')
        new_blog.image = request.FILES.get('image')
        new_blog.save()
        return redirect('blog:detail', new_blog.id)
        
    return redirect('blog:home')

def edit(request, blog_id):
    edit_blog = Blog.objects.get(id=blog_id)
    return render(request, 'edit.html',{'edit_blog':edit_blog})

def update(request, blog_id):
    if not request.POST.get('title') or not request.POST.get('content'):
            err_message = '제목과 내용을 전부 입력해주세요'
            return JsonResponse({'error': err_message}, status=400)
    old_blog = get_object_or_404(Blog, pk=blog_id)
    old_blog.title = request.POST.get('title')
    old_blog.content = request.POST.get('content')
    old_blog.category = request.POST.get('category')
    if request.FILES.get('image'):
        if old_blog.image:
            delete_image(old_blog.image.path)
        old_blog.image = request.FILES.get('image')
    old_blog.save()
    return redirect('blog:detail', old_blog.id)

def delete(request, blog_id):
    delete_blog = get_object_or_404(Blog, pk=blog_id)
    if delete_blog.image:
        delete_image(delete_blog.image.path)
    delete_blog.delete()
    return redirect('blog:home')

def add_comment(request, blog_id):
    blog=get_object_or_404(Blog, pk=blog_id)
    if request.method == 'POST':
        blog=get_object_or_404(Blog, pk=blog_id)
        comment_text = request.POST.get('comment_text')
        user = request.user
        comment = BlogComment(blog=blog, user=user, comment_text=comment_text)
        comment.save()
    return redirect('blog:detail', blog.id)

def update_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(BlogComment, pk=comment_id)
        comment.comment_text = request.POST.get('comment_text')
        comment.save()
    return redirect('blog:detail', comment.blog.id)

def delete_comment(request, comment_id):
    comment = get_object_or_404(BlogComment, pk=comment_id)
    blog_id = comment.blog.id
    comment.delete()
    return redirect('blog:detail', blog_id)

def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    user = request.user
    
    if blog.likes.filter(user=user).exists():
        liked = BlogLike.objects.get(blog=blog, user=user)
        liked.delete()
    else:
        liked = BlogLike(blog=blog, user=user)
        liked.save()

    return redirect('blog:detail', blog_id)

def delete_image(path):
    # 이미지 파일 삭제
    if os.path.exists(path):
        os.remove(path)
