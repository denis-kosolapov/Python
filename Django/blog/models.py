from django.utils import timezone
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q
from django.contrib.flatpages.models import FlatPage
from django.core.mail import send_mass_mail

class ArticleManager(models.Manager):
    use_for_related_fields = True

    def search(self, query=None):
        qs = self.get_queryset()
        if query:
            or_lookup = (Q(title__icontains=query) | Q(content__icontains=query))
            qs = qs.filter(or_lookup)

        return qs


class PageList(models.Model):
    url = models.CharField('Адрес страницы',max_length=100)
    title = models.CharField('Заголовок страницы',max_length=200)
    content = models.TextField('Текст стрницы в поиске',blank=True)
    objects = ArticleManager()

    class Meta:
        verbose_name = 'отображение странцы в поиске'
        verbose_name_plural = 'поиск по сайту'



class Post(models.Model):
    title = models.CharField('Заголовок новости', max_length=100)
    content = models.TextField('Основной текст новости')
    description = models.TextField('Краткое описание')
    image = models.ImageField('Загрузить картинку', upload_to='images/', default='images/No_image_available.svg.png')
    date_posted = models.DateTimeField('Дата/время публикации',default=timezone.now)
    objects = ArticleManager()


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'Новости'


# Migration is done first, so the form must be without RegexValidator validation

class Contacts(models.Model):
    """feedback form"""
    name = models.CharField('Имя', max_length=120)
    email = models.EmailField('Email', max_length=120)
    # phone = models.CharField('Телефон', max_length=15)
    phone = models.CharField('Телефон', max_length=15, validators=[
        RegexValidator(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')
    ])
    description = models.TextField('Тема звнока', max_length=1000, blank=True, null=True)
    date = models.DateTimeField('Дата/время получения сообщения',default=timezone.now)

    # to be displayed correctly in the admin panel
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'форма обратной связи'
        verbose_name_plural = 'формы обратной связи'


class Images(models.Model):
    name = models.CharField('Название изображения', max_length=50)
    image = models.ImageField('Выбрать изображение', upload_to='images/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Загрузить изображение'
        verbose_name_plural = 'Изображения'


class SenderEmails(models.Model):
    subject = models.CharField('Тема сообщения',max_length=150)
    message = models.TextField('Текст сообщения')
    date = models.DateTimeField('Дата отправки', default=timezone.now)
    class Meta:
        verbose_name = 'Добавить рассылку'
        verbose_name_plural = 'Создать рассылку'