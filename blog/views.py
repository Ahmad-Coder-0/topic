from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import HttpResponse
from django.core.paginator import Paginator
from .forms import *
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.db.models.functions import Greatest


def home_page(request):
    return render(request, 'pages/home_page.html')


def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 3)
    page_num = request.GET.get('page', 1)
    page = paginator.get_page(page_num)
    posts = page
    context = {
        'posts': posts
    }
    return render(request, 'pages/post_list.html', context)


def post_detail(request, id):
    post = get_object_or_404(Post.published.all(), pk=id)
    form = CommentForm()
    comment = post.comments.filter(active=True)
    context = {
        'post': post,
        'form': form,
        'comment': comment
    }
    return render(request, 'pages/post_detail.html', context)


def ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Ticket.objects.create(
                name=cd['name'],
                message=cd['message'],
                phone=cd['phone'],
                email=cd['email'],
                subject=cd['subject'],
            )
            return redirect('blog:ticket')
    else:
        form = TicketForm()
    context = {
        'form': form
    }
    return render(request, 'forms/ticket.html', context)


@require_POST
def commnet_post(request, post_id):
    post = get_object_or_404(Post.published.all(), id=post_id)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    else:
        form = CommentForm()
    context = {
        'form': form,
        'post': post,
        'comment': comment,
    }
    return render(request, 'forms/comment_post.html', context)


def createpost(request):
    post = None
    created = False
    form = PostForm(data=request.POST)
    if form.is_valid():
        post = form.save()
        # return HttpResponse("<h1><center>پست ایجاد شد و پس از بررسی مدیران سایت انتشار خواهد شد!</center></h1>")
        created = True
    else:
        form = PostForm()

    context = {
        'form': form,
        'post': post,
        'created': created
    }
    return render(request, 'forms/postform.html', context)


def search_post(request):
    # print(request.GET.get('query'))
    query = None
    results = []
    found = False
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results1 = Post.published.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            ).annotate(
                similarity=Greatest(
                    TrigramSimilarity('title', query),
                    TrigramSimilarity('description', query),
                )
            ).order_by('-similarity')
            results2 = Image.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            ).annotate(
                similarity=Greatest(
                    TrigramSimilarity('title', query),
                    TrigramSimilarity('description', query),
                )
            ).order_by('-similarity')
            results = list(results1) + list(results2)

            results = sorted(results, key=lambda x: x.similarity, reverse=True)
            found = bool(results)
            paginator = Paginator(results, 3)
            num_page = request.GET.get('page', 1)
            page = paginator.get_page(num_page)
            results = page

    context = {
        'query': query,
        'results': results,
        'found': found,
    }

    return render(request, 'pages/searchpost.html', context)
