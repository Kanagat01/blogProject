from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
                      .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Черновик'
        PUBLISHED = 'PB', 'Опубликован'

    title = models.CharField(verbose_name='Заголовок', max_length=250)
    slug = models.SlugField(verbose_name='Слаг', max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
			       verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField(verbose_name='Основной текст')
    publish = models.DateTimeField(verbose_name='Время публикации', default=timezone.now)
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    status = models.CharField(verbose_name='Статус', max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    tags = TaggableManager()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post,
			     verbose_name='Пост',
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(verbose_name='Имя', max_length=80)
    email = models.EmailField(verbose_name='Email')
    body = models.TextField(verbose_name='Основной текст')
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    active = models.BooleanField(verbose_name='Активен', default=True)

    class Meta:
	    verbose_name = 'Комментарий'
	    verbose_name_plural = 'Комментарии'
	    ordering = ['created']
	    indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Комментарий от {self.name} к посту {self.post}'
