from django.test import TestCase, Client
from django.contrib.auth.models import User
from Tasks.models import Task, Note
from django.utils import timezone

class TestMainNavigation(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        Task.objects.create(title="Test", description="tasks", start_date=timezone.now(),)
        Note.objects.create(title="Test", description="notes", created_date=timezone.now(),)

    def test_home(self):
        page = self.client.get('/')
        self.assertEqual(page.status_code, 200)

    def test_tasks(self):        
        tasks = self.client.get('/tasks/')        
        self.assertEqual(tasks.status_code, 200)
        self.assertTemplateUsed(tasks, 'Tasks/tasks.html')

    def test_task(self):
        t = Task.objects.all()[0]
        page = self.client.get('/task/%s' % t.pk)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'Tasks/task-detail.html')
    
    def test_task_delete(self):
        t = Task.objects.all()[0]
        page = self.client.get('/task/delete/%s' % t.pk)
        self.assertEqual(page.status_code, 302) # test for redirect
    
    def test_new_task(self):
        page = self.client.get('/new-task/')
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'Tasks/newtask.html')

    def test_task_management(self):
        page = self.client.get('/manage/')
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'Tasks/manage.html')
    
    def test_temp(self):
        page = self.client.get('/temp/')
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'Tasks/temp.html')
    
    def test_temp_data(self):        
        page = self.client.get('/temp_data/')
        self.assertEqual(page.status_code, 200)
        
    def test_notes(self):
        page = self.client.get('/notes/')
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'Notes/notes.html')

    def test_note(self):
        n = Note.objects.all()[0]
        page = self.client.get('/notes/%s' % n.pk)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'Notes/note-detail.html')

    def test_new_note(self):
        page = self.client.get('/notes/new')
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'Notes/newnote.html')        

