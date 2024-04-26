self.client.force_login()

<!-- # JURE -->
now I'm running tests:
python manage.py test .\core\tests\
python manage.py test .\shop\tests\

How to run all tests at once?
Now I do:
python manage.py test .\core\tests\ .\shop\tests\

But in documentation is just:
python manage.py test