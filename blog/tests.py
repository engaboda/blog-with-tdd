from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Entry



class EntryModelTest(TestCase):

    def test_string_representation(self):
        entry = Entry(title='my entry title')
        self.assertEqual( str(entry), entry.title )

    def test_verbose_name_plural(self):
        self.assertEqual( Entry._meta.verbose_name_plural, 'entries' )

    def test_hompage(self):
        response = self.client.get('/')
        self.assertEqual( response.status_code, 200 )

class HomePageTest(TestCase):
    '''
        test our blog entry show up on the homepage
    '''
    def setUp(self):
        self.user =  get_user_model().objects.create(username='aboda')

    def test_one_entry(self):
        Entry.objects.create(title='1-title', body='1-body', author=self.user)
        response = self.client.get('/')
        self.assertContains(response, '1-title')
        self.assertContains(response, '1-body')

    def test_two_entry(self):
        Entry.objects.create(title='1-title', body='1-body', author=self.user)
        Entry.objects.create(title='2-title', body='2-body', author=self.user)

        response = self.client.get('/')
        self.assertContains(response, '1-title')
        self.assertContains(response, '1-body')
        self.assertContains(response, '2-body')
    
    def test_no_entries(self):
        response = self.client.get('/')
        self.assertContains(response, 'no blog entries')

class EntryViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='aboda')
        self.entry = Entry.objects.create(title='1-title', body='1-body', author=self.user )

    def test_base_view(self):
        response = self.client.get( self.entry.get_absolute_url() )
        self.assertContains(response, self.entry.get_absolute_url())
    
    def test_get_absolute_url(self):
        # user =  get_user_model().objects.create(username='1-aboda')
        entry = Entry.objects.create(title='1-title', body='1-body', author=self.user)
        self.assertIsNotNone(entry.get_absolute_url())
    
    def test_title_in_entry(self):
        response = self.client.get(self.entry.get_absolute_url())
        self.assertContains(response, self.entry.title)
    
    def test_body_in_entry(self):
        response = self.client.get(self.entry.get_absolute_url())
        self.assertContains(response, self.entry.body)