from django.contrib import admin

from users.models import Users

@admin.register(Users)
class UniversalAdmin(admin.ModelAdmin):
    exclude = ('deleted_at',)

    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]













