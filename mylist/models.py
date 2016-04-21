from django.db import models

# Create your models here.

class Checklist(models.Model):
   
    #one list can have multiple items
    
    list_name = models.CharField(max_length=30)
    list_code = models.CharField(max_length=30)
    list_mkr = models.ForeignKey('auth.User')
    #can have one maker

    def __str__(self):
        return u'%s %s %s' %(self.list_name , self.list_code , self.list_mkr) #can remove some
        
class Sublist(models.Model):
    sub_list = models.ManyToManyField('Checklist', related_name='chklists')
    #multiple users can subscribe to one checklist & multiple checklists can belong to one user
    sub_user = models.ForeignKey('auth.User')
    #many to one relationship - ie. many subscribed lists can belong to one user
 

    def __str__(self):
        return u'%s' %( self.sub_user)
    
class Item(models.Model):
    item = models.CharField(max_length=40)
    comment = models.CharField(max_length=140)
    qty = models.IntegerField(default=1)
    shop = models.CharField(max_length=40)
    shoplist = models.ForeignKey('mylist.Checklist', related_name= 'items', null=True)
    #each item can only be on one Checklist
    #purchased = models.IntegerField(default=0)
    action = models.CharField(max_length=10, default='buy')
    #action can be buy,bought,saved,deleted
    

    def __str__(self):
        return self.item

    def purchased(self):
        self.action = "bought"
        self.save()
        
    def need_to_buy(self):
        self.purchased = "buy"
        self.save()
        
    def save_item(self):
        self.purchased = "saved"
        self.save()
        
