class NotificationConfiguration(object):
    name = 'Notification name'
    description = 'Description of notification'
    aggregable = False
    @classmethod
    def aggregated_text(cls,user_notifications):
        return "There are %d '%s' notifications" % (len(user_notifications), cls.name)
    @classmethod
    def aggregated_description(cls,user_notifications):
        return '\n'.join([un.notification.text for un in user_notifications])
    @classmethod
    def user_can_subscribe(cls,user):
        return True