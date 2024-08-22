from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    '''Custom admin for the Account model'''
    model = Account
    
    list_display = ['id', 'admission_number', 'course', 'email', 'first_name', 'last_name', 'campus', 'user_type', 'phone_number', 'is_first_time_user', 'parent', 'username', 'gender', 'accomodation', 'checked_in', 'password']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'phone_number', 'admission_number', 'course', 'campus', 'gender', 'accomodation')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('admission_number', 'email', 'first_name', 'last_name', 'username', 'campus', 'course', 'phone_number', 'user_type', 'password1', 'password2', 'gender', 'accomodation', 'checked_in'),
        }),
    )


    def get_queryset(self, request):
        '''Gets the queryset for the Account model'''
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.user_type == 'admin':
            return qs
        return qs.filter(id=request.user.id)

    def has_change_permission(self, request, obj=None):
        '''Checks if the user has permission to change the Account model'''
        if request.user.user_type == 'admin' or request.user.is_superuser:
            return True
        return obj is None or obj == request.user

    def has_add_permission(self, request):
        '''Checks if the user has permission to add an Account model'''
        if request.user.user_type == 'admin' or request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        '''Checks if the user has permission to delete an Account model'''
        if request.user.user_type == 'admin' or request.user.is_superuser:
            return True
        return obj is None or obj == request.user

admin.site.register(Account, AccountAdmin)