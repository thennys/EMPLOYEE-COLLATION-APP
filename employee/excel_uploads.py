from .models import EmployeeRecords, Supervisors, UploadLogs 
from openpyxl import Workbook
from openpyxl import load_workbook


"""Logical functions"""

def ValidateSupervisorCreation(get_employee_code):
	if EmployeeRecords.objects.filter(employee_code=get_employee_code).exists():
		employee 	= EmployeeRecords.objects.get(employee_code=get_employee_code)
		return employee.first_name+employee.middle_name
	else:
		return None



def UploadExcelAndValidation(excel_file):
	
	# Load spreadsheet
	work_book 				= load_workbook(excel_file, data_only=True)
	
	# Getting the active sheet
	rows 					= work_book.active
	total_rows				= 0
	succesful_rows_passed	= 0

	# Array: specifically to be used for handling duplicate entries
	duplicatedDetectArray = []
	duplicateDetectCount  = 0 

	error_message 		  = ""
	is_error 			  = False

	# Looping through number of individual row in total rows
	for a_row in rows:
		# Taking out the header in the excel file
		if total_rows==0:
			total_rows+=1
			pass
		
		# Getting a single row's values
		else:
			concatenateRowValues = "".replace(' ','')
			
			# Getting values from row in array
			a_row_value_array = []

			for a_row_value in a_row:
				# appending employee a_row_value_array
				a_row_value_array.append(a_row_value.value)
				# Concatenating
				concatenateRowValues+= str(a_row_value.value)
							
			# Checking and manipulating duplicate row data
			exists = concatenateRowValues in duplicatedDetectArray
			if exists ==True:
				duplicateDetectCount+=1
				pass
			# Creating employee
			else:
				first_name 				= a_row_value_array[0]
				middle_name 			= a_row_value_array[1]
				# Excel date entry validation
				try:
					if '"' not in a_row_value_array[2] and '"' not in a_row_value_array[3]:
						is_error 			= True
						error_message 		= "Please round your datetimes in quotation marks"
					else:
						date_of_graduation		= a_row_value_array[2].strip('"')
						date_of_graduation 		= date_of_graduation.strip("'")

						date_of_employment 		= a_row_value_array[3].strip('"')
						date_of_employment 		= date_of_employment.strip("'")
					
				except:
					is_error 			= True
					error_message		= "Datetime value expected. Please round your dates in column 4 and 5 in quotation marks"
					break

				position 				= a_row_value_array[4]
				try:
					salary 				= int(a_row_value_array[5])
				except:
					is_error 			= True
					error_message	 	= "Invalid input. Salary field expected a number"
					break

				supervisors				= a_row_value_array[6]
				
				# Saving employee into database
				try:
					employee 				= EmployeeRecords.objects.create(
												first_name=first_name, middle_name=middle_name,
												date_of_graduation=date_of_graduation, 
												date_of_employment=date_of_employment, position=position,
												salary=salary)
					

					# If no supervisor
					if supervisors==None:
						pass
					else:
						supervisor_key_name = ValidateSupervisorCreation(supervisors)
						# If the employee already have a supervisor account
						if Supervisors.objects.filter(supervisor=supervisor_key_name).exists():
							supervisor = Supervisors.objects.get(supervisor=supervisor_key_name)
							employee.supervisors.add(supervisor)

						# If the employee does not have a supervisor account
						else:
							supervisor = Supervisors.objects.create(supervisor=supervisor_key_name)
							supervisor.save()
							employee.supervisors.add(supervisor)

					succesful_rows_passed+=1
					duplicatedDetectArray.append(concatenateRowValues)

				except:
					is_error 		= True
					error_message 	= "Supervisor's employee code does not exist"
					break

							
			total_rows+=1
	# Saving and returning log
	if is_error==False:
		saveLog = UploadLogs.objects.create(
					number_of_employee_records_uploaded= succesful_rows_passed,
					status="Success",number_of_duplicate_entries=duplicateDetectCount)
		saveLog.save()

	else:
		saveLog = UploadLogs.objects.create(
					number_of_employee_records_uploaded= succesful_rows_passed,
					status = "Failed", errors=error_message, number_of_duplicate_entries=duplicateDetectCount)
		saveLog.save()

	return [duplicateDetectCount, succesful_rows_passed, is_error, error_message]
	
 
 
 
