# Generated by Django 3.2.4 on 2021-06-21 07:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='add_info.category')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('type', models.CharField(choices=[('R', 'Recommendation'), ('U', 'UserInfo')], max_length=1)),
                ('creaedDate', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='add_info.category')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='add_info.item')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastname', models.CharField(blank=True, max_length=50)),
                ('firstname', models.CharField(blank=True, max_length=50)),
                ('patronymic', models.CharField(blank=True, max_length=50)),
                ('group', models.CharField(blank=True, max_length=10)),
                ('role', models.ManyToManyField(blank=True, to='add_info.Role')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='images/', verbose_name='Файл для распознавания')),
                ('file_cropped', models.ImageField(blank=True, default='1', upload_to='images/', verbose_name='Файл для распознавания')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('userItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='add_info.useritem')),
            ],
            options={
                'verbose_name': 'photo',
                'verbose_name_plural': 'photos',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('userItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='add_info.useritem')),
            ],
        ),
        migrations.CreateModel(
            name='InfoSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('LT', 'Список значений'), ('UI', 'Ввод данных'), ('DC', 'Документ'), ('LK', 'Ссылка'), ('IM', 'Изображение')], max_length=2, verbose_name='Тип загружаемых данных')),
                ('itemNameKeywords', models.TextField(default='', verbose_name='Ключевые слова для поиска названия')),
                ('existOfName', models.BooleanField(verbose_name='Наличие данных о пользователе')),
                ('existOfScore', models.BooleanField(verbose_name='Наличие оценки')),
                ('scoreDescription', models.TextField(default='', verbose_name='Описание')),
                ('scoreKeywords', models.TextField(default='', verbose_name='Ключевые слова для поиска оценки')),
                ('existOfDescription', models.BooleanField(verbose_name='Наличие описания')),
                ('isRequiredDescription', models.BooleanField(verbose_name='Обязательность добавления описания')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='add_info.category', verbose_name='Категория')),
                ('createdUserRole', models.ManyToManyField(to='add_info.Role', verbose_name='Роль пользователя')),
            ],
            options={
                'verbose_name': 'Категории',
                'verbose_name_plural': 'Категория',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='files/', verbose_name='Файл для распознавания')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('startPage', models.IntegerField(blank=True)),
                ('endPage', models.IntegerField(blank=True)),
                ('userItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='add_info.useritem')),
            ],
        ),
    ]