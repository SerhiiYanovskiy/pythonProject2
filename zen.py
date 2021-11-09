from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.urls import path
from django.conf import settings
import importlib.util

settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    SECRET_KEY='gggg'
)


TEMPLATE = """
<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
    <div>
     {content}
    </div>
  </body>
</html>  
    """


def mod_handler(request, mod_name):
    if importlib.util.find_spec(mod_name) == None:
        return HttpResponse(status=404)
    else:
        list = [x for x in dir(__import__(mod_name)) if not x.startswith('_')]
        links = ['<a href ="{}">{}</a><br>'.format(name,name) for name in list]
        return HttpResponse(TEMPLATE.format(content=''.join(links),))


def obj_handler(request, mod_name, obj_name):
    link = [
            '<pre style="word-wrap: break-word; white-space: pre-wrap;"> {} </pre>'
            .format(getattr(__import__(mod_name), obj_name).__doc__)
           ]
    return HttpResponse(TEMPLATE.format(content=link))




urlpatterns = [
               path('doc/<mod_name>', mod_handler),
               path('doc/<mod_name>/<obj_name>', obj_handler)
              ]


if __name__ == '__main__':
    execute_from_command_line()