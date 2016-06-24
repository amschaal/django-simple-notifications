import django.dispatch

notification_created = django.dispatch.Signal(providing_args=["url", "text","type_id","importance","description","groups","users","groups","instance","super_users","exclude_user"])
