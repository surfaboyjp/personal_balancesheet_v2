from django.core.management.base import BaseCommand
from ...models import *
from datetime import datetime
from ...views import get_value_sum
import json


class Command(BaseCommand):
    def handle(self, *args, **options):
        journal_list = list(Journal.objects.all().values())
        for x in journal_list:
            record_name = x['name'] + '-' + datetime.now().strftime('%Y/%M')
            journal = Journal.objects.get(id=x['id'])

            asset = list(Asset.objects.filter(journal=journal).all().values())
            liquid_assets = [x for x in asset if x['category'] == 'L']
            liquid_assets = del_detetme(liquid_assets)
            la_sum = get_value_sum(liquid_assets)
            fixed_assets = [x for x in asset if x['category'] == 'F']
            fixed_assets = del_detetme(fixed_assets)
            fa_sum = get_value_sum(fixed_assets)
            deferred_assets = [x for x in asset if x['category'] == 'D']
            deferred_assets = del_detetme(deferred_assets)
            da_sum = get_value_sum(deferred_assets)

            liability = list(Liability.objects.filter(journal=journal).all().values())
            liquid_liabilities = [y for y in liability if y['category'] == 'L']
            liquid_liabilities = del_detetme(liquid_liabilities)
            ll_sum = get_value_sum(liquid_liabilities)
            fixed_liabilities = [y for y in liability if y['category'] == 'F']
            fixed_liabilities = del_detetme(fixed_liabilities)
            fl_sum = get_value_sum(fixed_liabilities)

            asset_sum = la_sum + fa_sum + da_sum
            liability_sum = ll_sum + fl_sum
            capital = asset_sum - liability_sum
            liability_capital_sum = liability_sum + capital

            income = list(Income.objects.filter(journal=journal).all().values())
            main_incomes = [y for y in income if y['category'] == 'M']
            main_incomes = del_detetme(main_incomes)
            mi_sum = get_value_sum(main_incomes)
            sub_incomes = [y for y in income if y['category'] == 'S']
            sub_incomes = del_detetme(sub_incomes)
            si_sum = get_value_sum(sub_incomes)

            cost = list(Cost.objects.filter(journal=journal).all().values())
            liquid_costs = [y for y in cost if y['category'] == 'L']
            liquid_costs = del_detetme(liquid_costs)
            lc_sum = get_value_sum(liquid_costs)
            fixed_costs = [y for y in cost if y['category'] == 'F']
            fixed_costs = del_detetme(fixed_costs)
            fc_sum = get_value_sum(fixed_costs)

            income_sum = mi_sum + si_sum
            cost_sum = lc_sum + fc_sum
            saving = income_sum - cost_sum
            JournalRecord.objects.create(
                name=record_name,
                journal=journal,
                asset_sum=asset_sum,
                liquid_asset_sum=la_sum,
                liquid_asset_list=json.dumps(liquid_assets),
                fixed_asset_sum=fa_sum,
                fixed_asset_list=json.dumps(fixed_assets),
                deferred_asset_sum=da_sum,
                deferred_asset_list=json.dumps(deferred_assets),
                liability_sum=liability_sum,
                liquid_liability_sum=ll_sum,
                liquid_liability_list=json.dumps(liquid_liabilities),
                fixed_liability_sum=fl_sum,
                fixed_liability_list=json.dumps(fixed_liabilities),
                capital=capital,
                liability_capital_sum=liability_capital_sum,
                income_sum=income_sum,
                main_income_sum=mi_sum,
                main_income_list=json.dumps(main_incomes),
                sub_income_sum=si_sum,
                sub_income_list=json.dumps(sub_incomes),
                cost_sum=cost_sum,
                liquid_cost_sum=lc_sum,
                liquid_cost_list=json.dumps(liquid_costs),
                fixed_cost_sum=fc_sum,
                fixed_cost_list=json.dumps(fixed_costs),
                saving=saving,
            )


def del_detetme(target_list):
    for item in target_list:
        item.pop('created_at')
        item.pop('updated_at')
    return target_list
