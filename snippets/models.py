from django.db import models

# Create your models here.

from django.conf import settings
from django.db import models


class Snippet(models.Model):
    title = models.CharField('タイトル', max_length=128)
    code = models.TextField('コード', blank=True)
    description = models.TextField('説明', blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name='投稿者',
                                   on_delete=models.CASCADE)
    # モデルのインスタンスを保存するタイミングで現在日時が自動的にセットされる
    created_at = models.DateTimeField('投稿日', auto_now_add=True)
    # モデルを更新するたびにその時点での時刻を自動で設定してくれる
    updated_at = models.DateTimeField('更新日', auto_now=True)

    class Meta:
        db_table = "snippets"

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    text = models.TextField('本文', blank=False)
    commented_to = models.ForeignKey(Snippet,
                                     verbose_name='スニペット',
                                     on_delete=models.CASCADE)
    commented_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     verbose_name='投稿者',
                                     on_delete=models.CASCADE)
    # モデルのインスタンスを保存するタイミングで現在日時が自動的にセットされる
    created_at = models.DateTimeField('投稿日', auto_now_add=True)
    # モデルを更新するたびにその時点での時刻を自動で設定してくれる
    updated_at = models.DateTimeField('更新日', auto_now=True)

    class Meta:
        db_table = "comments"

    def __str__(self) -> str:
        return f'{self.pk} {self.text}'
