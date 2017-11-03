from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .forms import MenuForm
from .models import Menu, Item, Ingredient


class MenuModelTest(TestCase):

    def setUp(self):
        # creating a user
        user = User.objects.create_user(
            'foo',
            'myemail@test.com',
            'pass'
        )
        # creating a new ingredient
        ingredient = Ingredient.objects.create(name='milk')
        ingredient.save()
        # creating a new item
        item = Item.objects.create(
            name='chocolate',
            description='chocolate brownies',
            chef=user,
            standard=True
        )
        item.save()
        item.ingredients.add(ingredient)
        # creating a new menu
        self.menu = Menu(
            season='my season',
            expiration_date='2017-10-15 19:00:00'

        )
        self.menu.save()
        self.menu.items.add(item)

    def test_menu_created(self):
        menu = Menu.objects.get(season='my season')
        self.assertEqual(menu.season, "my season")

    def test_menu_str_method(self):
        self.assertEqual(str(self.menu), self.menu.season)


class MenuViewTests(TestCase):

    def setUp(self):
        # creating a user
        user = User.objects.create_user(
            'andy',
            'andy@test.com',
            'pass'
        )
        # creating a new ingredient
        ingredient = Ingredient.objects.create(name='milk')
        ingredient.save()
        # creating a new item
        self.item = Item.objects.create(
            name='chocolate',
            description='chocolate milk',
            chef=user,
            standard=True
        )
        self.item.save()
        self.item.ingredients.add(ingredient)
        # creating a new menu
        self.menu = Menu(
            season='my season',
            expiration_date='2017-10-02 19:00:00'

        )
        self.menu.save()
        self.menu.items.add(self.item)
        self.menu.save()

    def get_items(self):
        items = []
        for item in self.menu.items.all():
            items.append(item.pk)
        return items

    def test_menu_list(self):
        """test that no menus are returned when the menu has expired,
        it has expired when the datetime is before the present datetime"""

        response = self.client.get(reverse('menu:menu_list'))
        self.assertEqual(response.status_code, 200)
        # check that the menu is not in context as expiration date is old
        self.assertNotContains(response, 'my season')
        self.assertTemplateUsed(response, 'menu/list_all_current_menus.html')

    def test_menu_detail(self):
        response = self.client.get(reverse('menu:menu_detail',
                                   kwargs={'pk': self.menu.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'my season')
        self.assertTemplateUsed(response, 'menu/menu_detail.html')

    def test_create_new_menu(self):
        form = MenuForm()
        response = self.client.get(reverse('menu:menu_new'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(form, type(response.context['form']))
        self.assertTemplateUsed(response, 'menu/menu_edit.html')

    def test_create_new_menu_redirection(self):
        """test that the view redirects correctly in a post request"""
        items = self.get_items()

        form_data = {
            'season': self.menu.season,
            'items': items,
            'expiration_date': self.menu.expiration_date,
        }
        form = MenuForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('menu:menu_new'), form_data)
        # get the lastest menu saved
        menu = Menu.objects.latest('id')
        self.assertRedirects(response, reverse('menu:menu_detail',
                             kwargs={'pk': menu.pk}))

    def test_edit_menu_get(self):
        # test the view in a get request
        form = MenuForm()
        response = self.client.get(reverse('menu:menu_edit',
                                   kwargs={'pk': self.menu.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(form, type(response.context['form']))
        self.assertIsInstance(self.menu, type(response.context['menu']))
        self.assertTemplateUsed(response, 'menu/change_menu.html')

    def test_edit_menu_post(self):
        # test the view in a post request
        response = self.client.post(reverse('menu:menu_edit',
                                    kwargs={'pk': self.menu.pk}))
        menu = Menu.objects.filter(season='my season')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            menu.exists()
        )


class MenuFormTest(TestCase):

    def setUp(self):
        # creating a user
        user = User.objects.create_user(
            'andy',
            'andy@test.com',
            'pass'
        )
        # creating a new ingredient
        ingredient = Ingredient.objects.create(name='milk')
        ingredient.save()
        # creating a new item
        self.item = Item.objects.create(
            name='chocolate',
            description='chocolate milk',
            chef=user,
            standard=True
        )
        self.item.save()
        self.item.ingredients.add(ingredient)
        # creating a new menu
        self.menu = Menu(
            season='my season',
            expiration_date='2017-10-28 20:00:00'

        )
        self.menu.save()
        self.menu.items.add(self.item)
        self.menu.save()

    def get_items(self):
        items = []
        for item in self.menu.items.all():
            items.append(item.pk)
        return items

    def test_menu_form(self):
        """test that the form is invalid
        when the expiration date is blank"""

        items = self.get_items()

        form_data = {
            'season': self.menu.season,
            'items': items,
            'expiration_date': '',
        }
        form = MenuForm(data=form_data)
        self.assertFalse(form.is_valid())


class ItemViewTests(TestCase):

    def setUp(self):
        # creating a user
        user = User.objects.create_user(
            'andy',
            'andy@test.com',
            'pass'
        )
        # creating a new ingredient
        ingredient = Ingredient.objects.create(name='milk')
        ingredient.save()
        # creating a new item
        self.item = Item.objects.create(
            name='chocolate',
            description='chocolate milk',
            chef=user,
            standard=True
        )
        self.item.save()
        self.item.ingredients.add(ingredient)

    def test_item_detail(self):
        response = self.client.get(reverse('menu:item_detail',
                                   kwargs={'pk': self.item.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'chocolate')
        self.assertTemplateUsed(response, 'menu/detail_item.html')
