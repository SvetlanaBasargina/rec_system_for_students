from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .get_text.get_text_from_img import get_test_from_img as get_text
from .models import Photo
from .forms import PhotoForm

# Create your views here.
from django.urls import reverse
from nltk.inference.tableau import Categories

import add_info.models as m


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def add_info(request):
    if request.method == 'POST':
        selectedCategory = m.Category.objects.get(name='Конкурсы').id
        selectedType = 'IM'
        return redirect(reverse('add_data', kwargs={'category_id': selectedCategory, 'type': selectedType}))
    else:
        categories = m.Category.objects.all()
        info_source_types = {}
        for elem in categories:
            types = m.InfoSource.objects.filter(category=elem).values_list("type", flat=True)
            info_source_types[elem] = types
        name_types = {}
        for elem in m.TYPE_OF_INPUT_INFO:
            name_types[elem[0]] = elem[1]
        return render(request, "add_info/add_new_info.html",
                      {'categories': categories, 'source_types': info_source_types, 'source_text': name_types})


def add_data(request, category_id, type):
    category = m.Category.objects.get(id=category_id)
    if type == 'IM':
        if request.method == 'POST':
            form = PhotoForm(request.POST, request.FILES)
            if form.is_valid():
                id = form.save()
                return redirect(reverse('check_data'))
        else:
            form = PhotoForm()
        return render(request, 'add_info/photo_list.html', {'form': form, 'category': category})


def check_data(request):
    if request.method == 'POST':
        return redirect(reverse('added_succesfully'))
    else:
        category = m.Category.objects.get(name='Олимпиады')
        print(category)
        # file = m.Photo.objects.get(id=file_id).file.url
        text = get_text('./media/images/83714980_68_page-0001.jpg')
        return render(request, 'add_info/check_data.html',
                      {'category': category, 'file': './media/images/83714980_68_page-0001.jpg', 'text': text})


def added_succesfully(request):
    return render(request, 'add_info/added_succesfully.html', {})


def profile(request):
    user = m.Profile.objects.get(id=1)
    return render(request, 'add_info/profile.html', {'user': user})


def user_info(request):
    list_of_items = m.UserItem.objects.filter(Q(author_id=1) | Q(type='U')).order_by('-creaedDate')[5:]
    return render(request, 'add_info/user_info.html', {'items': list_of_items})


def select_recommend(request):
    if request.method == "POST":
        return redirect(reverse('list_of_rec'))
    else:
        categories = m.Category.objects.all()
        items = m.Item.objects.filter(category__name='Курсы')
        return render(request, 'add_info/select_recommend.html', {'categories': categories, 'items': items})


def list_of_rec(request):
    category = m.Category.objects.get(name='Онлайн-курсы')
    method = "Рекомендации похожих элементов"
    list_rec = m.UserItem.objects.filter(Q(author_id=1) | Q(type='R') | Q(category=category)).order_by('-creaedDate')[:4]
    list_rec = reversed(list(list_rec))
    return render(request, 'add_info/list_of_rec.html', {'category': category, 'method': method, 'list_rec': list_rec})
