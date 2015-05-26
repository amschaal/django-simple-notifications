from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.utils.module_loading import import_string
from django.conf import settings
from notifications.models import NotificationType

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--long', '-l', dest='long',
            help='Help for the long options'),
    )
    help = 'Synchronize notification types included in NOTIFICATION_TYPES setting'
    def handle(self, **options):
        notification_type_dictionaries = getattr(settings,'NOTIFICATION_TYPES')
        for notification_type_dictionary in notification_type_dictionaries:
            notification_types = import_string(notification_type_dictionary)
            for type_id, type_kwargs in notification_types.iteritems():
                try:
                    obj = NotificationType.objects.get(id=type_id)
                    obj.name = type_kwargs['name']
                    obj.aggregable = type_kwargs['aggregable']
                    if hasattr(type_kwargs, 'description'):
                        obj.description = type_kwargs['description']
                    obj.save()
                    print "Updated notification type: " + type_id
                except NotificationType.DoesNotExist:
                    values = {'id':type_id,'name':type_kwargs['name'],'aggregable':type_kwargs['aggregable']}
                    if hasattr(type_kwargs, 'description'):
                        values['description'] = type_kwargs['description']
                    obj = NotificationType.objects.create(**values)
                    print "Created notification type: " + type_id