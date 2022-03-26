from django.contrib import admin
from employee.models import EmployeeRecords,Supervisors,UploadLogs

# Register your models here
class AdminEmployeeDisplay(admin.ModelAdmin):
	list_filter = ["position"]

class AdminUploadLogsDisplay(admin.ModelAdmin):
	list_display = ["timestamp_of_upload","status"]
	
admin.site.register(EmployeeRecords, AdminEmployeeDisplay) 
admin.site.register(UploadLogs, AdminUploadLogsDisplay)
admin.site.register(Supervisors)

