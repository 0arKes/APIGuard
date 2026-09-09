from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from monitoring.services.api_cache_services import get_user_apis, invalidate_user_apis

from .forms.api_form import APIForm
from .models import API

# Create your views here.


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        user_apis = get_user_apis(user_id=request.user.id)
        return render(request, "monitoring/dashboard.html", {"my_apis": user_apis})


class CreateAPI(LoginRequiredMixin, View):
    def get(self, request):
        api_form = APIForm()
        return render(request, "monitoring/create_api.html", {"api_form": api_form})

    def post(self, request):
        api_form = APIForm(request.POST)

        if API.objects.filter(owner=request.user).count() >= 4:
            api_form.add_error(None, "Você atingiu o limite máximo de 5 APIs.")

        if api_form.is_valid():
            api = api_form.save(commit=False)
            api.owner = request.user

            api.save()
            invalidate_user_apis(user_id=request.user.id)

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
            invalidate_user_apis(user_id=request.user.id)

            return redirect("monitoring:detail_api", id=api.id)

        return render(
            request, "monitoring/edit_api.html", {"edit_form": edit_form, "api": api}
        )


class DeleteAPI(LoginRequiredMixin, View):
    def get(self, request, id):
        api = get_object_or_404(API, id=id, owner=request.user)

        api.delete()
        invalidate_user_apis(user_id=request.user.id)

        return redirect("monitoring:dashboard")
