# Create your tests here.

from django.test import TestCase, RequestFactory
from snippets.views import top
from snippets.models import Snippet
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class TopPageTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test_user",
            email="test@example.com",
            password="top_secret_pass0001",
        )
        self.snippet = Snippet.objects.create(
            title="title1",
            code="print('hello')",
            description="description1",
            created_by=self.user,
        )

    def test_top_returns_200_and_expected_title(self):
        response = self.client.get('/')
        self.assertContains(response, "Djangoスニペット", status_code=200)

    def test_top_page_uses_expected_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, "snippets/top.html")

    def test_should_return_snippet_title(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.snippet.title)

    def test_should_return_username(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.user.username)


class SnippetDetailTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test_user2",
            email="test2@example.com",
            password="top_secret_pass0002",
        )
        self.snippet = Snippet.objects.create(
            title="タイトル",
            code="コード",
            description="開設",
            created_by=self.user,
        )

    def test_should_use_expected_template(self):
        response = self.client.get("/snippets/%s/" % self.snippet.id)
        self.assertTemplateUsed(response, "snippets/snippet_detail.html")

    def test_top_page_returns_200_and_expected_heading(self):
        response = self.client.get("/snippets/%s/" % self.snippet.id)
        self.assertContains(response, self.snippet.title, status_code=200)


class CreateSnippetTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test_user3",
            email="test3@example.com",
            password="top_secret_pass0003",
        )
        self.client.force_login(self.user)

    def test_render_creation_form(self):
        response = self.client.get("/snippets/new")
        self.assertContains(response, "スニペットの登録", status_code=200)

    def test_create_snippet(self):
        data = {'title': 'テストタイトル', 'code': 'コード', 'description': '説明'}
        self.client.post("/snippets/new", data)
        snippet = Snippet.objects.get(title='テストタイトル')
        self.assertEqual('コード', snippet.code)
        self.assertEqual('説明', snippet.description)
