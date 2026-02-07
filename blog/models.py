from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_jalali.db import models as jmodels
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = 'PB', 'انتشار'
        DRAFT = 'DF', 'پیش نویس'
        REJECTED = 'RE', 'رد شده'

    title = models.CharField(max_length=250, verbose_name='عنوان')
    description = models.TextField(verbose_name='جزئیات')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='کاربر', related_name="user")
    created = jmodels.jDateTimeField(
        auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name='تاریخ آپدیت')
    publish = jmodels.jDateTimeField(
        default=timezone.now, verbose_name='تاریخ انتشار')
    slug = models.SlugField(max_length=250, verbose_name='اسلاگ')
    status = models.CharField(
        max_length=100, choices=Status, default=Status.DRAFT, verbose_name='وضعیت')
    reading_time = models.PositiveIntegerField(verbose_name='زمان مطالعه')
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])


class Ticket(models.Model):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش مشکل')
    )
    name = models.CharField(max_length=250)
    message = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    subject = models.CharField(max_length=250, choices=SUBJECT_CHOICES)

    class Meta:
        ordering = ['-name']
        indexes = [
            models.Index(fields=['-name']),
        ]
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments', verbose_name='پست')
    name = models.CharField(max_length=250, verbose_name='نام شما')
    message = models.TextField(verbose_name='متن کامنت')
    created = jmodels.jDateTimeField(
        auto_now_add=True, verbose_name='تاریخ ایجاد')
    active = models.BooleanField(default=False, verbose_name='وضعیت کامنت')

    class Meta:
        ordering = ('-name', )
        indexes = [
            models.Index(fields=['-name']),
        ]
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

    def __str__(self):
        return self.name


class Image(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='image', verbose_name='پست')
    title = models.CharField(
        max_length=300, verbose_name='عنوان تصویر', null=True, blank=True)
    description = models.TextField(
        verbose_name='جزئیات تصویر', null=True, blank=True)
    image = models.ImageField(verbose_name="تصویر", upload_to='post_image')

    class Meta:
        ordering = ('-title', )
        indexes = [
            models.Index(fields=['-title'])
        ]
        verbose_name = "تصویر"
        verbose_name_plural = "تصاویر"
        