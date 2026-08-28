from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .forms.create_api_form import CreateAPIForm
from .models import API

# Create your views here.


@login_required(login_url="accounts:login")
def dashboard(request):
    user_apis = API.objects.filter(owner=request.user)
    return render(request, "monitoring/dashboard.html", {"my_apis": user_apis})


@login_required(login_url="accounts:login")
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


@login_required(login_url="accounts:login")
def detail_api(request, id):
    api = get_object_or_404(API, id=id, owner=request.user)

    histories = api.histories.order_by("-date")

    paginator = Paginator(histories, 100)

    page_history = paginator.get_page(request.GET.get("page"))

    return render(
        request, "monitoring/detail_api.html", {"api": api, "histories": page_history}
    )
