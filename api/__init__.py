# FLASK API CONFIG

import jinja2
from api.endpoints import app as application

# Loading template and static folders
my_loader = jinja2.ChoiceLoader([
        application.jinja_loader,
        jinja2.FileSystemLoader(['./templates', './static']),
    ])
application.jinja_loader = my_loader
