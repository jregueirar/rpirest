## Description

The Browseable REST API for your Raspberry IOT Projects

## Features

* API Rest browseable and documented
* APIRest modular, it is easily extending its functions.
* Support for asyncronous tasks (Long Polling).
* Massive deployment and configuration control with ansible.
* Security management, creation and management of API users.
* Open Source, with widely used technologies.

## Installation
* Install Raspbian in a RaspberryPi 2 or 3 with ssh access

* Desployment with Ansibble

```bash
git clone https://github.com/jregueirar/ansible-rpirest
ansible-galaxy install -r requiriments.yml
#Edit inventory file with your Raspberrypi infraestructure
ansible-playbook pirest-sense-hat.yml -l rpis -i inventory
```

* Create superuser for login in the GUI

```bash
ssh rpi
cd /opt/rpirest
python3 manage.py createsuperuser --username admin --email admin@localhost --noinput
python3 manage.py changepassword admin
```

* Login in the GUI with the superuser credentials

## Extending the API REST

If you have python know and you know how the DRF works, you can extend
this Framework. You can add support to a new shield, sensor or gadget
connected to your Raspberry.

You only have to follow these steps:

- Create a new django application: python3 manage.py startapp <name_app>
- Create a API REST with DRF using the class MyRouter() from core.common
- Make the Rest API Available editing rpirest/urls.py using the router
created.

Here is an example, extracted from the apires_dht app code:

```python
### file apirest_dht/views.py

def routes():

    router = MyRouter()
    router.register(r'env_sensor/humidity', HumidityView, base_name='dht_humidity')
    router.register(r'env_sensor/temperature', TemperatureView, base_name='dht_temperature')
    return router.urls
```

```python
### file rpirest/urls.py
   ........
   #APIs DRF
    url(r'^api/v1/dht11/', include(dht_routes()), {'device': "dht11"}),
   .........
```
## Screenshots

![index01](screenshots/rpirest_index01.png)

![index02](screenshots/rpirest_index02.png)



