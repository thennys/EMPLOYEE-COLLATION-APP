from django.urls import path

from .import views 

app_name = "employee"

urlpatterns = [
	path("", views.EmployeeListView ,name="list-employees"),
	path("add-employee", views.AddEmployeeView, name="add-employee"),
	path("upload-excel-file", views.ExcelDataUploadView, name="upload-excel"),
	path("upload-logs", views.UploadLogsView, name="logs-employees"),

	path("login/", views.LoginView, name="login"),
	path("logout", views.Logout, name="logout")
]