from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from registration.signals import user_registered

# Create your models here.

class UsersManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email = UsersManager.normalize_email(email),
            date_of_birth = date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        user = self.create_user(
            email = email,
            password = password,
            date_of_birth = date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class UsersModelAuth(models.Model):
    """
    Use this for model authentication
    """
    email = models.EmailField(db_index=True, null=False)
    username = models.CharField(max_length=128, null=True)
    user_type = models.CharField(max_length=128, null=False)
    date_of_birth = models.DateField(null=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UsersManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'user_type', 'date_of_birth']

    def __unicode__(self):
        return self.user

    def get_full_name(self):
        return self.email
   
    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email 

    def get_username(self):
        return self.USERNAME_FIELD

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Users(AbstractBaseUser):
    """
    Users model
    """
    email = models.EmailField(unique=True, db_index=True, null=False)
    username = models.CharField(max_length=128, null=True)
    user_type = models.CharField(max_length=128, null=False)
    first_name = models.CharField(max_length=128, null=True)
    last_name = models.CharField(max_length=128, null=True)
    date_of_birth = models.DateField(null=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    # By default, user is active as soon as he reigsters 
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UsersManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'date_of_birth']


    def get_full_name(self):
        return self.username
   
    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    def get_username(self):
        return self.USERNAME_FIELD

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

def user_registered_callback(sender, request, **kwargs):
    user = Users(email=request.POST['email'])
    user.user_type = request.POST["user_type"]
    # Already saved
    #user.save()
 
user_registered.connect(user_registered_callback)

class Articles(models.Model):
    """
    Article model
    """
    author = models.ForeignKey(Users, related_name='Users', null=True)
    title = models.TextField(null=True)
    content = models.TextField(null=True)
    num_like = models.IntegerField(null=True, default=0)
    num_read = models.IntegerField(null=True, default=0)
    num_frwd = models.IntegerField(null=True, default=0)
    num_para = models.IntegerField(null=True, default=0)

def update_filename(instance, filename):
    return 'static/uploads/%s' % '{0}/{1}'.format(instance.user, filename)

class UploadFile(models.Model):
    """
    File upload model
    """
    user = models.CharField(max_length=128, null=True)
    file_uploaded = models.FileField(upload_to=update_filename)

## Library articles
#class Category(models.Model):
#    name = models.CharField(max_length=30)
#    description = models.CharField(max_length=200, default="")
#    code = models.IntegerField(null=True, blank=True)
#    parent = models.ForeignKey("Category", null=True, blank=True)
#    added = models.DateTimeField('date added',null=True,auto_now_add=True)
#
#    def __str__(self):
#        return self.name.encode('utf-8').strip()
#
#class Article(models.Model):
#    category = models.ForeignKey(Category)
#    title = models.CharField(max_length=120)
#    author = models.CharField(max_length=30)
#    body = models.TextField('Content')
#    added = models.DateTimeField('date added',null=True,auto_now_add=True)
#                                                                                                        
#    def __str__(self):
#        return '%s: %s' % (self.author.encode('utf-8').strip(), 
#                           self.title.encode('utf-8').strip())
