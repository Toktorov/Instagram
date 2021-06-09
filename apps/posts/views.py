from django.shortcuts import render, redirect
from apps.posts.models import Post, PostImage, Like
from apps.comments.models import Comment
from apps.posts.forms import PostForm, PostImageForm
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from apps.tags.models import Tag
from django.db.models import Q



def index(request, id=id):
    posts = Post.objects.all()
    if 'key_word' in request.GET:
        key = request.GET.get('words')
        posts = Post.objects.filter(Q(tag__title__icontains=key) |
                                    Q(owner__username__icontains=key))
    if 'comment' in request.POST:
        id = request.POST.get('post_id')
        post = Post.objects.get(id=id)
        text = request.POST.get('comment_text')
        comment = Comment.objects.create(text=text, post=post, user=request.user)
        return redirect('index')
    
    if 'likes' in request.POST:
        id = request.POST.get('post_id')
        post_object = Post.objects.get(id=id)
        try:
            like = Like.objects.get(user=request.user, post = post_object)
            like.delete()
        except:
            Like.objects.create(user=request.user, post=post_object)
    return render(request, 'posts/index.html', {"posts": posts})
    

def create(request):
    form = PostForm(request.POST or None)
    PostImageFormSet = inlineformset_factory(Post, PostImage, form=PostImageForm, extra=1)
    if request.method == 'POST':
        if form.is_valid():
            post = Post()
            post.owner = request.user
            post.description = form.cleaned_data['description']
            post.save()
            tags = form.cleaned_data['tag']
            for tag in tags.split(" "):
                obj, created = Tag.objects.get_or_create(title=tag)
                post.tag.add(obj)
            formset = PostImageFormSet(request.POST, request.FILES, instance=post)
            if formset.is_valid():
                formset.save()
            return redirect('index')
    formset = PostImageFormSet()
    return render(request, 'posts/create.html', locals())


def detail(request, id):
    post = Post.objects.get(id=id)
    return render(request, 'posts/detail.html', {"post": post})
    


def update(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post.image = form.cleaned_data['image']
            post.description = form.cleaned_data['description']
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'posts/update.html', {'form': form})


def delete(request, id):
    if request.method == 'POST':
        post = Post.objects.get(id=id)
        post.delete()
        return redirect('index')
    return render(request, 'posts/delete.html')


def get_profile(request, id):
    profile = User.objects.get(id=id)
    return render(request, 'profile.html', {'profile': profile})


