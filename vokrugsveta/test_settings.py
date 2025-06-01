from .settings import *  
  
DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.sqlite3',  
        'NAME': ':memory:',  
    }  
}  
  
# Полностью отключаем миграции  
MIGRATION_MODULES = {}