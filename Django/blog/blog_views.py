from itertools import chain
import re
from django.contrib import messages
from .forms import ContactForm
from django.views.generic import View
from django.core.mail import send_mail
from django.conf.global_settings import EMAIL_HOST_USER
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    DetailView,
)
from .models import Post, PageList


def home(request):
    return render(request, 'blog/home.html')


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def news(request):
    context = {
        'posts': Post
    }

    return render(request, 'blog/news.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/news.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10


def flatpage(request):
    return render(request, 'flatpages/default.html')


class PostDetailView(DetailView):
    model = Post


# ----------------------   Site search   ---------------------------------------

class SearchResultsView(View):
    template_name = 'blog/search_results.html'

    def get(self, request):
        context = {}

        q = request.GET.get('q')
        if q:
            query_sets = []  # Общий QuerySet

            # Ищем по всем моделям
            query_sets.append(PageList.objects.search(query=q))
            query_sets.append(Post.objects.search(query=q))

            # и объединяем выдачу
            final_set = list(chain(*query_sets))

            context['last_question'] = '?q=%s' % q

            current_page = Paginator(final_set, 10)

            page = request.GET.get('page')
            try:
                context['object_list'] = current_page.page(page)
            except PageNotAnInteger:
                context['object_list'] = current_page.page(1)
            except EmptyPage:
                context['object_list'] = current_page.page(current_page.num_pages)

        return render(request=request, template_name=self.template_name, context=context)


# ---------------------------FEEDBACK FORM-------------------------------------------------
# 1. Email subject
# 2. Message (message body)
# 3. Sender
# 4. Recipient

def email(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        name = form.data['name']
        email = form.data['email']
        description = form.data['description']
        send_mail(
            'Здравствуйте ' + name,
            # render(request, 'blog/mail.html', {'mail': mail}),
            'Вы оставили сообщение на сайте трест12.рф \n' + description,
            EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        # send_mail(
        #     'Поступило сообщение с сайта!',
        #     # render(request, 'blog/mail.html', {'mail': mail}),
        #     'Вам оставили сообщение на сайте трест12.рф',
        #     'esywebmoney@yandex.ru',
        #     ['trest12_1@mail.ru'],
        #     fail_silently=False,
        # )


class SendContact(View):
    def post(self, request):
        form = ContactForm(request.POST)
        # field validation
        phone = form.data['phone']
        regex_phone = re.fullmatch(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', phone)
        name = form.data['name']
        # displaying a message about successful submission of data from the form
        if form.is_valid():
            form.save()
            email(request)
            messages.success(request, 'Спасибо за обращение!')
        # displaying messages to the user about input errors
        if name == 'scisoftdev' or name == 'Денис Косолапов' or name == 'CrazyHacker':
            messages.success(request, 'разработчики сайта SciSoftDev, Денис Косолапов и CrazyHacker')
        if regex_phone is None:
            messages.success(request, 'Введите корректный номер телефона')
        # get the address of the current page
        address = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # anchor to the form
        return redirect(address.url + '#feedback')


# ---------------------------------SHOW DEBUGGING CONTACT FORM--------------------------------------
# def snippet_detail(request):
#     if request.method == 'POST':
#         form = SnippetForm(request.POST)
#         # field validation
#         phone = form.data['phone']
#         regex_phone = re.fullmatch(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', phone)
#         # displaying a message about successful submission of data from the form
#         if form.is_valid():
#             form.save()
#             email(request)
#             messages.success(request, 'Спасибо за обращение!')
#         # displaying messages to the user about input errors
#         if regex_phone == None:
#             messages.success(request, 'Введите корректный номер телефона')
#     form = SnippetForm()
#     return render(request, 'blog/form.html', {'form': form})