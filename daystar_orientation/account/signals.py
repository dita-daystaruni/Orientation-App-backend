from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from .models import Account
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=Account)
def set_first_time_user_flag(sender, instance, created, **kwargs):
    """Set the is_first_time_user flag to True for regular users."""
    if created and instance.user_type == 'regular':
        instance.is_first_time_user = True
        instance.save()

@receiver(post_save, sender=Account)
def assign_permissions_based_on_user_type(sender, instance, created, **kwargs):
    """Assign permissions based on user type after saving the Account instance."""
    set_permissions(instance)

def set_permissions(user):
    """Set permissions based on user type."""
    if user.user_type == 'admin':
        user.user_permissions.set(Permission.objects.all())
    elif user.user_type in ['parent', 'regular']:
        view_permissions = Permission.objects.filter(codename__startswith='view_')
        user.user_permissions.set(view_permissions)

@receiver(post_save, sender=Account)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Create a token for the user after saving the Account instance."""
    if created:
        Token.objects.create(user=instance)