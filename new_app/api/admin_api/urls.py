from .get_company_info import GetCompanyInfoApi
from .get_companies import GetCompaniesApi
from django.urls import path, re_path, include

prefix = 'ad'
urlpatterns = [
    path('get-company-info', GetCompanyInfoApi.as_view(), name=f'{prefix}-get-company-info'),
    path('get-companies', GetCompaniesApi.as_view(), name=f'{prefix}-get-companies')
]