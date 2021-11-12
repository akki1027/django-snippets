# Create your views here.

from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_safe
from django.contrib.auth.decorators import login_required
from snippets.models import Snippet
from snippets.forms import SnippetForm


@require_safe
def top(request):
    snippets = Snippet.objects.all()
    context = {'title': 'Djangoスニペット', 'snippets': snippets}
    return render(request, 'snippets/top.html', context)


@login_required
def snippet_new(request):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.created_by = request.user
            snippet.save()
            return redirect(snippet_detail, snippet_id=snippet.pk)
    else:
        form = SnippetForm()
        context = {'title': 'スニペットの登録', 'form': form}
    return render(request, 'snippets/snippet_new.html', context)


@login_required
def snippet_edit(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    if snippet.created_by_id != request.user.id:
        return HttpResponseForbidden('このスニペットの編集は許可されていません。')

    if request.method == 'POST':
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid:
            form.save()
            return redirect(snippet_detail, snippet_id=snippet_id)
    else:
        form = SnippetForm(instance=snippet)
        context = {'title': '%sの編集' % snippet.title, 'form': form}
    return render(request, 'snippets/snippet_edit.html', context)


@require_safe
def snippet_detail(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    context = {'title': snippet.title, 'snippet': snippet}
    return render(request, 'snippets/snippet_detail.html', context)
