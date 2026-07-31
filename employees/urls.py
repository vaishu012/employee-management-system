from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.add_employee, name="add_employee"),

    # new url
    path("edit/<int:id>/", views.edit_employee, name="edit_employee"),
    path("delete/<int:id>/", views.delete_employee, name="delete_employee"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("export-excel/", views.export_excel, name="export_excel"),
    path("export-pdf/", views.export_pdf, name="export_pdf"),
]