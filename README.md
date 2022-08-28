# django-photo-app
Django photo app for django-graphene

# Usage

- Clone [django-graphene](https://github.com/kennyhyun/django-graphene.git) first and setup
- in the django-graphene directory, add this repo as a submodule `photo`
  - `git submodule add https://github.com/kennyhyun/django-photo-app.git photo`
- add `photo` to `INSTALLED_APPS` in `core/settings.py`
- add `Query` and `Mutate` from `django-photo-app` to the `core/schema.py`
- run migration
  - `./manage.py migrate`

![image](https://user-images.githubusercontent.com/5399854/187075187-7dab510c-c527-41e6-939e-a66702b35fa4.png)

