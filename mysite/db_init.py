# Usage:  python manage.py shell < db_init.py

from django.contrib.auth.models import User, Group, Permission

def notify(_type, _name, _created):
    if _created:
        print("%s %s has been created" % (_type,_name))
    else:
        print("%s %s already exists (skipped)" % (_type,_name))

def notify_group(_type, _created, _skipped):
    print("%s --> %s new instances were created, %s were skipped (already exist)" % (_type,_created,_skipped))

# ------------------------------------------------------------- G R O U P S -------------------------------------------------------------------------

groups = Group.objects
permissions = Permission.objects

obj, created = groups.get_or_create(name='Advanced Users')
if created:
    obj.permissions.add(permissions.get(name='Can add group'))
    obj.permissions.add(permissions.get(name='Can change group'))
    obj.permissions.add(permissions.get(name='Can delete group'))
    obj.save()
notify('Group', obj.name, created)

obj, created = groups.get_or_create(name='Basic Users')
notify('Group', obj.name, created)

# -------------------------------------------------------------- U S E R S --------------------------------------------------------------------------

users = User.objects

# Staff (ID=1):
obj, created = users.get_or_create(username='admin', first_name='Admin', last_name='Admin', email='admin@domain.com', is_active=True, is_staff=True, is_superuser=True)
if created:
    obj.set_password('123456')
    obj.profile.email_confirmed=True
    obj.profile.org_name='Place-Holder'
    obj.save()
notify('User', obj.username, created)

# Advanced User (ID=2):
obj, created = users.get_or_create(username='george.eliot@gmail.com', first_name='George', last_name='Eliot', email='george.eliot@gmail.com', is_active=True, is_staff=False, is_superuser=False)
if created:
    obj.set_password('123456')
    obj.profile.email_confirmed=True
    obj.profile.org_name='Place-Holder'
    obj.groups.add(groups.get(name='Advanced Users'))
    obj.save()
notify('User', obj.username, created)

# Advanced User (ID=3):
obj, created = users.get_or_create(username='mark.twain@gmail.com', first_name='Mark', last_name='Twain', email='mark.twain@gmail.com', is_active=True, is_staff=False, is_superuser=False)
if created:
    obj.set_password('123456')
    obj.profile.email_confirmed=True
    obj.profile.org_name='Place-Holder'
    obj.groups.add(groups.get(name='Basic Users'))
    obj.save()
notify('User', obj.username, created)

# ---------------------------------------------------------------------------------------------------------------------------------------------------

print("Done")

