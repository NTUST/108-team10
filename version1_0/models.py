from django.db import models as m

# Create your models here.


class Shop(m.Model):
    ShopId = m.TextField(primary_key=True, default='',
                         max_length=1, null=False)
    name = m.TextField(null=False)
    info = m.TextField(null=True, default='none')
    logoPath = m.TextField(null=True, default='none')
    imagePath = m.TextField(null=True, default='none')
    remark = m.TextField(null=True, default='none')

    def __str__(self):
        return(self.name)


class Category(m.Model):
    CategoryId = m.TextField(
        primary_key=True, default='', max_length=2, null=False)
    name = m.TextField(default='', null=False)

    def __str__(self):
        return(self.name)


class Beverage(m.Model):
    BeverageId = m.TextField(
        primary_key=True, default='NNN', max_length=3, null=False)
    Shop = m.ForeignKey(Shop, default='X',
                        on_delete=m.CASCADE, related_name='beverages')
    Category = m.ForeignKey(Category, default='CX',
                            on_delete=m.SET_DEFAULT, related_name='products')
    name = m.TextField(default='', null=False)
    info = m.TextField(null=True, default='none')
    imagePath = m.TextField(null=True, default='none')
    hasCold = m.BooleanField(null=False, default=True)
    hasHot = m.BooleanField(null=False, default=False)
    remark = m.TextField(null=True, default='none')

    def save(self, *args, **kwargs):
        if self.BeverageId == 'NNN':
            s = len(self.__class__.objects.filter(Shop=self.Shop))+1
            self.BeverageId = self.Shop.ShopId + format(s, '02')
        super(self.__class__, self).save(*args, **kwargs)

    def __str__(self):
        return(''.join([self.Shop.name, '/', self.name]))


class BeverageCapacity(m.Model):
    Number = m.IntegerField(primary_key=True, default=0, null=False)
    BeverageId = m.ForeignKey(
        Beverage, default='XXX', null=False, on_delete=m.CASCADE, related_name='capacitys')
    capacity = m.TextField(default='M', max_length=2, null=False)
    price = m.IntegerField(default=0, null=False)
    calories = m.IntegerField(default=0, null=False)

    def __str__(self):
        sn = self.BeverageId.Shop.name
        bn = self.BeverageId.name
        return(''.join([sn, '/', bn, '-', self.capacity]))

    def save(self, *args, **kwargs):
        if self.Number == 0:
            s = len(self.__class__.objects.all())+1
            self.Number = s
        super(self.__class__, self).save(*args, **kwargs)


class TeamMember(m.Model):
    StudentId = m.TextField(
        primary_key=True, default='B00000000', max_length=9, null=False)
    name = m.TextField(null=False, default='none')
    introduction = m.TextField(null=False, default='none')
    photoPath = m.TextField(null=True, default='none')
    job = m.TextField(null=False, default='none')

    def __str__(self):
        return(''.join([self.name]))
