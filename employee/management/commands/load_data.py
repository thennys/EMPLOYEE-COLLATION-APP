from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


""" using Django fixtures """
class Command(BaseCommand):
    help = 'Admin user automated creation'
    
    def handle(self,*args, **kwargs):
        User.objects.all().delete()
        admin_user = User(
            username="admin", 
            is_superuser=True)
        admin_user.set_password("keypass")
        admin_user.save()
        