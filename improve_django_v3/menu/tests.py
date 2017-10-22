from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from .forms import MenuForm
from .models import Menu,Item,Ingredient

class MenuItemIngredientModelTest(TestCase):

    def setUp(self):
        #creating a user
        user = User.objects.create_user(
            'foo',
            'myemail@test.com',
            'pass'
        )
        #creating a new ingredient
        ingredient = Ingredient.objects.create(name='milk')
        ingredient.save()
        # creating a new item
        item = Item.objects.create(
            name='chocolate',
            description='chocolate brownies',
            chef = user,
            standard = True
        )
        item.save()
        item.ingredients.add(ingredient)
        #creating a new menu
        menu = Menu(
            season='my season',
            expiration_date = '2017-10-15 19:00:00'

        )
        menu.save()
        menu.items.add(item)


    def test_menu_created(self):
        menu = Menu.objects.get(season='my season')
        self.assertEqual(menu.season,"my season")


class MenuViewTests(TestCase):

    def setUp(self):
        #creating a user
        user = User.objects.create_user(
            'andy',
            'andy@test.com',
            'pass'
        )
        #creating a new ingredient
        ingredient = Ingredient.objects.create(name='milk')
        ingredient.save()
        # creating a new item
        item = Item.objects.create(
            name='chocolate',
            description='chocolate milk',
            chef = user,
            standard = True
        )
        item.save()
        item.ingredients.add(ingredient)
        #creating a new menu
        self.menu = Menu(
            season='my season',
            expiration_date = '2017-10-02 19:00:00'

        )
        self.menu.save()
        self.menu.items.add(item)
        self.menu.save()


    def test_menu_list(self):
        """test that no menus are returned when the menu has expired,
        it has expired when the datetime is before the present datetime"""

        response = self.client.get(reverse('menu:menu_list'))
        self.assertEqual(response.status_code,200)
        #check that the menu is not in context as expiration date is old
        self.assertNotContains(response,'my season')
        self.assertTemplateUsed(response,'menu/list_all_current_menus.html')


    def test_menu_detail(self):
        response = self.client.get(reverse('menu:menu_detail',
                                            kwargs={'pk':self.menu.pk}))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'my season')
        self.assertTemplateUsed(response,'menu/menu_detail.html')


    def test_create_new_menu(self):
        form = MenuForm()
        response = self.client.get(reverse('menu:menu_new'))
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(form,type(response.context['form']))
        self.assertTemplateUsed(response,'menu/menu_edit.html')


    def test_create_new_menu_redirection(self):
        """test that the view redirects correctly in a post request"""

        response = self.client.post(reverse('menu:menu_new'),{
            'season':self.menu.season,
            'items':self.menu.items,
            'expiration_date':self.menu.expiration_date
        })
        self.assertEqual(response.status_code,200)
        self.assertRedirects(response,reverse('menu:menu_detail',
                                                kwargs={'pk':self.menu.pk}))

    def test_edit_menu(self):
        form = MenuForm()
        response = self.client.get(reverse('menu:menu_edit',
                                            kwargs={'pk':self.menu.pk}))
        self.assertEqual(response.status_code,200)
        self.assertIsInstance(form,type(response.context['form']))
        self.assertIsInstance(self.menu,type(response.context['menu']))
        self.assertTemplateUsed(response,'menu/change_menu.html')


class ItemViewTests(TestCase):

    def setUp(self):
        #creating a user
        user = User.objects.create_user(
            'andy',
            'andy@test.com',
            'pass'
        )
        #creating a new ingredient
        ingredient = Ingredient.objects.create(name='milk')
        ingredient.save()
        # creating a new item
        self.item = Item.objects.create(
            name='chocolate',
            description='chocolate milk',
            chef = user,
            standard = True
        )
        self.item.save()
        self.item.ingredients.add(ingredient)


    def test_item_detail(self):
        response = self.client.get(reverse('menu:item_detail',
                                            kwargs={'pk':self.item.pk}))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'chocolate')
        self.assertTemplateUsed(response,'menu/detail_item.html')
