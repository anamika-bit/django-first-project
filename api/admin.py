from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Country,State,City

# Register your models here.
admin.site.register(User)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)

#class AccountAdmin(UserAdmin):
#    list_display = ('email', 'name','date-joined', 'last-login', 'is_admin', 'is_staff')
#    search_fields = ('email')
#    readonly_fields = ('id', 'date-joined', 'last-login')

#    fieldsets = ()
#    filter_horizontal = ()
#    list_filter = ()

#admin.site.register(User, AccountAdmin)