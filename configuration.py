class NotificationConfiguration(object):
    name = 'Notification name'
    description = 'Description of notification'
    aggregable = False
    @classmethod
    def aggregated_text(cls,notifications):
        return "There are %d '%s' notifications" % (len(notifications), cls.name)
    @classmethod
    def aggregated_description(cls,notifications):
        return '\n'.join([n.text for n in notifications])
    @classmethod
    def user_can_subscribe(cls,user):
        return True