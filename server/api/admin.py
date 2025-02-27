from django.contrib import admin

# Register your models here.
from api.models import TaskState, Task, User, Guild

admin.site.register(TaskState)
admin.site.register(Task)
admin.site.register(User)
admin.site.register(Guild)
