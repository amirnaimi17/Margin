from django.contrib import admin

from margin_check.models import CI050


# Register your models here.
class CI050Admin(admin.ModelAdmin):
    pass


admin.site.register(CI050, CI050Admin)
