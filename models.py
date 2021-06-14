from django.db import models

#user_login,user_details,expert_details,crop_type,crop_master,crop_pics,crop_variety,fertilizer_master,
#pesticides_master,disease_master,cultivation_details,cultivation_pics,ask_expert,feedback

# Create your models here.
class user_login(models.Model):
    uname = models.CharField(max_length=100)
    passwd = models.CharField(max_length=25)
    u_type = models.CharField(max_length=10)

    def __str__(self):
        return self.uname

class user_details(models.Model):
    user_id = models.IntegerField()
    kcno = models.IntegerField()
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=200)
    gender = models.CharField(max_length=25)
    age = models.IntegerField()
    addr = models.CharField(max_length=500)
    pin  = models.CharField(max_length=25)
    contact  = models.CharField(max_length=25)
    email = models.CharField(max_length=250)
    status  = models.CharField(max_length=25)
    def __str__(self):
        return self.fname

class expert_details(models.Model):
    user_id = models.IntegerField()
    fname  = models.CharField(max_length=50)
    lname  = models.CharField(max_length=50)
    contact  = models.CharField(max_length=25)
    email  = models.CharField(max_length=250)
    status  = models.CharField(max_length=25)

class crop_type(models.Model):
    type_name  = models.CharField(max_length=25)

class crop_master(models.Model):
    crop_type_id = models.IntegerField()
    crop_name = models.CharField(max_length=50)
    crop_sname = models.CharField(max_length=50)
    crop_descp = models.CharField(max_length=500)
    crop_area = models.CharField(max_length=500)

class crop_pics(models.Model):
    crop_id = models.IntegerField()
    pic_path = models.CharField(max_length=250)

class crop_variety(models.Model):
    crop_id = models.IntegerField()
    variety_name = models.CharField(max_length=50)
    variety_sname = models.CharField(max_length=50)
    crop_descp = models.CharField(max_length=500)
    crop_area = models.CharField(max_length=250)
    pic_path = models.CharField(max_length=250)


class fertilizer_master(models.Model):
    crop_id = models.IntegerField()
    f_type = models.CharField(max_length=25)
    f_name = models.CharField(max_length=50)
    descp = models.CharField(max_length=250)
    image = models.CharField(max_length=25)
    application = models.CharField(max_length=500)


class pesticides_master(models.Model):
    crop_id = models.IntegerField()
    pt_type = models.CharField(max_length=25)
    product_name = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    image = models.CharField(max_length=25)
    descp = models.CharField(max_length=250)
    application = models.CharField(max_length=500)


class disease_master(models.Model):
    crop_id = models.IntegerField()
    name = models.CharField(max_length=50)
    descrp= models.CharField(max_length=250)
    pic_path = models.CharField(max_length=250)

class cultivation_details(models.Model):
    crop_id = models.IntegerField()
    land_type = models.CharField(max_length=500)
    soil_concentration = models.CharField(max_length=500)
    descp = models.CharField(max_length=50)
    pic_path = models.CharField(max_length=50)

#class cultivation_pics(models.Model):
#    cultivation_id = models.IntegerField()
#    pic_path = models.CharField(max_length=50)


class ask_expert(models.Model):
    expert_id = models.IntegerField()
    user_id = models.IntegerField()
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=500)
    dt = models.CharField(max_length=50)
    tm = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

class feedback(models.Model):
    user_id = models.IntegerField()
    descp = models.CharField(max_length=500)
    dt = models.CharField(max_length=50)
    tm = models.CharField(max_length=50)



class seller_details(models.Model):
    user_id = models.IntegerField()
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=200)
    addr = models.CharField(max_length=500)
    pin  = models.CharField(max_length=25)
    contact  = models.CharField(max_length=25)
    email = models.CharField(max_length=250)
    status  = models.CharField(max_length=25)

class product_details(models.Model):
    user_id = models.IntegerField()
    p_name = models.CharField(max_length=50)
    descp = models.CharField(max_length=250)
    price = models.CharField(max_length=25)
    image = models.CharField(max_length=25)

class user_transaction(models.Model):
    product_id = models.IntegerField()
    user_id = models.IntegerField()
    amt = models.FloatField()
    addr = models.CharField(max_length=100)
    status = models.CharField(max_length=25)
   # card_no  = models.CharField(max_length=25)
    #cvv  = models.CharField(max_length=25)
    #expiry  = models.CharField(max_length=25)
    dt = models.CharField(max_length=25)
    tm = models.CharField(max_length=25)