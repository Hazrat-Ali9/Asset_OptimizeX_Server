from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

#  Custom User Manager
class UserManager(BaseUserManager):
  def create_user(self, email, name, phone_number,  password=None, password2=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')
      
      user = self.model(
          email=self.normalize_email(email),
          name=name,
          phone_number = phone_number,
         
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, name, phone_number,  password=None ):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      user = self.create_user(
          email,
          password=password,
          name=name,
          phone_number=phone_number,
         
      )
      user.is_admin = True
      user.is_staff = True
      user.is_superuser = True
      user.save(using = self._db)
      return user

#  Custom User Model
class User(AbstractBaseUser):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  name = models.CharField(max_length=200)
  phone_number = models.CharField(max_length=50, unique=True )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  image = models.ImageField(upload_to = 'images/account/', null=False, blank = False, default='profile_pics/profile.jpg')
  bio = models.CharField(max_length=50,blank=False, null=False, default=False) 
  
 
  country = models.CharField(max_length=100, default=False, null=False, blank=False)
  zip_code = models.CharField(max_length=100, default=False, null=False)

  is_admin = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_superadmin = models.BooleanField(default=False)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name',  'phone_number']
  
  objects = UserManager()
  
  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

