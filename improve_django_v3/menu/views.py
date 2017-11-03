from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib import messages
from .forms import MenuForm
from .models import Menu, Item


def menu_list(request):
    all_menus = Menu.objects.filter(expiration_date__gte=timezone.now())
    return render(request, 'menu/list_all_current_menus.html',
                  {'menus': all_menus})


def menu_detail(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_menu(request):
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Record has been created!')
            return redirect(reverse('menu:menu_detail',
                            kwargs={'pk': menu.pk}))
    else:
        form = MenuForm()
    return render(request, 'menu/menu_edit.html', {'form': form})


def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    form = MenuForm(instance=menu)
    if request.method == "POST":
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.items = request.POST.getlist("items")
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Record has been updated!')
            return redirect(reverse('menu:menu_list'))

    return render(request, 'menu/change_menu.html', {
            'form': form,
            'menu': menu
        })
