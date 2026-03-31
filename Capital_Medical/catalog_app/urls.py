from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from catalog_app import views


urlpatterns = [
    path("", views.CategoryList.as_view()),
    path("<int:pk>/", views.CategoryDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)