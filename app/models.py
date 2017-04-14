from django.db import models

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models, router
from django.db.models.deletion import Collector

class BaseModel(models.Model):
    """
        Parent model
        :model:`paymyrent.BaseModel`
    """
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def can_delete(self):
        """
            Selects which fields of the base model can be deleted
        """
        if self._get_pk_val():
            seen_objs = Collector(router.db_for_write(self.__class__, instance=self))
            seen_objs.collect([self])
            if len(seen_objs.data) > 1:
                raise ValidationError("Sorry, cannot be deleted.")

    def delete(self, **kwargs):
        """
            Deletes fields from base model
        """
        assert self._get_pk_val() is not None, "Object %s cannot be deleted because %s is null." % (
            self._meta.object_name, self._meta.pk.attname)
        seen_objs = Collector(router.db_for_write(self.__class__, instance=self))
        seen_objs.collect([self])
        self.can_delete()
        seen_objs.delete()

    def save(self, **kwargs):
        """
            Saves fields
        """
        models.Model.save(self)

    class Meta:
        abstract = True

class Genders(BaseModel):
    """
        Model that identifies the user's gender
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Gender'
        verbose_name_plural = 'Genders'
        db_table = 'genders'
        unique_together = ('name',)


class UsersGroup(BaseModel):
    """
        Determines the type of user:
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Users Group'
        verbose_name_plural = 'Users Group'
        db_table = 'users_group'
        unique_together = ('name',)

    def get_amount_users(self):
        return self.users_set.count()


class Users(BaseModel):
    """
        Model used to define a user according to the following fields:
    """
    user = models.OneToOneField(User)
    group = models.ForeignKey(UsersGroup, blank=True, null=True)
    gender = models.ForeignKey(Genders, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    birth_year = models.IntegerField(default=0, blank=True, null=True)
    birth_day = models.DateField(blank=True, null=True)
    avatar = models.FileField(upload_to='images/', max_length=100, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.user)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'
        unique_together = ('user',)

