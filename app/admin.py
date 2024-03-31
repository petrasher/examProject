from django.contrib import admin
import inspect
import app.models


get_all_members = inspect.getmembers(app.models, inspect.isclass)
for model in get_all_members: print(model[0])
for model in get_all_members: admin.site.register(model[1])