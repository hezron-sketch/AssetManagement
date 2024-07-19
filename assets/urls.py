from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('track/', views.track, name='track'),
    path('maintenance/', views.maintenance, name='maintenance'),
    path('return/<int:lend_id>/', views.return_asset, name='return_asset'),
    path('fix/<int:maintenance_id>/', views.fix_asset, name='fix_asset'),
    path('get-asset-ids/', views.get_asset_ids, name='get_asset_ids'),
]
