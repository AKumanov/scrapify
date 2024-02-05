from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete, post_save
from django.contrib.auth.models import User
from scrapify.settings import AUTH_USER_MODEL

from .models import CustomUser, BaseUser

UserModel = get_user_model

def delete_user(sender, instance, **kwargs):
    """
     When you delete a disposition object, automatically delete the corresponding user
    :param sender: the model, that sends the signal
    :param instance: the instance of the model, that triggers this
    """
    # TODO: Implement Soft Delete for UserModel
    try:
        user = instance.user
        user.delete()
    except Exception as ex:
        print(str(ex))
        pass

post_delete.connect(delete_user, sender=CustomUser)
