from django.db import models


class Category(models.Model):
    """产品分类"""
    name = models.CharField('分类名称', max_length=50, unique=True)
    key = models.CharField('英文标识', max_length=30, unique=True)
    sort = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('启用', default=True)

    class Meta:
        db_table = 'categories'
        verbose_name = verbose_name_plural = '产品分类'
        ordering = ['sort']

    def __str__(self): return self.name


class Product(models.Model):
    """成品商品"""
    code = models.CharField('型号', max_length=20, unique=True)
    name = models.CharField('名称', max_length=100)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.SET_NULL, null=True, blank=True)
    material = models.CharField('材质', max_length=200, blank=True, default='')
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    desc = models.CharField('描述', max_length=200, blank=True, default='')
    size = models.CharField('尺寸', max_length=100, blank=True, default='')
    details = models.TextField('详细特性', blank=True, default='', help_text='每行一个特性')
    image = models.ImageField('产品图片', upload_to='products/', blank=True)
    tag = models.CharField('标签', max_length=20, blank=True, default='', help_text='如：热卖、新品')
    is_active = models.BooleanField('上架', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'products'
        verbose_name = '成品商品'
        verbose_name_plural = '成品商品'
        ordering = ['category', 'code']

    def __str__(self):
        return f'{self.code} {self.name}'


class Order(models.Model):
    """成品购买订单"""
    contact_person = models.CharField('收货人', max_length=50)
    phone = models.CharField('联系电话', max_length=20)
    address = models.CharField('收货地址', max_length=200)
    note = models.TextField('备注', blank=True, default='')
    items = models.TextField('购买明细', help_text='JSON 格式存储')
    total = models.DecimalField('订单总额', max_digits=12, decimal_places=2)
    status = models.CharField('状态', max_length=20, default='new', choices=[
        ('new', '新订单'), ('confirmed', '已确认'), ('shipped', '已发货'),
        ('delivered', '已签收'), ('cancelled', '已取消'),
    ])
    created_at = models.DateTimeField('下单时间', auto_now_add=True)

    class Meta:
        db_table = 'orders'
        verbose_name = '成品订单'
        verbose_name_plural = '成品订单'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.contact_person} - {self.total}元'


class Partner(models.Model):
    """合作品牌"""
    name = models.CharField('品牌名称', max_length=100)
    is_active = models.BooleanField('展示', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'partners'
        verbose_name = '合作品牌'
        verbose_name_plural = '合作品牌'

    def __str__(self): return self.name


class Testimonial(models.Model):
    """客户评价"""
    name = models.CharField('客户名称', max_length=50)
    role = models.CharField('身份', max_length=100)
    text = models.TextField('评价内容')
    is_active = models.BooleanField('展示', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'testimonials'
        verbose_name = '客户评价'
        verbose_name_plural = '客户评价'

    def __str__(self): return f'{self.name} - {self.role}'


class Workshop(models.Model):
    """工厂车间"""
    name = models.CharField('车间名称', max_length=50)
    area = models.CharField('面积', max_length=30)
    workers = models.IntegerField('工人数', default=0)
    equip = models.TextField('设备清单')
    sort = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('展示', default=True)
    class Meta:
        db_table = 'workshops'; verbose_name = verbose_name_plural = '工厂车间'; ordering = ['sort']
    def __str__(self): return self.name


class Craft(models.Model):
    """工艺流程"""
    step = models.CharField('步骤编号', max_length=5)
    title = models.CharField('步骤名称', max_length=50)
    desc = models.TextField('详细描述')
    sort = models.IntegerField('排序', default=0)
    class Meta:
        db_table = 'crafts'; verbose_name = verbose_name_plural = '工艺流程'; ordering = ['sort']
    def __str__(self): return f'{self.step} {self.title}'


class FAQ(models.Model):
    """常见问题"""
    question = models.CharField('问题', max_length=200)
    answer = models.TextField('答案')
    sort = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('展示', default=True)
    class Meta:
        db_table = 'faqs'; verbose_name = verbose_name_plural = '常见问题'; ordering = ['sort']
    def __str__(self): return self.question


class SiteConfig(models.Model):
    """站点配置（单例）"""
    company_name = models.CharField('公司名称', max_length=100, default='尚品工坊')
    phone = models.CharField('联系电话', max_length=30, default='400-888-6688')
    email = models.CharField('联系邮箱', max_length=50, default='info@shangpin.com')
    address = models.CharField('公司地址', max_length=200, default='广东省佛山市顺德区龙江镇工业大道188号')
    hero_title = models.CharField('首页主标题', max_length=100, default='以工艺之名\n定义家居美学')
    hero_sub = models.CharField('首页副标题', max_length=200, blank=True, default='二十三年专注高端家具制造\n从原木到成品，每一件都是对品质的承诺')

    class Meta:
        verbose_name = verbose_name_plural = '站点配置'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self): return '站点配置'



class Announcement(models.Model):
    text = models.CharField(max_length=200)
    link = models.CharField(max_length=200, blank=True, default="")
    is_active = models.BooleanField(default=True)
    sort = models.IntegerField(default=0)
    class Meta:
        db_table = "announcements"; verbose_name = verbose_name_plural = "网站公告"; ordering = ["sort"]
    def __str__(self): return self.text[:30]


class Banner(models.Model):
    title = models.CharField(max_length=100, blank=True, default="")
    image = models.ImageField(upload_to="banners/")
    link = models.CharField(max_length=200, blank=True, default="")
    sort = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = "banners"; verbose_name = verbose_name_plural = "首页轮播"; ordering = ["sort"]
    def __str__(self): return self.title or f"Banner{self.id}"

class SeoConfig(models.Model):
    home_title = models.CharField(max_length=100, default="")
    home_desc = models.TextField(blank=True, default="")
    products_title = models.CharField(max_length=100, default="")
    products_desc = models.TextField(blank=True, default="")
    shop_title = models.CharField(max_length=100, default="")
    shop_desc = models.TextField(blank=True, default="")
    class Meta:
        db_table = "seo_config"; verbose_name = verbose_name_plural = "SEO 配置"
    def save(self, *args, **kwargs): self.pk = 1; super().save(*args, **kwargs)
    @classmethod
    def load(cls): obj, _ = cls.objects.get_or_create(pk=1); return obj
    def __str__(self): return "SEO 配置"
class Contract(models.Model):
    """联系表单 - 客户咨询记录"""

    PROJECT_TYPES = [
        ('', '请选择项目类型'),
        ('full_house', '全屋定制'),
        ('hotel', '酒店工程'),
        ('showroom', '样板间/售楼处'),
        ('office', '办公空间'),
        ('restaurant', '餐饮门店'),
        ('club', '会所/别墅'),
        ('single', '单件定制'),
        ('other', '其他'),
    ]

    QUANTITIES = [
        ('', '请选择预计数量'),
        ('1-10', '1-10件'),
        ('10-50', '10-50件'),
        ('50-100', '50-100件'),
        ('100-500', '100-500件'),
        ('500+', '500件以上'),
    ]

    BUDGETS = [
        ('', '请选择预算区间'),
        ('under_50k', '5万以下'),
        ('50k_100k', '5-10万'),
        ('100k_300k', '10-30万'),
        ('300k_500k', '30-50万'),
        ('500k_1m', '50-100万'),
        ('1m_3m', '100-300万'),
        ('over_3m', '300万以上'),
    ]

    contact_person = models.CharField('联系人', max_length=50)
    phone = models.CharField('联系电话', max_length=20)
    company = models.CharField('公司/品牌', max_length=100, blank=True, default='')
    project_type = models.CharField('项目类型', max_length=30, choices=PROJECT_TYPES, blank=True, default='')
    quantity = models.CharField('预计数量', max_length=20, choices=QUANTITIES, blank=True, default='')
    city = models.CharField('交付城市', max_length=50, blank=True, default='')
    budget = models.CharField('预算区间', max_length=20, choices=BUDGETS, blank=True, default='')
    description = models.TextField('需求说明', blank=True, default='')
    status = models.CharField('状态', max_length=20, default='new', choices=[
        ('new', '新提交'),
        ('contacted', '已联系'),
        ('negotiating', '洽谈中'),
        ('confirmed', '已确认'),
        ('closed', '已关闭'),
    ])
    created_at = models.DateTimeField('提交时间', auto_now_add=True)

    class Meta:
        db_table = 'contract'
        verbose_name = '客户咨询'
        verbose_name_plural = '客户咨询'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.contact_person} - {self.phone}'


class CustomCase(models.Model):
    """定制案例"""
    name = models.CharField('项目名称', max_length=100)
    case_type = models.CharField('项目类型', max_length=30, choices=[
        ('full_house', '全屋定制'), ('club', '会所家具'), ('villa', '别墅定制'),
        ('hotel', '酒店工程'), ('office', '办公定制'), ('garden', '庭院家具'),
    ])
    area = models.CharField('面积', max_length=30)
    style = models.CharField('风格', max_length=30)
    desc = models.TextField('描述')
    is_active = models.BooleanField('展示', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'custom_cases'
        verbose_name = '定制案例'
        verbose_name_plural = '定制案例'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
