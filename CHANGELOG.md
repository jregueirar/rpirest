

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

