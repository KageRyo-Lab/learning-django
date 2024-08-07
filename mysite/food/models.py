from django.db import models
from django.forms import ValidationError
from django_resized import ResizedImageField

# 標籤
class Tag(models.Model):
    name = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name
    
# 付款方式（設備）
class Device(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
# 店家
class Place(models.Model):
    name = models.CharField(max_length=20, help_text='輸入商店名稱')
    address = models.CharField(max_length=50, null=True)
    pub_date = models.DateTimeField('上傳日期')
    phone_number = models.CharField(max_length=20, default="無")
    website = models.CharField(max_length=200, default="無")
    introduction = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, through='Tag_Management', through_fields=('place', 'tags'))
    devices = models.ManyToManyField(Device, through='Device_Management', through_fields=('place', 'devices'))

    def __str__(self):
        return self.name
    
# 限制照片上傳大小
def validateFileSize(value):
    fileSize = value.size
    if fileSize > 102400:
        raise ValidationError("The Maxium File Size That Can be Uploaded is 100KB!")
    else:
        return value

# 照片
class Photo(models.Model):
    name = models.CharField(max_length=255)
    file = ResizedImageField(size=[256, 256], crop=['middle', 'center'], force_format='PNG', upload_to='photos', validators=[validateFileSize])
    place = models.ForeignKey(Place, help_text='商店名稱', on_delete=models.SET_NULL, null=True)
    
# 標籤與店家關聯
class Tag_Management(models.Model):
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True)
    tags = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    
# 付款方式（設備）與店家關聯
class Device_Management(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    devices = models.ForeignKey(Device, on_delete=models.CASCADE)