from django.urls import path
from . import views
from django.conf.urls import include, url
from django.contrib.auth import logout

app_name = 'webapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('journals', views.AddJournalView.as_view(), name='add_journal'),
    path('assets', views.AddAssetView.as_view(), name='add_asset'),
    path('liability', views.AddLiabilityView.as_view(), name='add_liability'),
    path('income', views.AddIncomeView.as_view(), name='add_income'),
    path('cost', views.AddCostView.as_view(), name='add_cost'),
    path('journals/<int:pk>/', views.JournalDetailView.as_view(), name='journal_detail'),
    path('journals/<int:pk>/records/', views.RecordView.as_view(), name='records'),
    path('journals/<int:pk>/records/<int:record_pk>', views.RecordDetailView.as_view(), name='record_detail'),
    # path('fstatement_detail/<int:pk>', views.FstatementView.as_view(), name='fstatement'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('signup', views.CreateUserView.as_view(), name='signup'),
]

