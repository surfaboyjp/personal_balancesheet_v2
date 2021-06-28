from django.shortcuts import render
from django.views import generic
from django.views.generic import TemplateView, DetailView, ListView, CreateView
from .models import *
from django.views.generic.list import MultipleObjectMixin  # この行を追加
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
import numpy
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
import json


class IndexView(TemplateView):
    template_name = 'webapp/index.html'

    def get_context_data(self, **kwargs):
        journal_list = Journal.objects.filter(user=self.request.user).all().order_by('-created_at')
        params = {
            'journal_list': journal_list,
        }
        return params

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class JournalDetailView(DetailView, MultipleObjectMixin):
    model = Journal
    template_name = 'webapp/journal_detail.html'

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login')

        journal = Journal.objects.get(id=kwargs.get('pk'))
        print(journal)
        if not journal.user == request.user:
            return redirect('/')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = {
            'journal_id': kwargs.get('pk'),
            'bs': self.get_bs_dict(),
            'pl': self.get_pl_dict(),
            'records': self.get_records(),
        }
        return context

    def get_records(self):
        records = list(JournalRecord.objects.filter(journal=self.kwargs.get('pk')).order_by('-closed_at').values())[:11]
        return records

    def get_bs_dict(self):
        assets = list(Asset.objects.filter(journal=self.kwargs.get('pk')).all().values())
        liabilities = list(Liability.objects.filter(journal=self.kwargs.get('pk')).all().values())
        liquid_assets = [x for x in assets if x['category'] == 'L']
        la_sum = get_value_sum(liquid_assets)
        fixed_assets = [x for x in assets if x['category'] == 'F']
        fa_sum = get_value_sum(fixed_assets)
        deferred_assets = [x for x in assets if x['category'] == 'D']
        da_sum = get_value_sum(deferred_assets)

        liquid_liabilities = [y for y in liabilities if y['category'] == 'L']
        ll_sum = get_value_sum(liquid_liabilities)
        fixed_liabilities = [y for y in liabilities if y['category'] == 'F']
        fl_sum = get_value_sum(fixed_liabilities)

        asset_sum = la_sum + fa_sum + da_sum
        liability_sum = ll_sum + fl_sum
        capital = asset_sum - liability_sum
        liability_capital_sum = liability_sum + capital

        get_rate_in_list(liquid_assets, asset_sum)
        get_rate_in_list(fixed_assets, asset_sum)
        get_rate_in_list(deferred_assets, asset_sum)
        get_rate_in_list(liquid_liabilities, asset_sum)
        get_rate_in_list(fixed_liabilities, asset_sum)

        liquid_asset_rate = numpy.float64(la_sum) / asset_sum * 100
        fixed_asset_rate = numpy.float64(fa_sum) / asset_sum * 100
        deferred_asset_rate = numpy.float64(da_sum) / asset_sum * 100
        liquid_liability_rate = numpy.float64(ll_sum) / liability_sum * 100
        fixed_liability_rate = numpy.float64(fl_sum) / liability_sum * 100
        capital_rate = numpy.float64(capital) / liability_capital_sum * 100

        bs = {
            'asset': asset_sum,
            'liquid_assets': la_sum,
            'liquid_asset_rate': liquid_asset_rate,
            'liquid_asset_list': liquid_assets,
            'fixed_assets': fa_sum,
            'fixed_asset_rate': fixed_asset_rate,
            'fixed_asset_list': fixed_assets,
            'deferred_assets': da_sum,
            'deferred_asset_rate': deferred_asset_rate,
            'deferred_asset_list': deferred_assets,
            'liability': liability_sum,
            'liquid_liability': ll_sum,
            'liquid_liability_rate': liquid_liability_rate,
            'liquid_liability_list': liquid_liabilities,
            'fixed_liability': fl_sum,
            'fixed_liability_rate': fixed_liability_rate,
            'fixed_liability_list': fixed_liabilities,
            'capital': capital,
            'capital_rate': capital_rate,
            'liability_capital_sum': liability_capital_sum ,
        }
        return bs

    def get_pl_dict(self):
        incomes = list(Income.objects.filter(journal=self.kwargs.get('pk')).all().values())
        costs = list(Cost.objects.filter(journal=self.kwargs.get('pk')).all().values())
        main_incomes = [y for y in incomes if y['category'] == 'M']
        mi_sum = get_value_sum(main_incomes)
        sub_incomes = [y for y in incomes if y['category'] == 'S']
        si_sum = get_value_sum(sub_incomes)

        liquid_costs = [y for y in costs if y['category'] == 'L']
        lc_sum = get_value_sum(liquid_costs)
        fixed_costs = [y for y in costs if y['category'] == 'F']
        fc_sum = get_value_sum(fixed_costs)

        income_sum = mi_sum + si_sum
        cost_sum = lc_sum + fc_sum
        saving = income_sum - cost_sum

        get_rate_in_list(main_incomes, income_sum)
        get_rate_in_list(sub_incomes, income_sum)
        get_rate_in_list(liquid_costs, income_sum)
        get_rate_in_list(fixed_costs, income_sum)

        cost_rate = numpy.float64(cost_sum) / income_sum * 100
        main_income_rate = numpy.float64(mi_sum) / income_sum * 100
        sub_income_rate = numpy.float64(si_sum) / income_sum * 100
        liquid_cost_rate = numpy.float64(lc_sum) / income_sum * 100
        fixed_cost_rate = numpy.float64(fc_sum) / income_sum * 100
        saving_rate = numpy.float64(saving) / income_sum * 100

        pl = {
            'income': income_sum,
            'main_incomes': mi_sum,
            'main_income_rate': main_income_rate,
            'main_income_list': main_incomes,
            'sub_incomes': si_sum,
            'sub_income_rate': sub_income_rate,
            'sub_income_list': sub_incomes,
            'cost': cost_sum,
            'cost_rate': cost_rate,
            'liquid_costs': lc_sum,
            'liquid_cost_rate': liquid_cost_rate,
            'liquid_cost_list': liquid_costs,
            'fixed_costs': fc_sum,
            'fixed_cost_rate': fixed_cost_rate,
            'fixed_cost_list': fixed_costs,
            'saving': saving,
            'saving_rate': saving_rate,
        }
        return pl


class RecordView(TemplateView):
    model = JournalRecord
    template_name = 'webapp/records.html'

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login')

        journal = Journal.objects.get(id=kwargs.get('pk'))
        if not journal.user == request.user:
            return redirect('/')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        journal = Journal.objects.get(id=self.kwargs.get('pk'))
        records = JournalRecord.objects.filter(journal=journal).all().order_by('-created_at')
        context = {
            'journal_id': journal.id,
            'records_list': records,
        }
        return context


class RecordDetailView(DetailView):
    model = JournalRecord
    template_name = 'webapp/record_detail.html'

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login')

        record = JournalRecord.objects.get(id=kwargs.get('record_pk'))
        if not record.journal.user == request.user:
            return redirect('/')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        record = JournalRecord.objects.get(id=self.kwargs.get('record_pk'))
        la_json = json.loads(record.liquid_asset_list)
        record.liquid_asset_list = la_json

        fa_json = json.loads(record.fixed_asset_list)
        record.fixed_asset_list = fa_json

        da_json = json.loads(record.deferred_asset_list)
        record.deferred_asset_list = da_json

        ll_json = json.loads(record.liquid_liability_list)
        record.liquid_liability_list = ll_json

        fl_json = json.loads(record.fixed_liability_list)
        record.fixed_liability_list = fl_json

        mi_json = json.loads(record.main_income_list)
        record.main_income_list = mi_json

        si_json = json.loads(record.sub_income_list)
        record.sub_income_list = si_json

        lc_json = json.loads(record.liquid_cost_list)
        record.liquid_cost_list = lc_json

        fc_json = json.loads(record.fixed_cost_list)
        record.fixed_cost_list = fc_json
        context = {
            'record': record,
        }
        return context


# class FstatementView(DetailView):
#     model = Fstatement

class CreateUserView(CreateView):
    form_class = SignUpForm
    template_name = 'webapp/signup.html'
    success_url = reverse_lazy('webapp:index')

    def form_valid(self, form):
        user = form.save()
        self.object = user
        messages.info(self.request, 'ユーザー登録をしました。')
        return HttpResponseRedirect(self.get_success_url())


class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'webapp/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'webapp/login.html'


class AddAssetView(CreateView):
    template_name = 'webapp/add_asset.html'
    model = Asset
    form_class = AssetForm
    success_url = reverse_lazy('webapp:index')


class AddLiabilityView(CreateView):
    template_name = 'webapp/add_liability.html'
    model = Liability
    form_class = LiabilityForm
    success_url = reverse_lazy('webapp:index')


class AddIncomeView(CreateView):
    template_name = 'webapp/add_income.html'
    model = Income
    form_class = IncomeForm
    success_url = reverse_lazy('webapp:index')


class AddCostView(CreateView):
    template_name = 'webapp/add_cost.html'
    model = Cost
    form_class = CostForm
    success_url = reverse_lazy('webapp:index')


class AddJournalView(CreateView):
    template_name = 'webapp/add_journal.html'
    model = Journal
    form_class = JournalForm
    success_url = reverse_lazy('webapp:index')

    # def get(self, request, *args, **kwargs):
    #     form_class = self.get_form_class()
    #     form = form_class(user=request.user)
    #     return super(AddJournalView, self).get(self.request)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AddJournalView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # def form_valid(self, form):
    #     form['user'] = self.request.user
    #     form.save()
    #     # journal = form.save(commit=False)
    #     # journal.create_user = self.request.user
    #     # journal.save()
    #     return super().form_valid(form)


def get_value_sum(dict_list):
    result = 0
    for dict in dict_list:
        result += dict['value']
    return result


def get_rate_in_list(dict_list, sum_person):
    for item in dict_list:
        item_rate = numpy.float64(item['value']) / sum_person * 100
        item['rate'] = item_rate