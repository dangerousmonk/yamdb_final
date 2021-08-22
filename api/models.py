from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import year_validator


class Genre(models.Model):
    name = models.CharField(
        max_length=25,
        verbose_name=_('name'),
    )
    slug = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('address'),
    )

    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
        ordering = ['slug', ]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=25, verbose_name=_('category'))
    slug = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('slug'),
    )

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['slug', ]

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        db_index=True,
        max_length=100,
        unique=True,
        verbose_name=_('name'),
    )
    year = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name=_('year'),
        validators=[year_validator],
    )
    description = models.TextField(verbose_name=_('description'))
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
        verbose_name=_('genre'),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name=_('category'),
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('pub_date'),
    )

    class Meta:
        verbose_name = _('Title')
        verbose_name_plural = _('Titles')
        ordering = ['-pub_date', ]

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        blank=True,
        null=True,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name=_('title'),
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5,
        verbose_name=_('rating'),
    )
    author = models.ForeignKey(
        'users.User',
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name=_('author'),
    )
    text = models.TextField(verbose_name=_('text'))
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('pub_date'),
    )

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ['-pub_date', ]
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title', ], name='unique-author-title'
            )
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    text = models.TextField(verbose_name=_('comment text'))
    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name=_('review'),
    )
    author = models.ForeignKey(
        'users.User',
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name=_('author')
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('publication date'),
    )

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['-pub_date', ]

    def __str__(self):
        return self.text[:15]
