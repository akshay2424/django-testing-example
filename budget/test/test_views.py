from django.http import response
from django.test import TestCase, Client
from django.urls import reverse
from django.urls.base import clear_script_prefix
from budget.models import Project, Category, Expense
import json


class TestViews(TestCase):

    def setUp(self):
        client = Client()
        self.list_url = reverse('list')
        self.detail_url = reverse('detail', args=['project1'])
        self.project1 = Project.objects.create(
            name='project1',
            budget=100000,

        )

    def test_project_list_GET(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 200)

    def test_project_detail_GET(self):
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, 200)

    def test_project_detail_POST_add_new_expense(self):
        Category.objects.create(project=self.project1, name='dev')
        response = self.client.post(self.detail_url, {
            'title': 'expense1',
            'amount': '1000',
            'category': 'dev'

        })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.project1.expenses.first().title, 'expense1')
