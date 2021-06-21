from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Role(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lastname = models.CharField(max_length=50, blank=True)
    firstname = models.CharField(max_length=50, blank=True)
    patronymic = models.CharField(max_length=50, blank=True)
    group = models.CharField(max_length=10, blank=True)
    role = models.ManyToManyField(Role, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return "User - %s, фамилия - %s, имя - %s , отчетство - %s, группа - %s, роль - %s" \
               % (self.user, self.lastname, self.firstname, self.patronymic, self.group, self.role)

TYPE_OF_INPUT_INFO = (
    ('LT', 'Список значений'),
    ('UI', 'Ввод данных'),
    ('DC', 'Документ'),
    ('LK', 'Ссылка'),
    ('IM', 'Изображение'),
)

class InfoSource(models.Model):
    type = models.CharField(max_length=2, choices=TYPE_OF_INPUT_INFO, verbose_name='Тип загружаемых данных')
    createdUserRole = models.ManyToManyField(Role, verbose_name='Роль пользователя')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    itemNameKeywords = models.TextField(default='', verbose_name='Ключевые слова для поиска названия')
    existOfName = models.BooleanField(verbose_name='Наличие данных о пользователе')
    existOfScore = models.BooleanField(verbose_name='Наличие оценки')
    scoreDescription = models.TextField(default='', verbose_name='Описание')
    scoreKeywords = models.TextField(default='', verbose_name='Ключевые слова для поиска оценки')
    existOfDescription = models.BooleanField(verbose_name='Наличие описания')
    isRequiredDescription = models.BooleanField(verbose_name='Обязательность добавления описания')

    class Meta:
        verbose_name = "Категории"
        verbose_name_plural = 'Категория'

STATUS_OF_USER_ITEMS = (
    ('R', 'Recommendation'),
    ('U', 'UserInfo')
)

class UserItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    type = models.CharField(max_length=1, choices=STATUS_OF_USER_ITEMS)
    creaedDate = models.DateTimeField(auto_now=True)

class Photo(models.Model):
    file = models.ImageField(upload_to='images/', verbose_name='Файл для распознавания')
    file_cropped = models.ImageField(upload_to='images/', verbose_name='Файл для распознавания', blank=True, default='1')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    userItem = models.ForeignKey(UserItem, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'

class File(models.Model):
    file = models.FileField(upload_to='files/', verbose_name='Файл для распознавания')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    userItem = models.ForeignKey(UserItem, on_delete=models.CASCADE)
    startPage = models.IntegerField(blank=True)
    endPage = models.IntegerField(blank=True)

class Link(models.Model):
    name = models.TextField()
    userItem = models.ForeignKey(UserItem, on_delete=models.CASCADE)