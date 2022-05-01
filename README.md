EMPLOYMENT DATA COLLATION APP

- HOW TO RUN THE PROJECT
	NB: Python must be installed on your pc

	1. Create and activate a virtual environment using
	  $ py -3 -m venv ."<virtual environment name>"
	  $ .<virtual environment name>\scripts\activate
	2. Navigate to the projects root directory in a terminal

	4. Install all dependencies and packages using
	  $ pip install -r requirements.txt

	5. Create your msql database and change the DATABASE settings in the 
	project's settings.py file


	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.mysql',
	        'NAME': '<your database name>',
	        'USER': '<root username>',
	        'PASSWORD': '<database password>',
	        'HOST': '127.0.0.1',
	        'PORT': '<database port number>',
	    }
	}

	6. Admin user will automatically be created
	username: admin
	password: keypass

	7. Attached are the excel files for testing
			- user_data   : Valid Excel file
			- employee_records.xls 	  : Invalid excel file
			- employee_records.xlss : wrong file name


- URLS FOR ACCESSING THE WEB APPLICATION
	1. LOGIN PAGE 								:  http://127.0.0.1:8000/login/
	2. EMPLOYEE LIST PAGE 						:  http://127.0.0.1:8000
	3. MANUAL UPLOAD OF EMPLOYEE ON APP PAGE 	:  http://127.0.0.1:8000/add-employee
	4. ADD EMPLOYEES FROM EXCEL 				:  http://127.0.0.1:8000/upload-excel-file  
	5. VIEW ALL UPLOAD LOGS 					:  http://127.0.0.1:8000/upload-logs
	6. LOGOUT 									:  http://127.0.0.1:8000/logout


