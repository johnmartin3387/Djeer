from django.contrib import admin

from djeer_auth.models import *
# Register your models here.

class PersonAdmin(admin.ModelAdmin):
    model = Person
    list_display = ['id', 'email', 'first_name', 'last_name', 'role', 'birthday', 'description', 'active']

admin.site.register(Person, PersonAdmin)


class DjAdmin(admin.ModelAdmin):
    model = Dj
    list_display = ['title', 'rate', 'discount_rate', 'discount_hour', 'event_type', 'genre']

admin.site.register(Dj, DjAdmin)


class HelpAdmin(admin.ModelAdmin):
    model = Help
    list_display = ['title', 'content', 'get_parent']

    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'parent', 'sort')
        }),
    )

    def get_parent(self, obj):
    	if obj.parent == None:
    		return "Top Level"
        return obj.parent.title

admin.site.register(Help, HelpAdmin)

'''class HostAdmin(admin.ModelAdmin):
    model = Host
    list_display = ['event_type', 'genre']

admin.site.register(Host, HostAdmin)

class EquipmentAdmin(admin.ModelAdmin):
    model = Equipment

admin.site.register(Equipment, EquipmentAdmin)

class AddressAdmin(admin.ModelAdmin):
    model = Address
    list_display = ['street', 'city', 'state', 'country']

admin.site.register(Address, AddressAdmin)

admin.site.register(Schedule)
admin.site.register(Event)
admin.site.register(Bid)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Notification)'''