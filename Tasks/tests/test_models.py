from django.test import TestCase
from Tasks.models import Task, Note
from django.utils import timezone
from Tasks.forms import NewTaskForm

# models test
class TaskTest(TestCase):

    def create_task(self, title="Test", description="This is test"):
        return Task.objects.create(title=title, description=description, start_date=timezone.now(), finish_date=timezone.now())

    def test_task_creation(self):
        t = self.create_task()
        self.assertTrue(isinstance(t, Task))
        
