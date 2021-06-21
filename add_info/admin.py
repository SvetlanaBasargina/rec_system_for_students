from django.contrib import admin
import add_info.models as m

# Register your models here.

admin.site.register(m.Role)
admin.site.register(m.Category)
admin.site.register(m.Item)
admin.site.register(m.Profile)
admin.site.register(m.UserItem)
admin.site.register(m.Photo)

@admin.register(m.InfoSource)
class InfoSourceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('type', 'category'),'createdUserRole')
        }),
        ('Настроки категории', {
            'fields': ('existOfName', 'itemNameKeywords', 'existOfScore', 'scoreKeywords')
        }),
        ('Описание элемента', {
            'fields': ('existOfDescription', 'isRequiredDescription')
        }),
    )

