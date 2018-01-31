Probando

## v.5 (2018-01-02

 - Divide and win. The ansible code is moved to other git project

## v0.401 (2017-12-17)
 - The script showTempRest.py. Example, using the HTTP-REST APIs of two devices.

## v0.4
 - It is used yaml files for the configuration of the devices conenneted to the RPi. Maybe in the future pass to json.

## v0.302 (2017-08-24)
 - Fix errors in the deployment of graphite.

## 0.301 (2017-08-21)
 - graphite-api is used instead graphite-web. graphite-api is installed from pip3 because
   the package doesn't exist for Raspbian Jessie.

## 0.3 (2017-07-18)
 - Support for logs, it is useful for debugging.
 - For time series charts, the javascript dygraph library is used.
 - For gauge charts, the javascript google chart library is used.
 - It is send metrics to the local graphite.
 - It isn't charged the python sense-hat library if the operative system isn't Raspbian (For example debug with vagrant).
 - Appearance is improved


## 0.202 (2017-05-04)

Bugfixes:
  - Fix HTMLs ids

## 0.201 (2017-05-01)

Bugfixes:
  - Fix templates dirtectory path. Use django default template setting.
  By convention DjangoTemplates looks for a “templates” subdirectory
  in each of the INSTALLED_APPS for look template source files.
  - Avoid error Cross Site Request Forgery. Retrieve CSRF-token in
  template base.html used in Jquery Request (XHR).

Features:
  - Built-int Login System. Bibliography:
    - https://docs.djangoproject.com/en/1.11/topics/auth/default/
    - http://blog.narenarya.in/right-way-django-authentication.html

Others:
  - Refactoring template code
  - Reorganizing URLs
  - Upgrade from Django 1.9.6 to Django 1.11

## 0.2 (2017-??)
  - Improving the appearance. We start the design of the APP.
  We copy the CSS template from

