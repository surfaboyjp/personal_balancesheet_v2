from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import get_user_model


ASSET_CATEGORIES = (
    ("L", "流動資産"),
    ("F", "固定資産"),
    ("D", "繰越資産"),
)

LIABILITY_CATEGORIES = (
    ("L", "流動負債"),
    ("F", "固定負債"),
)

INCOME_CATEGORIES = (
    ("M", "メイン収入"),
    ("S", "サブ収入"),
)

COST_CATEGORIES = (
    ("L", "流動支出"),
    ("F", "固定支出"),
)


User = get_user_model()


class Journal(models.Model):
    name = models.CharField("帳簿名", max_length=64)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    def __str__(self):
        return str(self.name)


class JournalRecord(models.Model):
    name = models.CharField("帳簿名", max_length=64)
    journal = models.ForeignKey(Journal, on_delete=models.PROTECT)
    closed_at = models.DateField("決算日", auto_now_add=True)
    # data_json = models.TextField("帳簿データのJSON")
    asset_sum = models.IntegerField("資産合計", default=0)
    liquid_asset_sum = models.IntegerField("流動資産合計", default=0)
    liquid_asset_list = models.TextField("流動資産リスト", default=0)
    fixed_asset_sum = models.IntegerField("固定資産合計", default=0)
    fixed_asset_list = models.TextField("固定資産リスト", default=0)
    deferred_asset_sum = models.IntegerField("繰越資産合計", default=0)
    deferred_asset_list = models.TextField("繰越資産リスト", default=0)
    liability_sum = models.IntegerField("負債合計", default=0)
    liquid_liability_sum = models.IntegerField("流動負債合計", default=0)
    liquid_liability_list = models.TextField("流動負債リスト", default=0)
    fixed_liability_sum = models.IntegerField("固定負債合計", default=0)
    fixed_liability_list = models.TextField("固定負債リスト", default=0)
    capital = models.IntegerField("総資産", default=0)
    liability_capital_sum = models.IntegerField("負債・純資産合計", default=0)
    income_sum = models.IntegerField("収入合計", default=0)
    main_income_sum = models.IntegerField("メイン収入合計", default=0)
    main_income_list = models.TextField("メイン収入リスト", default=0)
    sub_income_sum = models.IntegerField("サブ収入合計", default=0)
    sub_income_list = models.TextField("サブ収入リスト", default=0)
    cost_sum = models.IntegerField("支出合計", default=0)
    liquid_cost_sum = models.IntegerField("流動支出合計", default=0)
    liquid_cost_list = models.TextField("流動支出リスト", default=0)
    fixed_cost_sum = models.IntegerField("固定支出合計", default=0)
    fixed_cost_list = models.TextField("固定支出リスト", default=0)
    saving = models.IntegerField("繰越資産", default=0)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    def __str__(self):
        return str(self.name)


class Asset(models.Model):
    name = models.CharField("資産名", max_length=64)
    journal = models.ForeignKey(Journal, on_delete=models.PROTECT)
    value = models.IntegerField("残額")
    category = models.CharField("カテゴリー", choices=ASSET_CATEGORIES, max_length=2)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    def __str__(self):
        return str(self.name)


class Liability(models.Model):
    name = models.CharField("負債名", max_length=64)
    journal = models.ForeignKey(Journal, on_delete=models.PROTECT)
    value = models.IntegerField("残額")
    category = models.CharField("カテゴリー", choices=LIABILITY_CATEGORIES, max_length=2)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    def __str__(self):
        return str(self.name)


class Income(models.Model):
    name = models.CharField("収入名", max_length=64)
    journal = models.ForeignKey(Journal, on_delete=models.PROTECT)
    value = models.IntegerField("残額")
    category = models.CharField("カテゴリー", choices=INCOME_CATEGORIES, max_length=2)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    def __str__(self):
        return str(self.name)


class Cost(models.Model):
    name = models.CharField("支出名", max_length=64)
    journal = models.ForeignKey(Journal, on_delete=models.PROTECT)
    value = models.IntegerField("残額")
    category = models.CharField("カテゴリー", choices=COST_CATEGORIES, max_length=2)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    def __str__(self):
        return str(self.name)
