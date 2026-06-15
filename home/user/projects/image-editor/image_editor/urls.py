"""
URL configuration for image_editor project.
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.conf import settings
from django.conf.urls.static import static
from editor import views
from editor import views_auth

urlpatterns = [
    path('', lambda r: HttpResponseRedirect('/admin/')),
    path('admin/', admin.site.urls),
    # 认证
    path('api/auth/register/', views_auth.register, name='register'),
    path('api/auth/login/', views_auth.login, name='login'),
    path('api/auth/refresh/', views_auth.refresh_token, name='refresh_token'),
    path('api/auth/me/', views_auth.me, name='me'),
    path('api/auth/update/', views_auth.update_profile, name='update_profile'),
    # 业务
    path('api/contract/submit/', views.submit_contract, name='submit_contract'),
    path('api/order/submit/', views.submit_order, name='submit_order'),
    path('api/categories/', views.get_categories, name='get_categories'),
    path('api/products/', views.get_products, name='get_products'),
    path('api/cases/', views.get_cases, name='get_cases'),
    path('api/partners/', views.get_partners, name='get_partners'),
    path('api/testimonials/', views.get_testimonials, name='get_testimonials'),
    path('api/workshops/', views.get_workshops, name='get_workshops'),
    path('api/crafts/', views.get_crafts, name='get_crafts'),
    path('api/certs/', views.get_certs, name='get_certs'),
    path('api/announcements/', views.get_announcements, name='get_announcements'),
    path('api/banners/', views.get_banners, name='get_banners'),
    path('api/seo-config/', views.get_seo_config, name='get_seo_config'),
    path('api/site-config/', views.get_site_config, name='get_site_config'),
    path('api/faqs/', views.get_faqs, name='get_faqs'),
    path('api/orders/mine/', views.my_orders, name='my_orders'),
    path('api/orders/<int:order_id>/delete/', views.delete_order, name='delete_order'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
