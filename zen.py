from django.shortcuts import render, redirect
from django.urls import path
import string
from django.core.management import execute_from_command_line
from django.db import connection, IntegrityError
import random
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DEBUG=True,
ROOT_URLCONF='zen'
ALLOWED_HOSTS = ['*']
SECRET_KEY = 'Test'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],

}
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR/'urldb.sqlite3'
    }
}
CREATE_URLS_TABLE = '''
CREATE TABLE IF NOT EXISTS urls (
url_key CHAR(5) PRIMARY KEY,
url TEXT
);
'''
INSERT_INTO_URLS = '''
INSERT INTO urls (url_key, url)
VALUES (%s, %s);
'''
SELECT_FROM_URLS = '''
SELECT url
FROM urls
WHERE url_key = %s;
'''




def create_table(create_query):
    with connection.cursor() as c:
        c.execute(create_query)



def handler(request):
    text= {}
    if request.method == 'POST':
        url = request.POST['url']
        text['url'] = url
        if url.lower().startswith(('http:', 'https:', 'ftp:')):
            text['is_valid'] = True
            unique_id_found = False
            while not unique_id_found:
                letters = string.ascii_letters
                digits = string.digits
                key = ''.join(random.choice(letters + digits) for i in range(5))
                url_key = key
                with connection.cursor() as c:
                    try:
                        c.execute(INSERT_INTO_URLS, (url_key, url))
                        unique_id_found = True
                    except IntegrityError as e:
                        if 'unique constraint' in e.args[0].lower():
                            print(f" {url_key} such a key is in the database.")
            text['url_key'] = url_key
    return render(request, 'index.html', text)


def url_handler(request, url_key):
    with connection.cursor() as c:
        c.execute(SELECT_FROM_URLS, [url_key])
        row = c.fetchone()
        url = row[0] if row else '/'
        return redirect(url)




urlpatterns = [
    path('', handler),
    path('<url_key>',url_handler),
]

create_table(CREATE_URLS_TABLE)
if __name__ == '__main__':
    execute_from_command_line()