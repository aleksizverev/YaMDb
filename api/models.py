from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year


class Role(models.TextChoices):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'


class User(AbstractUser):
    role = models.CharField(choices=Role.choices, default=Role.USER,
                            max_length=500)
    bio = models.TextField(max_length=500, blank=True)
    confirmation_code = models.CharField(max_length=32, blank=True)

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == Role.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR


class Genre(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название жанра')
    slug = models.SlugField(unique=True, blank=True,
                            null=True, verbose_name='Слаг жанра')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(unique=True, blank=True,
                            null=True, verbose_name='Слаг категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True, related_name='category_titles',
                                 verbose_name='Категория')
    genre = models.ManyToManyField(Genre, blank=True,
                                   null=True, related_name='genre_titles',
                                   verbose_name='Жанр')
    name = models.CharField(max_length=255, verbose_name='Название')
    year = models.PositiveSmallIntegerField(validators=[validate_year])
    description = models.TextField(
        max_length=500, blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name="review")
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="author")

    score = models.IntegerField(validators=(MaxValueValidator(10),
                                            MinValueValidator(0)))
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True,
                                    db_index=True)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="comments")
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE,
                                  related_name="comments")
    text = models.TextField()
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True,
                                    db_index=True)
