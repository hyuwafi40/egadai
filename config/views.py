from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views import View


class IndexViews(View):
    template_name = "index.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("core:index")
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(
                    request,
                    f"Selamat datang, {user.get_full_name() or user.username}!",
                )
                return redirect("core:index")
            messages.error(request, "Akun Anda telah dinonaktifkan.")
            return render(request, self.template_name)
        messages.error(request, "Username atau Password salah!")
        return render(request, self.template_name)


def logout_view(request):
    logout(request)
    messages.info(request, "Anda telah keluar.")
    return redirect("login")
