from django.test import TestCase
from django.contrib.auth import get_user_model
# from djago.utils import datetime

from .models import Entry
from .models import Comment

from .forms import CommentForm

from django_webtest import WebTest

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

class EntryViewTest(WebTest):
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

    def test_view_page(self):
        page = self.app.get(self.entry.get_absolute_url())
        self.assertEqual(len(page.forms),1)


    def test_form_error(self):
        page = self.app.get(self.entry.get_absolute_url())
        page = page.form.submit()
        self.assertContains( page, 'This field is required.')

    def test_from_success(self):
        page = self.app.get( self.entry.get_absolute_url() )
        page.form['name'] ='aboda'
        page.form['email'] ='abodaelkaass@yahoo.com'
        page.form['body'] ='i love test'
        page = page.form.submit()
        self.assertRedirects( page, self.entry.get_absolute_url())

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='aboda')
        self.entry = Entry.objects.create(title='1-title', body='1-body', author=self.user)
        self.comment = Comment.objects.create(
            entry=self.entry,
            name='aboda',
            email='aboda@yahoo.com',
            body='i love coding',
            )
    
    def test_string_representation(self):
        self.assertEqual(str(self.comment), 'i love coding' )
    
    def test_comment_in_entry_detail(self):
        comment = Comment.objects.create(
            entry=self.entry,
            name='aboda',
            email='aboda@yahoo.com',
            body='i love coding',
        )
        response = self.client.get(self.entry.get_absolute_url())
        self.assertContains( response, 'i love coding' )
    
    def test_empty_comment(self):
        self.entry = Entry.objects.create(title='1-title', body='1-body', author=self.user)
        response = self.client.get( self.entry.get_absolute_url() )
        self.assertContains( response, 'No comments yet.' )


class CommentFormTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create(username='ahmed')
        self.entry = Entry.objects.create(author=user, title='1-title')

    def test_init(self):
        CommentForm(entry=self.entry)

    def test_form_without_entry(self):
        with self.assertRaises(KeyError):
            CommentForm()

    def test_valid_data(self):
        form = CommentForm({
            'name':'aboda elkasass',
            'email':'abodaelkaass@yahoo.com',
            'body':'i love coding',
        }, entry=self.entry) 

        self.assertTrue(form.is_valid())
        comment = form.save()
        self.assertEqual( comment.name,'aboda elkasass' )
        self.assertEqual( comment.email,'abodaelkaass@yahoo.com' )
        self.assertEqual( comment.body,'i love coding' )
    
    def test_blank_data(self):
        form = CommentForm( {}, entry=self.entry )
        self.assertFalse( form.is_valid() )
        self.assertEqual( form.errors, {
            'name':['This field is required.'],
            'email':['This field is required.'],
            'body':['This field is required.'],
        } )




