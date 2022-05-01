import os
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import EmployeeRecords, Supervisors, UploadLogs
from .excel_uploads import ValidateSupervisorCreation, UploadExcelAndValidation
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def LoginView(request):
	if request.method=="POST":
		username 		= request.POST.get("username")
		password 		= request.POST.get("password")
		user 			= authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('employee:list-employees')

		else:
			messages.error(request, "Please enter the correct username and password. Note that both fields may be case-sensitive")
			
	return render(request, 'login.html')

@login_required
def Logout(request):
	logout(request)
	return redirect('/login')

@login_required
def EmployeeListView(request):
	employees  	= EmployeeRecords.objects.all().order_by('first_name')
	context 	= {"employees":employees}
	return render(request, 'employee-list.html',context)

@login_required
def AddEmployeeView(request):
	employees 	= EmployeeRecords.objects.all()
	context 	= {"employees":employees}
	
	"""Taking form values on post"""
 
	if request.method =='POST':
		first_name    				=  request.POST.get('first_name')
		middle_name   				=  request.POST.get('middle_name')
		date_of_graduation     		=  request.POST.get('date_of_graduation')
		date_of_employment  		=  request.POST.get('date_of_employment')
		position					=  request.POST.get('position')
		salary						=  request.POST.get('salary')
		getSupervisors				=  request.POST.getlist('get_supervisor')
		
		try:
			employee 		= EmployeeRecords.objects.create(
								first_name=first_name, middle_name=middle_name,
								date_of_graduation=date_of_graduation, 
								date_of_employment=date_of_employment, position=position,
								salary=salary)
			employee.save()

			"""If no supervisor was selected"""
			if len(getSupervisors)==0:
				pass
			# If one or more supervisor(s) were selected
			else:
				for supervisor_code in getSupervisors:
					supervisor_key_name = ValidateSupervisorCreation(supervisor_code)
					
					# If the employee already have a supervisor account
					if Supervisors.objects.filter(supervisor=supervisor_key_name).exists():
						supervisor = Supervisors.objects.get(supervisor=supervisor_key_name)
						employee.supervisors.add(supervisor)

					# If the employee does not have a supervisor account
					else:
						supervisor = Supervisors.objects.create(supervisor=supervisor_key_name)
						supervisor.save()
						employee.supervisors.add(supervisor)

			saveLog 		= UploadLogs.objects.create(
								number_of_employee_records_uploaded= 1,
								status="Success", number_of_duplicate_entries=0)
			saveLog.save()

			messages.success(request, "Employee added successfully")
			return render(request, 'add-employee.html', context)

		except Exception as e:
			messages.error(request, str(e))
	return render(request, 'add-employee.html',context)

@login_required
def ExcelDataUploadView(request):
	if request.method == "POST":
		excel_file     			= request.FILES.get("employee_excel_file")
		# Getting filename and extension
		file_name, extension 	= os.path.splitext(excel_file.name)
				
		if '.xlsx' == extension:
			uploadAndCheck 		= UploadExcelAndValidation(excel_file)
			# Checking if any error occured
			if uploadAndCheck[2]==True:
				messages.error(request, uploadAndCheck[3])

			# Valid file
			else:
				messages.success(request, "Employee Data uploaded successfully")
				return render(request, 'excel-file-upload.html')
		
		# If file wasn't a '.xlsx'
		else:
			messages.error(request, "Invalid file upload, please upload an excel file")
			return render(request, 'excel-file-upload.html')

	return render(request, 'excel-file-upload.html')

@login_required
def UploadLogsView(request):
	logs 		= UploadLogs.objects.all()
	context 	= {"logs":logs}
	return render(request, 'logs.html', context)







