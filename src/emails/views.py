from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import services
from django.contrib import messages
from django.conf import settings
from .forms import EmailForm
from django_htmx.http import HttpResponseClientRedirect
# Create your views here.

EMAIL_ADDRESS = settings.EMAIL_ADDRESS

def logout_btn_hx_view(request):
    if not request.htmx:
        return redirect("/")
    if request.method == "POST":
        try:
            del request.session['email_id']
        except:
            pass
        email_id_in_session = request.session.get('email_id')
        if not email_id_in_session:
            return HttpResponseClientRedirect("/")
    return render(request, "emails/hx/logout-btn.html", {})

def email_token_login_view(request):
    if not request.htmx:
        return redirect("/")
    email_id_in_session = request.session.get('email_id')

    template_name = "emails/hx/form.html"
    form = EmailForm(request.POST or None)
    context = {
        "form": form,
        "message": "",
        "show_form" : not email_id_in_session,
    }
    if form.is_valid():
        email_val = form.cleaned_data.get('email')
        obj = services.start_verification_event(email_val)
        context['form'] = EmailForm()
        context['message'] = f"Success! Check your Email for verification from {EMAIL_ADDRESS}"
        # return HttpResponseClientRedirect('/check-your-email')
        return render(request, template_name, context)
    else:
        print(form.errors)
    # print('email_id',request.session.get('email_id'))
    return render(request, template_name, context)

def verify_email_token_view(request, token , *args, **kwargs):
    did_verify, msg, email_obj = services.verify_token(token)
    if not did_verify:
        try:
            del request.session['email_id']
        except:
            pass
        messages.error(request, msg)
        return redirect("/login/")
    messages.success(request, msg)
    request.session['email_id'] = f"{email_obj.id}"
    next_url = request.session.get('next_url') or "/"
    if not next_url.startswith("/"):
        next_url = "/"
    return redirect(next_url)


# 6:19:34
# handling logout 