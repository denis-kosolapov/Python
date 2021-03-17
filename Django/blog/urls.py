from django.contrib.flatpages import views
from django.urls import include, path, re_path
from .blog_views import (
    PostListView,
    PostDetailView,
    SendContact,
    SearchResultsView,
)
from . import blog_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', blog_views.home, name='blog-home'),
    path('about/', blog_views.about, name='blog-about'),
    path('новости/', PostListView.as_view(), name='новости'),
    path('новости/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('pages/', include('django.contrib.flatpages.urls')),
    # path('form/', blog_views.snippet_detail),
    path('contact-form/', SendContact.as_view(), name="contact-form"),
    path('search_results/', SearchResultsView.as_view(), name='search_results'),
]


# Your other patterns here
urlpatterns += [
    re_path(r'^(?P<url>.*/)$', views.flatpage),
    path('контакты/', views.flatpage, {'url': '/контакты/'}, name='контакты'),
    path('о-компании/', views.flatpage, {'url': '/о-компании/'}, name='о-компании'),
    path('цены/', views.flatpage, {'url': '/цены/'}, name='цены'),
    path('услуги/', views.flatpage, {'url': '/услуги/'}, name='услуги'),
    path('отзывы/', views.flatpage, {'url': '/отзывы/'}, name='отзывы'),
    # backblock services
    path('технический-надзор/', views.flatpage, {'url': '/технический-надзор/'}, name='технический-надзор'),
    path('инженерные-изыскания/', views.flatpage, {'url': '/инженерные-изыскания/'}, name='инженерные-изыскания'),
    path('обследование-зданий-и-сооружений/', views.flatpage, {'url': '/обследование-зданий-и-сооружений/'}, name='обследование-зданий-и-сооружений'),
    path('проектирование/', views.flatpage, {'url': '/проектирование/'}, name='проектирование'),
    path('строительно-техническая-экспертиза/', views.flatpage, {'url': '/строительно-техническая-экспертиза/'}, name='строительно-техническая-экспертиза'),
    path('аутсорсинг-пто/', views.flatpage, {'url': '/аутсорсинг-пто/'}, name='аутсорсинг-пто'),
    path('строительный-аудит/', views.flatpage, {'url': '/строительный-аудит/'}, name='строительный-аудит'),
    path('составление-и-проверка-смет/', views.flatpage, {'url': '/составление-и-проверка-смет/'}, name='составление-и-проверка-смет'),
    path('пре-девелопмент-объектов-недвижимости/', views.flatpage, {'url': '/пре-девелопмент-объектов-недвижимости/'}, name='пре-девелопмент-объектов-недвижимости'),
    path('геодезическое-сопровождение/', views.flatpage, {'url': '/геодезическое-сопровождение/'}, name='геодезическое-сопровождение'),
]

# function displays downloaded pictures
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)