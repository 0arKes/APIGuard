from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms.api_form import APIForm
from .models import API

# Create your views here.


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        user_apis = API.objects.filter(owner=request.user)
        return render(request, "monitoring/dashboard.html", {"my_apis": user_apis})


class CreateAPI(LoginRequiredMixin, View):
    def get(self, request):
        api_form = APIForm()
        return render(request, "monitoring/create_api.html", {"api_form": api_form})

    def post(self, request):
        api_form = APIForm(request.POST)

        if api_form.is_valid():
            api = api_form.save(commit=False)
            api.owner = request.user

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


class EditAPI(LoginRequiredMixin, View):
    def get(self, request, id):
        api = get_object_or_404(API, id=id, owner=request.user)
        edit_form = APIForm(instance=api)

        return render(
            request, "monitoring/edit_api.html", {"edit_form": edit_form, "api": api}
        )

    def post(self, request, id):
        api = get_object_or_404(API, id=id, owner=request.user)
        edit_form = APIForm(request.POST, instance=api)

        if edit_form.is_valid():
            api = edit_form.save(commit=False)
            api.save()

            return redirect("monitoring:detail_api", id=api.id)

        return render(
            request, "monitoring/edit_api.html", {"edit_form": edit_form, "api": api}
        )


class DeleteAPI(LoginRequiredMixin, View):
    def get(self, request, id):
        api = get_object_or_404(API, id=id, owner=request.user)
        api.delete()

        return redirect("monitoring:dashboard")
