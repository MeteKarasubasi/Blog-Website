from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Site URLs
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('kategori/<slug:slug>/', views.category_detail, name='category_detail'),
    path('etiket/<slug:slug>/', views.tag_detail, name='tag_detail'),
    path('iletisim/', views.contact, name='contact'),
    path('hakkimda/', views.hakkimda, name='hakkimda'),
    path('arama/', views.search, name='search'),
    path('arsiv/', views.archive, name='archive'),
    path('sss/', views.faq, name='faq'),
    
    # Panel URLs
    path('panel/', views.panel_home, name='panel_home'),
    
    # Yazı Yönetimi
    path('panel/yazilar/', views.panel_posts, name='panel_posts'),
    path('panel/yazi/ekle/', views.panel_post_add, name='panel_post_add'),
    path('panel/yazi/<int:post_id>/', views.panel_post_edit, name='panel_post_edit'),
    path('panel/yazi/<int:post_id>/sil/', views.panel_post_delete, name='panel_post_delete'),
    
    # Kategori Yönetimi
    path('panel/kategoriler/', views.panel_categories, name='panel_categories'),
    path('panel/kategori/ekle/', views.panel_category_add, name='panel_category_add'),
    path('panel/kategori/<int:category_id>/', views.panel_category_edit, name='panel_category_edit'),
    path('panel/kategori/<int:category_id>/sil/', views.panel_category_delete, name='panel_category_delete'),
    
    # Etiket Yönetimi
    path('panel/etiketler/', views.panel_tags, name='panel_tags'),
    path('panel/etiket/ekle/', views.panel_tag_add, name='panel_tag_add'),
    path('panel/etiket/<int:tag_id>/', views.panel_tag_edit, name='panel_tag_edit'),
    path('panel/etiket/<int:tag_id>/sil/', views.panel_tag_delete, name='panel_tag_delete'),
    
    # Yorum Yönetimi
    path('panel/yorumlar/', views.panel_comments, name='panel_comments'),
    path('panel/yorum/<int:comment_id>/', views.panel_comment_edit, name='panel_comment_edit'),
    path('panel/yorum/<int:comment_id>/sil/', views.panel_comment_delete, name='panel_comment_delete'),
    path('panel/yorum/<int:comment_id>/onayla/', views.panel_comment_approve, name='panel_comment_approve'),
    
    # İletişim Mesajları
    path('panel/mesajlar/', views.panel_messages, name='panel_messages'),
    path('panel/mesaj/<int:message_id>/', views.panel_message_view, name='panel_message_view'),
    path('panel/mesaj/<int:message_id>/sil/', views.panel_message_delete, name='panel_message_delete'),
    
    # SSS Yönetimi
    path('panel/sss/', views.panel_faqs, name='panel_faqs'),
    path('panel/sss/ekle/', views.panel_faq_add, name='panel_faq_add'),
    path('panel/sss/<int:faq_id>/', views.panel_faq_edit, name='panel_faq_edit'),
    path('panel/sss/<int:faq_id>/sil/', views.panel_faq_delete, name='panel_faq_delete'),
    
    # Kullanıcı Yönetimi
    path('panel/kullanicilar/', views.panel_users, name='panel_users'),
    path('panel/kullanici/ekle/', views.panel_user_add, name='panel_user_add'),
    path('panel/kullanici/<int:user_id>/', views.panel_user_edit, name='panel_user_edit'),
    path('panel/kullanici/<int:user_id>/sil/', views.panel_user_delete, name='panel_user_delete'),
    
    # Profil URL'leri
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/change-password/', views.change_password, name='change_password'),
    
    # Şifre Sıfırlama URL'leri
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/verify/', views.password_reset_verify, name='password_reset_verify'),
    path('password-reset/confirm/', views.password_reset_confirm, name='password_reset_confirm'),
]