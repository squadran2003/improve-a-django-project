# improve-a-django-project
improving a previously built django project

# Motivation
9th project as part of the Python Web developement

# Installation
* Create a virtual env that uses Python3 by running the command below
	* virtualenv -p python3 yourdirectory
* Clone the repo
* activate the enviroment by running the command below
	* source bin/activate
* change directory into improve-a-django-project
* Run the requirements.txt file with the command below
	* pip install -r requirements.txt
* change directory into improve_django_v3
* then run python commnad below
	* python manage.py runserver

# Running Tests
* Navigate to the directory that contains the manage.py file
* run the commands below
  * coverage run manage.py test
  * coverage report --include="./*"

