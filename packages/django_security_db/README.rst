===========
security_db
===========

security_db provides models to use in every container of the pyfolio project as
well as classes for interfacing with said models in an easy and understandable
way.


usage:
1. Add "security_db" to your INSTALLED_APPS like this:
    INSTALLED_APPS = [
        ...,
        'security_db',
    ]

2. Run 'python manage.py sqlmigrate' to create the models
