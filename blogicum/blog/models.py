from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class AddPublishedCreatedFieldModel(models.Model):
    is_published = models.BooleanField('Опубликовано',
                                       default=True,
                                       help_text=('Снимите галочку, чтобы'
                                                  ' скрыть публикацию.'))
    created_at = models.DateTimeField('Добавлено',
                                      auto_now_add=True)

    class Meta:
        abstract = True


class Post(AddPublishedCreatedFieldModel):
    title = models.CharField('Заголовок',
                             max_length=256,)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField('Дата и время публикации',
                                    help_text=('Если установить дату и время '
                                               'в будущем — можно делать'
                                               ' отложенные публикации.')
                                    )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор публикации')
    location = models.ForeignKey('Location',
                                 on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True,
                                 verbose_name='Местоположение')
    category = models.ForeignKey('Category',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name='Категория')
    image = models.ImageField('Картина поста',
                              upload_to='posts_images',
                              blank=True)

    class Meta:
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = '-pub_date',

    def __str__(self):
        return self.title


class Category(AddPublishedCreatedFieldModel):
    title = models.CharField('Заголовок',
                             max_length=256)
    description = models.TextField('Описание')
    slug = models.SlugField('Идентификатор',
                            unique=True,
                            help_text=('Идентификатор страницы для URL;'
                                       ' разрешены символы латиницы, цифры,'
                                       ' дефис и подчёркивание.'))

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(AddPublishedCreatedFieldModel):
    name = models.CharField('Название места',
                            max_length=256)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Comments(models.Model):
    created_at = models.DateTimeField('Добавлено',
                                      auto_now_add=True)
    text = models.TextField('Текст коментария')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор коментария',)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             verbose_name='Пост')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = 'created_at',

    def __str__(self):
        return self.text
