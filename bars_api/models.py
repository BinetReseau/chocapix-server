from django.db import models


class Bar(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.id

class User(models.Model):
    name = models.CharField(max_length=50)
    login = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Account(models.Model):
    bar = models.ForeignKey(Bar)
    owner = models.ForeignKey(User)
    money = models.DecimalField(max_digits=7, decimal_places=3)

    def __unicode__(self):
        return self.owner.name + " ("+self.bar.id+")"
