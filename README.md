## Installation
* Install Raspbian in a RaspberryPi 2 or 3 with ssh access

* Desployment
  * cd deploy
  * Edit inventory file with your Raspberrypi infraestructure
  * ansible-galaxy install -r
  * ansible-playbook pirest-sense-hat.yml -l rpis -i inventory

* Create superuser for login in the GUI
  * ssh rpi
  * cd /opt/pirest_sense_hat
  * python3 manage.py createsuperuser --username admin --email admin@localhost --noinput
  * python3 manage.py changepassword admin

* Login in the GUI with the superuser credentials

## Screenshots

### Main Dashboard Page
![tutua](screenshots/env_sensors.png)


