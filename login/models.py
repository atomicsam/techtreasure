from django.db import models
from django.utils.text import slugify


# 商品发布表
class Merchandise(models.Model):
    title = models.CharField(max_length=30)  # 物品标题
    describe = models.TextField()  # 物品描述
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 物品价格
    file_image = models.ImageField()  # 图片路径
    user_id = models.CharField(max_length=30,null=True)  # 用户id
    user_name = models.CharField(max_length=30,null=True)  # 用户名
    creation_time = models.DateTimeField(auto_now_add=True)  # 创建时间

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Merchandise, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Merchandise'

    def __str__(self):
        return self.title


# 购买历史表
class HistoryRecord(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 物品价格
    user_id = models.CharField(max_length=30,null=True)  # 发布用户id
    user_name = models.CharField(max_length=30,null=True)  # 发布用户名
    purchase_user_id = models.CharField(max_length=30,null=True)  # 购买用户id
    purchase_user_name = models.CharField(max_length=30,null=True)  # 购买用户名
    creation_time = models.DateTimeField(auto_now_add=True)  # 购买时间
    merchandise = models.ForeignKey(Merchandise, on_delete=models.CASCADE)  # 物品名称 id

    def save(self, *args, **kwargs):
        self.slug = slugify(self.merchandise.title)
        super(HistoryRecord, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'HistoryRecord'

    def __str__(self):
        return self.merchandise.file_image,self.price,self.merchandise.title
