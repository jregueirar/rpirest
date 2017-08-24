- vagrant up (to up virtualbox machine pirest01)
- ansible-playbook -i inventory -l pirest01 pirest-sense-hat.yml

TAGS
====

* grafana: To deploy only grafana (backend graphite)
* app_code: To deploy only change in the app code
* configuration: To deploy only change in configuration
* installation: To install all the necessary
