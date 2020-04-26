from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComment
from django.contrib import messages

# Create your views here.
def index(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request, 'blog/index.html', context)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post)
    context = {'post': post, 'comments': comments}
    return render(request, 'blog/post.html', context)


def postComment(request):
    if request.method=="POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')        
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno')

        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, 'Your comment has been posted successfully.')
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, 'Your reply has been posted successfully.')
        
    return redirect(f"/blog/{post.slug}")


def createPost(request):
    if request.method=="POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.POST.get('name')
        slug = request.POST.get('slug')

        if author=="":
            messages.error(request, 'Please Login then you can create any NEW-POST!.')
        elif title=="" or content=="" or slug=="":
            messages.error(request, 'All fields are required!.')
        else:
            newpost = Post(title=title, content=content, author=author, slug=slug)
            newpost.save()
            messages.success(request, 'Your New-Post has been saved successfully.')

    return render(request, 'blog/createPost.html')