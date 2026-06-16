from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.http import HttpResponse
import csv
from .models import Contract, Order, Product, CustomCase, Partner, Testimonial, Workshop, Craft, FAQ, Category, SiteConfig, Announcement, Banner, SeoConfig, ShopCategory


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ('基本信息', {'fields': ('company_name', 'phone', 'email', 'address')}),
        ('首页文案', {'fields': ('hero_title', 'hero_sub')}),
    )

    def has_add_permission(self, request): return not SiteConfig.objects.exists()
    def has_delete_permission(self, request, obj=None): return False




@admin.register(SeoConfig)
class SeoConfigAdmin(admin.ModelAdmin):
    fieldsets = (("首页", {"fields": ("home_title", "home_desc")}), ("产品页", {"fields": ("products_title", "products_desc")}), ("购买页", {"fields": ("shop_title", "shop_desc")}))
    def has_add_permission(self, request): return not SeoConfig.objects.exists()
    def has_delete_permission(self, request, obj=None): return False
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["text", "is_active", "sort"]
    list_editable = ["is_active", "sort"]
    fieldsets = (('公告内容', {'fields': ('text', 'link')}), ('状态', {'fields': ('sort', 'is_active')}))


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ["image_preview", "title", "is_active", "sort"]
    list_editable = ["is_active", "sort"]
    fieldsets = (('基本信息', {'fields': ('title', 'image', 'link')}), ('状态', {'fields': ('sort', 'is_active')}))

    @admin.display(description='图片')
    def image_preview(self, obj):
        if obj.image: return format_html('<img src="{}" style="width:80px;height:50px;object-fit:cover" />', obj.image.url)
        return '-'
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name', 'key', 'sort', 'is_active']
    list_editable = ['sort', 'is_active']

    @admin.display(description='图片')
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:50px;height:50px;object-fit:cover" />', obj.image.url)
        return format_html('<img src="http://localhost:5173/images/cat-{}.svg" style="width:50px;height:50px" />', obj.key)


@admin.register(ShopCategory)
class ShopCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'key', 'sort', 'is_active']
    list_editable = ['sort', 'is_active']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'sort', 'is_active']
    list_editable = ['sort', 'is_active']
    search_fields = ['question', 'answer']


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ['name', 'area', 'workers', 'is_active', 'sort']
    list_editable = ['sort', 'is_active']
    search_fields = ['name', 'equip']
    fieldsets = (('基本信息', {'fields': ('name', 'area', 'workers')}), ('设备清单', {'fields': ('equip',)}), ('状态', {'fields': ('sort', 'is_active')}))


@admin.register(Craft)
class CraftAdmin(admin.ModelAdmin):
    list_display = ['step', 'title', 'sort']
    list_editable = ['sort']
    search_fields = ['title', 'desc']
    fieldsets = (('步骤信息', {'fields': ('step', 'title')}), ('详细描述', {'fields': ('desc',)}), ('排序', {'fields': ('sort',)}))


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_editable = ['is_active']
    search_fields = ['name']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'is_active']
    list_editable = ['is_active']
    search_fields = ['name', 'role', 'text']


@admin.register(CustomCase)
class CustomCaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'case_type', 'area', 'style', 'is_active', 'created_at']
    list_filter = ['case_type', 'style', 'is_active']
    search_fields = ['name', 'desc']
    fieldsets = (
        ('基本信息', {'fields': ('name', 'case_type', 'area', 'style')}),
        ('描述', {'fields': ('desc',)}),
        ('状态', {'fields': ('is_active',)}),
    )


# 先注销默认 User，再用自定义 UserAdmin 重新注册
admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ['username', 'first_name', 'email', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'first_name', 'email']

    fieldsets = (
        ('基本信息', {'fields': ('username', 'first_name', 'last_name', 'email')}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('日期', {'fields': ('date_joined', 'last_login')}),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'code', 'name', 'category_name', 'price', 'is_active', 'tag', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'code']
    list_editable = ['is_active', 'tag']
    ordering = ['category__sort', 'code']

    @admin.display(description='图片')
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:40px;height:40px;object-fit:cover" />', obj.image.url)
        return '-'

    @admin.display(description='分类', ordering='category__sort')
    def category_name(self, obj):
        return obj.category.name if obj.category else '-'

    fieldsets = (
        ('基本信息', {'fields': ('code', 'name', 'category', 'shop_category', 'material', 'price')}),
        ('展示信息', {'fields': ('image', 'desc', 'size', 'details', 'tag')}),
        ('状态', {'fields': ('is_active',)}),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['contact_person', 'phone', 'item_count', 'city', 'total', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['contact_person', 'phone', 'address']
    readonly_fields = ['created_at', 'items_display']
    actions = ['mark_confirmed', 'mark_shipped', 'mark_delivered', 'export_csv']

    fieldsets = (
        ('客户信息', {'fields': ('contact_person', 'phone', 'address', 'note')}),
        ('订单信息', {'fields': ('items_display', 'total', 'status')}),
        ('系统信息', {'fields': ('created_at',)}),
    )

    @admin.display(description='购买件数')
    def item_count(self, obj):
        import json
        try:
            items = json.loads(obj.items)
            return sum(i.get('quantity', 0) for i in items)
        except: return '-'

    @admin.display(description='城市')
    def city(self, obj):
        return obj.address.split(' ')[0] if obj.address else '-'

    @admin.display(description='购买明细')
    def items_display(self, obj):
        import json
        try:
            items = json.loads(obj.items)
            rows = ['<table style="width:100%;border-collapse:collapse">',
                    '<tr style="background:#fafaf8"><th style="padding:6px 10px;text-align:left">商品</th><th style="padding:6px 10px">数量</th><th style="padding:6px 10px;text-align:right">单价</th></tr>']
            for i in items:
                rows.append(f'<tr><td style="padding:4px 10px">{i["name"]}</td><td style="padding:4px 10px;text-align:center">×{i["quantity"]}</td><td style="padding:4px 10px;text-align:right">¥{i["price"]:,}</td></tr>')
            rows.append('</table>')
            return format_html(''.join(rows))
        except: return obj.items

    def mark_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_confirmed.short_description = '标记为已确认'

    def mark_shipped(self, request, queryset):
        queryset.update(status='shipped')
    mark_shipped.short_description = '标记为已发货'

    def mark_delivered(self, request, queryset):
        queryset.update(status='delivered')
    mark_delivered.short_description = '标记为已签收'

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="orders.csv"'
        writer = csv.writer(response)
        writer.writerow(['编号', '收货人', '电话', '金额', '状态', '时间', '城市', '件数', '购买明细'])
        for o in queryset:
            import json
            items = json.loads(o.items) if o.items else []
            detail = '；'.join(f"{i['name']}×{i['quantity']}" for i in items)
            writer.writerow([o.id, o.contact_person, o.phone, o.total, o.get_status_display(),
                           o.created_at.strftime('%Y-%m-%d %H:%M'),
                           o.address.split(' ')[0] if o.address else '-',
                           sum(i.get('quantity',0) for i in items),
                           detail])
        return response
    export_csv.short_description = '导出 CSV'


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['contact_person', 'phone', 'company', 'project_type', 'city', 'status', 'created_at']
    list_filter = ['project_type', 'status', 'budget', 'city', 'created_at']
    search_fields = ['contact_person', 'phone', 'company', 'description']
    readonly_fields = ['created_at']

    fieldsets = (
        ('基本信息', {'fields': ('contact_person', 'phone', 'company')}),
        ('项目信息', {'fields': ('project_type', 'quantity', 'city', 'budget')}),
        ('详细需求', {'fields': ('description',)}),
        ('跟进状态', {'fields': ('status',)}),
        ('系统信息', {'fields': ('created_at',)}),
    )
