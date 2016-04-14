from django import forms
from notifications.models import NotificationTypeSubscription
from django.forms.models import modelformset_factory
class NotificationTypeSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NotificationTypeSubscription
        fields = ('subscribe','email')
#     def __init__(self,*args,**kwargs):
#         user = kwargs.pop('user')
#         super(SubscriptionForm,self ).__init__(*args,**kwargs)
#         #Don't allow updates of id because it won't get cascaded
#         if self.instance.id:
#             self.fields.pop('id')

NotificationSubscriptionFormset = modelformset_factory(NotificationTypeSubscription,form=NotificationTypeSubscriptionForm,extra=0)