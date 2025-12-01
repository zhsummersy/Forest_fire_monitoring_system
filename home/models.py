from django.db import models


# Create your models here.
class Contact(models.Model):
    sn0 = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=100)
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'Message from ' + self.name 

# Create your models here.

class Category(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()

	def __str__(self):
		return self.title

class Image(models.Model):
	title=models.CharField(max_length=200)
	description=models.TextField()
	image=models.ImageField(upload_to='homeimages')
	added_date=models.DateTimeField()
	cat=models.ForeignKey(Category, on_delete=models.CASCADE)

	def __str__(self):
		return self.title
	
	

			

