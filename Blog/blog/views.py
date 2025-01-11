from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from hitcount.views import HitCountDetailView
from hitcount.utils import get_hitcount_model
from datetime import datetime
from .models import Post, Category, Tag, Contact, Comment, FAQ, CustomUser, PasswordResetCode
from .forms import CommentForm, ContactForm, PostForm, CategoryForm, TagForm, FAQForm, UserForm, ProfileUpdateForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import random

def is_admin(user):
    return user.is_authenticated and (user.is_admin or user.is_staff)

def generate_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        User = get_user_model()
        
        try:
            user = User.objects.get(email=email)
            
            # Eski kodları devre dışı bırak
            PasswordResetCode.objects.filter(email=email, is_used=False).update(is_used=True)
            
            # Yeni kod oluştur
            code = generate_code()
            PasswordResetCode.objects.create(email=email, code=code)
            
            # E-posta gönder
            send_mail(
                'Şifre Sıfırlama Kodu',
                f'Şifre sıfırlama kodunuz: {code}\n\nBu kod 30 dakika süreyle geçerlidir.',
                'Blog <adamwarlock628@gmail.com>',
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'Şifre sıfırlama kodu e-posta adresinize gönderildi.')
            return redirect('blog:password_reset_verify')
        except User.DoesNotExist:
            messages.error(request, 'Bu e-posta adresi ile kayıtlı bir kullanıcı bulunamadı.')
    
    return render(request, 'blog/password_reset_request.html')

def password_reset_verify(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = request.POST.get('code')
        
        # Son 30 dakika içinde oluşturulan ve kullanılmamış kodu bul
        reset_code = PasswordResetCode.objects.filter(
            email=email,
            code=code,
            is_used=False,
            created_at__gte=timezone.now() - timezone.timedelta(minutes=30)
        ).first()
        
        if reset_code:
            reset_code.is_used = True
            reset_code.save()
            
            # Kodu session'a kaydet ve yönlendir
            request.session['reset_email'] = email
            return redirect('blog:password_reset_confirm')
        else:
            messages.error(request, 'Geçersiz veya süresi dolmuş kod.')
    
    return render(request, 'blog/password_reset_verify.html')

def password_reset_confirm(request):
    email = request.session.get('reset_email')
    if not email:
        messages.error(request, 'Geçersiz işlem.')
        return redirect('blog:password_reset_request')
    
    User = get_user_model()
    
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Şifreler eşleşmiyor.')
        else:
            try:
                user = User.objects.get(email=email)
                user.set_password(password1)
                user.save()
                
                # Session'ı temizle
                del request.session['reset_email']
                
                messages.success(request, 'Şifreniz başarıyla değiştirildi. Şimdi giriş yapabilirsiniz.')
                return redirect('account_login')
            except User.DoesNotExist:
                messages.error(request, 'Kullanıcı bulunamadı.')
    
    return render(request, 'blog/password_reset_confirm.html')

# Site Views
def post_list(request):
    posts = Post.objects.filter(status='published', published_date__lte=timezone.now())
    
    # Arama sorgusu
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
    
    # Kategori filtresi
    category = request.GET.get('category')
    if category:
        posts = posts.filter(category__slug=category)
    
    # Etiket filtresi
    tag = request.GET.get('tag')
    if tag:
        posts = posts.filter(tags__slug=tag)
    
    posts = posts.order_by('-published_date')
    paginator = Paginator(posts, 10)
    
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    # Popüler yazılar için hit count'u kullan
    popular_posts = Post.objects.filter(status='published').annotate(
        hit_count_value=Count('hit_count')
    ).order_by('-hit_count_value')[:5]
    
    context = {
        'posts': posts,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
        'query': query,
        'popular_posts': popular_posts,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.filter(is_approved=True).order_by('-created_date')
    
    # Hit count'u artır
    hit_count = get_hitcount_model().objects.get_for_object(post)
    hits = hit_count.hits
    hit_count_response = hit_count.increase()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Yorum yapabilmek için giriş yapmalısınız.')
            return redirect('account_login')
        
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Yorumunuz başarıyla gönderildi. Onaylandıktan sonra yayınlanacaktır.')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'hits': hits,
    }
    return render(request, 'blog/post_detail.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published').order_by('-published_date')
    
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'category': category,
        'posts': posts,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    }
    return render(request, 'blog/category_detail.html', context)

def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, status='published').order_by('-published_date')
    
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'tag': tag,
        'posts': posts,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    }
    return render(request, 'blog/tag_detail.html', context)

def contact(request):
    # Popüler yazılar için hit count'u kullan
    popular_posts = Post.objects.filter(status='published').annotate(
        hit_count_value=Count('hit_count')
    ).order_by('-hit_count_value')[:5]
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mesajınız başarıyla gönderildi.')
            return redirect('blog:contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
        'popular_posts': popular_posts,
    }
    return render(request, 'blog/contact.html', context)

def hakkimda(request):
    # Popüler yazılar için hit count'u kullan
    popular_posts = Post.objects.filter(status='published').annotate(
        hit_count_value=Count('hit_count')
    ).order_by('-hit_count_value')[:5]
    
    context = {
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
        'popular_posts': popular_posts,
    }
    return render(request, 'blog/hakkimda.html', context)

def search(request):
    query = request.GET.get('q')
    results = []
    
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query),
            status='published'
        ).order_by('-published_date')
    
    context = {
        'query': query,
        'results': results,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    }
    return render(request, 'blog/search.html', context)

def archive(request):
    # Popüler yazılar için hit count'u kullan
    popular_posts = Post.objects.filter(status='published').annotate(
        hit_count_value=Count('hit_count')
    ).order_by('-hit_count_value')[:5]
    
    posts = Post.objects.filter(status='published').order_by('-created_date')
    years = posts.dates('created_date', 'year')
    months = posts.dates('created_date', 'month')
    
    year = request.GET.get('year')
    month = request.GET.get('month')
    
    if year and month:
        posts = posts.filter(created_date__year=year, created_date__month=month)
    elif year:
        posts = posts.filter(created_date__year=year)
    
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'posts': posts,
        'years': years,
        'months': months,
        'selected_year': year,
        'selected_month': month,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
        'popular_posts': popular_posts,
    }
    return render(request, 'blog/archive.html', context)

def faq(request):
    faqs = FAQ.objects.filter(is_active=True).order_by('order')
    context = {
        'faqs': faqs,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    }
    return render(request, 'blog/faq.html', context)

# Panel Views
@login_required
@user_passes_test(is_admin)
def panel_home(request):
    # İstatistikler
    total_posts = Post.objects.count()
    total_comments = Comment.objects.count()
    total_messages = Contact.objects.count()
    total_categories = Category.objects.count()
    total_tags = Tag.objects.count()
    
    # Son eklenen içerikler
    recent_posts = Post.objects.order_by('-created_date')[:5]
    recent_comments = Comment.objects.order_by('-created_date')[:5]
    recent_messages = Contact.objects.order_by('-created_date')[:5]
    
    # Kategori ve etiket istatistikleri
    categories_with_counts = Category.objects.annotate(post_count=Count('posts'))
    tags_with_counts = Tag.objects.annotate(post_count=Count('posts'))
    
    context = {
        'total_posts': total_posts,
        'total_comments': total_comments,
        'total_messages': total_messages,
        'total_categories': total_categories,
        'total_tags': total_tags,
        'recent_posts': recent_posts,
        'recent_comments': recent_comments,
        'recent_messages': recent_messages,
        'categories_with_counts': categories_with_counts,
        'tags_with_counts': tags_with_counts,
    }
    
    return render(request, 'blog/panel/home.html', context)

@login_required
@user_passes_test(is_admin)
def panel_posts(request):
    posts = Post.objects.all().order_by('-created_date')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/panel/posts/list.html', {'posts': posts, 'is_paginated': paginator.num_pages > 1, 'page_obj': posts})

@login_required
@user_passes_test(is_admin)
def panel_post_add(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, 'Yazı başarıyla eklendi.')
            return redirect('blog:panel_posts')
    else:
        form = PostForm()
    return render(request, 'blog/panel/posts/form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def panel_post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Yazı başarıyla güncellendi.')
            return redirect('blog:panel_posts')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/panel/posts/form.html', {'form': form, 'post': post})

@login_required
@user_passes_test(is_admin)
def panel_post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, 'Yazı başarıyla silindi.')
    return redirect('blog:panel_posts')

@login_required
@user_passes_test(is_admin)
def panel_categories(request):
    categories = Category.objects.annotate(post_count=Count('posts'))
    return render(request, 'blog/panel/categories/list.html', {'categories': categories})

@login_required
@user_passes_test(is_admin)
def panel_category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategori başarıyla eklendi.')
            return redirect('blog:panel_categories')
    else:
        form = CategoryForm()
    return render(request, 'blog/panel/categories/form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def panel_category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategori başarıyla güncellendi.')
            return redirect('blog:panel_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'blog/panel/categories/form.html', {'form': form, 'category': category})

@login_required
@user_passes_test(is_admin)
def panel_category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, 'Kategori başarıyla silindi.')
    return redirect('blog:panel_categories')

@login_required
@user_passes_test(is_admin)
def panel_tags(request):
    tags = Tag.objects.annotate(post_count=Count('posts'))
    return render(request, 'blog/panel/tags/list.html', {'tags': tags})

@login_required
@user_passes_test(is_admin)
def panel_tag_add(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Etiket başarıyla eklendi.')
            return redirect('blog:panel_tags')
    else:
        form = TagForm()
    return render(request, 'blog/panel/tags/form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def panel_tag_edit(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, 'Etiket başarıyla güncellendi.')
            return redirect('blog:panel_tags')
    else:
        form = TagForm(instance=tag)
    return render(request, 'blog/panel/tags/form.html', {'form': form, 'tag': tag})

@login_required
@user_passes_test(is_admin)
def panel_tag_delete(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    tag.delete()
    messages.success(request, 'Etiket başarıyla silindi.')
    return redirect('blog:panel_tags')

@login_required
@user_passes_test(is_admin)
def panel_comments(request):
    comments = Comment.objects.all().order_by('-created_date')
    paginator = Paginator(comments, 20)
    page = request.GET.get('page')
    comments = paginator.get_page(page)
    return render(request, 'blog/panel/comments/list.html', {'comments': comments})

@login_required
@user_passes_test(is_admin)
def panel_comment_edit(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Yorum başarıyla güncellendi.')
            return redirect('blog:panel_comments')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/panel/comments/form.html', {'form': form, 'comment': comment})

@login_required
@user_passes_test(is_admin)
def panel_comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    messages.success(request, 'Yorum başarıyla silindi.')
    return redirect('blog:panel_comments')

@login_required
@user_passes_test(is_admin)
def panel_messages(request):
    messages_list = Contact.objects.all().order_by('-created_date')
    paginator = Paginator(messages_list, 10)
    page = request.GET.get('page')
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)
    return render(request, 'blog/panel/messages/list.html', {'messages': messages})

@login_required
@user_passes_test(is_admin)
def panel_message_view(request, message_id):
    message = get_object_or_404(Contact, id=message_id)
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'blog/panel/messages/view.html', {'message': message})

@login_required
@user_passes_test(is_admin)
def panel_message_delete(request, message_id):
    message = get_object_or_404(Contact, id=message_id)
    message.delete()
    messages.success(request, 'Mesaj başarıyla silindi.')
    return redirect('blog:panel_messages')

@login_required
@user_passes_test(is_admin)
def panel_faqs(request):
    faqs = FAQ.objects.all().order_by('order')
    return render(request, 'blog/panel/faqs/list.html', {'faqs': faqs})

@login_required
@user_passes_test(is_admin)
def panel_faq_add(request):
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'SSS başarıyla eklendi.')
            return redirect('blog:panel_faqs')
    else:
        form = FAQForm()
    return render(request, 'blog/panel/faqs/form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def panel_faq_edit(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    if request.method == 'POST':
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            messages.success(request, 'SSS başarıyla güncellendi.')
            return redirect('blog:panel_faqs')
    else:
        form = FAQForm(instance=faq)
    return render(request, 'blog/panel/faqs/form.html', {'form': form, 'faq': faq})

@login_required
@user_passes_test(is_admin)
def panel_faq_delete(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    faq.delete()
    messages.success(request, 'SSS başarıyla silindi.')
    return redirect('blog:panel_faqs')

@login_required
@user_passes_test(is_admin)
def panel_users(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    paginator = Paginator(users, 20)
    page = request.GET.get('page')
    users = paginator.get_page(page)
    return render(request, 'blog/panel/users/list.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def panel_user_add(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Kullanıcı başarıyla eklendi.')
            return redirect('blog:panel_users')
    else:
        form = UserForm()
    return render(request, 'blog/panel/users/form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def panel_user_edit(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Kullanıcı başarıyla güncellendi.')
            return redirect('blog:panel_users')
    else:
        form = UserForm(instance=user)
    return render(request, 'blog/panel/users/form.html', {'form': form, 'user_obj': user})

@login_required
@user_passes_test(is_admin)
def panel_user_delete(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    messages.success(request, 'Kullanıcı başarıyla silindi.')
    return redirect('blog:panel_users')

@login_required
@user_passes_test(is_admin)
def panel_comment_approve(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.is_approved = True
    comment.save()
    messages.success(request, 'Yorum başarıyla onaylandı.')
    return redirect('blog:panel_comments')

@login_required
def profile_view(request):
    context = {
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    }
    return render(request, 'blog/profile.html', context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profiliniz başarıyla güncellendi.')
            return redirect('blog:profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'form': form,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    }
    return render(request, 'blog/profile_edit.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Şifre değiştikten sonra oturumu güncelle
            update_session_auth_hash(request, user)
            messages.success(request, 'Şifreniz başarıyla değiştirildi!')
            return redirect('blog:profile')
        else:
            messages.error(request, 'Lütfen aşağıdaki hataları düzeltin.')
    else:
        form = PasswordChangeForm(request.user)
    
    context = {
        'form': form,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    }
    return render(request, 'blog/change_password.html', context)
