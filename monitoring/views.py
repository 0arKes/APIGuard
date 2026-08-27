from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms.create_api_form import CreateAPIForm
from .forms.login_form import CreateUserForm, LoginUserForm
from .models import API


# Create your views here.
def register_user(request):

    form_user = CreateUserForm()

    if request.method == "POST":
        form_user = CreateUserForm(request.POST)
        if form_user.is_valid():
            form = form_user.cleaned_data
            User.objects.create_user(
                username=form["username"],
                email=form["email"],
                password=form["password"],
            )
            return redirect("login")

        return render(request, "monitoring/register.html", {"form": form_user})

    return render(request, "monitoring/register.html", {"form": form_user})


def login_user(request):
    login_form = LoginUserForm()

    if request.method == "POST":
        login_form = LoginUserForm(request.POST)

        if login_form.is_valid():
            user = authenticate(
                username=login_form.cleaned_data["username"],
                password=login_form.cleaned_data["password"],
            )

            if user is None:
                login_form.add_error(None, "Credenciais Invalidas")

            else:
                login(request, user)

    return render(request, "monitoring/login.html", {"form": login_form})


@login_required(login_url="login")
def dashboard(request):
    user_apis = API.objects.filter(owner=request.user)
    return render(request, "monitoring/dashboard.html", {"my_apis": user_apis})


@login_required(login_url="login")
def create_api(request):
    api_form = CreateAPIForm()

    if request.method == "POST":
        api_form = CreateAPIForm(request.POST)

        if api_form.is_valid():
            api = api_form.save(commit=False)
            api.owner = request.user
            api.check_interval *= 60

            api.save()

    return render(request, "monitoring/create_api.html", {"api_form": api_form})


@login_required(login_url="login")
def detail_api(request, id):
    api = get_object_or_404(API, id=id, owner=request.user)

    histories = api.histories.order_by("-date")

    paginator = Paginator(histories, 100)

    page_history = paginator.get_page(request.GET.get("page"))

    return render(
        request, "monitoring/detail_api.html", {"api": api, "histories": page_history}
    )
