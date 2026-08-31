from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms.create_api_form import CreateAPIForm
from .models import API

# Create your views here.


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        user_apis = API.objects.filter(owner=request.user)
        return render(request, "monitoring/dashboard.html", {"my_apis": user_apis})


class CreateAPI(LoginRequiredMixin, View):
    def get(self, request):
        api_form = CreateAPIForm()
        return render(request, "monitoring/create_api.html", {"api_form": api_form})

    def post(self, request):
        api_form = CreateAPIForm(request.POST)

        if api_form.is_valid():
            api = api_form.save(commit=False)
            api.owner = request.user
            api.check_interval *= 60

            api.save()

            return redirect("monitoring:detail_api", id=api.id)

        return render(request, "monitoring/create_api.html", {"api_form": api_form})


class DetailAPI(LoginRequiredMixin, View):
    def get(self, request, id):
        api = get_object_or_404(API, id=id, owner=request.user)

        histories = api.histories.order_by("-date")

        paginator = Paginator(histories, 100)

        page_history = paginator.get_page(request.GET.get("page"))

        return render(
            request,
            "monitoring/detail_api.html",
            {"api": api, "histories": page_history},
        )
