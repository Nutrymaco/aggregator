"""aggregator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from storage.views import vacancies, possible_query_list
from monitoring.views import cached_query, key_words_invert_index, query_statistic

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vacancies/', vacancies),
    path('api/autocomplete/', possible_query_list),
    path('monitoring/cached_query/', cached_query),
    path('monitoring/key_words_index/', key_words_invert_index),
    path('monitoring/query_statistic/', query_statistic)
]
