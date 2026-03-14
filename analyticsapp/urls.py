from django.urls import path
from . import views

urlpatterns = [
    # Web Pages
    path('', views.dashboard_view, name='home'),
    path('reports/', views.reports_view, name='reports'),
    path('prediction/', views.prediction_view, name='prediction'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # APIs
    path('api/sales/', views.sales_api, name='sales_api'),
    path('api/reports/', views.reports_api, name='reports_api'),
    path('api/predict/', views.predict_api, name='predict_api'),
]






# from django.urls import path
# from . import views

# urlpatterns = [
#     path("", views.dashboard, name="dashboard"),
#     path("reports/", views.reports_view, name="reports"),
#     path("prediction/", views.prediction_view, name="prediction"),
# ]