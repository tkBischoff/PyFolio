from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from security_db.models import PyfolioUser, Security

from . import forms
# Create your views here.

@login_required
def buy_security(request, ticker):
    if request.method == 'POST':
        form = forms.BuySecurityForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user = PyfolioUser.objects.get(id=request.user.id)
            security = Security.get_by_ticker(ticker)

            user.invest(security, amount)

            return HttpResponseRedirect(reverse('home'))
    else:
        form = forms.BuySecurityForm()

    return render(request, 'buy_security.html', {'form': form, 'ticker': ticker})
