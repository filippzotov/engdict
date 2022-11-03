from django.shortcuts import render, redirect
from .models import Word
from .forms import WordForm
from django.http import HttpResponseRedirect

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from django.views.generic.edit import FormView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from googletrans import Translator

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("login/")
    wordform = WordForm()
    words = Word.objects.filter(user=request.user)

    context = {"wordform": wordform, "words": words}
    if request.method == "POST":
        title = request.POST.get("title")
        translator = Translator()

        if translator.detect(title).lang == "en":
            desc = translator.translate(title, dest="ru").text
        else:
            desc = request.POST.get("title")
            title = translator.translate(desc, dest="en").text
        newword = Word(title=title, description=desc, user=request.user)
        newword.save()
        return HttpResponseRedirect("/")
    return render(request, "dict/index.html", context=context)


def delete(request, pk):
    words = Word.objects.get(id=pk)
    words.delete()
    return HttpResponseRedirect("/")


class CustomLoginView(LoginView):
    template_name = "dict/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("index")


class RegisterPage(FormView):
    template_name = "dict/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        user = form.save()
        print(user)
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("index")
        return super(RegisterPage, self).get(*args, **kwargs)
