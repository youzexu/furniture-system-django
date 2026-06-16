import json
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from .models import Contract, Order, Product, CustomCase, Partner, Testimonial, Workshop, Craft, FAQ, Category, SiteConfig, Announcement, Banner, SeoConfig, ShopCategory


@csrf_exempt
@require_POST
def submit_contract(request):
    """接收前端联系表单提交，写入 contract 表"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'JSON 格式错误'}, status=400)

    # 校验必填字段
    contact_person = data.get('contact_person', '').strip()
    phone = data.get('phone', '').strip()

    if not contact_person:
        return JsonResponse({'success': False, 'message': '请填写联系人'}, status=400)
    if not phone:
        return JsonResponse({'success': False, 'message': '请填写联系电话'}, status=400)

    try:
        contract = Contract.objects.create(
            contact_person=contact_person,
            phone=phone,
            company=data.get('company', '').strip(),
            project_type=data.get('project_type', ''),
            quantity=data.get('quantity', ''),
            city=data.get('city', '').strip(),
            budget=data.get('budget', ''),
            description=data.get('description', '').strip(),
        )
        return JsonResponse({
            'success': True,
            'message': '提交成功！我们将在一个工作日内与您联系。',
            'id': contract.id,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'提交失败：{str(e)}'}, status=500)


@csrf_exempt
@require_POST
def submit_order(request):
    """接收前端成品购买订单"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'JSON 格式错误'}, status=400)

    contact_person = data.get('contact_person', '').strip()
    phone = data.get('phone', '').strip()
    address = data.get('address', '').strip()

    if not contact_person or not phone or not address:
        return JsonResponse({'success': False, 'message': '请填写收货人、电话和地址'}, status=400)

    try:
        order = Order.objects.create(
            contact_person=contact_person,
            phone=phone,
            address=address,
            note=data.get('note', ''),
            items=json.dumps(data.get('items', []), ensure_ascii=False),
            total=data.get('total', 0),
        )
        return JsonResponse({
            'success': True,
            'message': '下单成功！我们将尽快与您确认订单。',
            'id': order.id,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'提交失败：{str(e)}'}, status=500)


@require_GET
def get_categories(request):
    qs = Category.objects.filter(is_active=True).order_by('sort')
    return JsonResponse({'success': True, 'data': [{'key': c.key, 'name': c.name, 'desc': c.desc, 'image': c.image.url if c.image else ''} for c in qs]})


@require_GET
def get_shop_categories(request):
    qs = ShopCategory.objects.filter(is_active=True).order_by('sort')
    return JsonResponse({'success': True, 'data': [{'key': c.key, 'name': c.name} for c in qs]})


@require_GET
def get_products(request):
    """返回成品商品数据给前端"""
    qs = Product.objects.filter(is_active=True).select_related("category", "shop_category").order_by('category__sort', 'code')
    cat = request.GET.get('cat', '')
    search = request.GET.get('search', '')
    if cat and cat != 'all':
        qs = qs.filter(category=cat)
    shop_cat = request.GET.get("shop_cat", "")
    if shop_cat and shop_cat != "all":
        qs = qs.filter(shop_category__key=shop_cat)
    if search:
        query = Q()
        for ch in search:
            if ch.strip():
                query |= Q(name__icontains=ch) | Q(material__icontains=ch) | Q(desc__icontains=ch)
        qs = qs.filter(query)

    data = [{
        'code': p.code, 'name': p.name, 'cat': p.category.key if p.category else '',
        'shop_cat': p.shop_category.key if p.shop_category else '',
        'shop_catName': p.shop_category.name if p.shop_category else '',
        'catName': p.category.name if p.category else '',
        'material': p.material, 'price': f'¥{int(p.price):,}',
        'priceNum': int(p.price), 'desc': p.desc, 'tag': p.tag,
        'image': p.image.url if p.image else '',
        'size': p.size,
        'details': json.loads(p.details) if p.details else [],
    } for p in qs]
    return JsonResponse({'success': True, 'data': data})


@require_GET
def get_cases(request):
    """返回定制案例数据给前端"""
    qs = CustomCase.objects.filter(is_active=True).order_by('-created_at')
    data = [{
        'name': c.name, 'type': c.get_case_type_display(), 'area': c.area,
        'style': c.style, 'desc': c.desc,
    } for c in qs]
    return JsonResponse({'success': True, 'data': data})


@require_GET
def get_partners(request):
    qs = Partner.objects.filter(is_active=True)
    return JsonResponse({'success': True, 'data': [p.name for p in qs]})


@require_GET
def get_testimonials(request):
    qs = Testimonial.objects.filter(is_active=True)
    return JsonResponse({'success': True, 'data': [{'name': t.name, 'role': t.role, 'text': t.text} for t in qs]})


@csrf_exempt
def delete_order(request, order_id):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return JsonResponse({'success': False, 'message': '未登录'}, status=401)
    from rest_framework_simplejwt.tokens import AccessToken
    try:
        AccessToken(auth_header[7:])
        order = Order.objects.get(id=order_id)
        if order.status != 'delivered':
            return JsonResponse({'success': False, 'message': '仅已签收订单可删除'}, status=400)
        order.delete()
        return JsonResponse({'success': True, 'message': '订单已删除'})
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'message': '订单不存在'}, status=404)
    except Exception:
        return JsonResponse({'success': False, 'message': 'token 无效'}, status=401)


@require_GET
def get_workshops(request):
    qs = Workshop.objects.filter(is_active=True)
    return JsonResponse({'success': True, 'data': [{'name': w.name, 'area': w.area, 'workers': w.workers, 'equip': w.equip} for w in qs]})


@require_GET
def get_crafts(request):
    qs = Craft.objects.all()
    return JsonResponse({'success': True, 'data': [{'step': c.step, 'title': c.title, 'desc': c.desc} for c in qs]})


@require_GET
def get_certs(request):
    return JsonResponse({'success': True, 'data': [
        'ISO 9001:2015', 'ISO 14001:2015', 'FSC 森林认证', 'SGS 产品检测',
        '欧盟 E1 环保', '美国 CARB 认证', 'OHSAS 18001', '中国环保标志'
    ]})



@require_GET
def get_announcements(request):
    qs = Announcement.objects.filter(is_active=True).order_by("sort")
    return JsonResponse({"success": True, "data": [{"text": a.text, "link": a.link} for a in qs]})


@require_GET
def get_banners(request):
    qs = Banner.objects.filter(is_active=True).order_by("sort")
    return JsonResponse({"success": True, "data": [{"title": b.title, "image": b.image.url if b.image else "", "link": b.link} for b in qs]})

@require_GET
def get_seo_config(request):
    cfg = SeoConfig.load()
    return JsonResponse({"success": True, "data": {
        "home_title": cfg.home_title, "home_desc": cfg.home_desc,
        "products_title": cfg.products_title, "products_desc": cfg.products_desc,
        "shop_title": cfg.shop_title, "shop_desc": cfg.shop_desc,
    }})
    return JsonResponse({"success": True, "data": [{"title": b.title, "image": b.image.url if b.image else "", "link": b.link} for b in qs]})
@require_GET
def get_site_config(request):
    cfg = SiteConfig.load()
    return JsonResponse({'success': True, 'data': {
        'company_name': cfg.company_name, 'phone': cfg.phone, 'email': cfg.email,
        'address': cfg.address, 'hero_title': cfg.hero_title, 'hero_sub': cfg.hero_sub,
    }})


@require_GET
def get_faqs(request):
    qs = FAQ.objects.filter(is_active=True)
    return JsonResponse({'success': True, 'data': [{'q': f.question, 'a': f.answer} for f in qs]})


@csrf_exempt
def my_orders(request):
    """返回当前登录用户的订单列表"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return JsonResponse({'success': False, 'message': '请先登录'}, status=401)

    from rest_framework_simplejwt.tokens import AccessToken
    try:
        token = AccessToken(auth_header[7:])
        user_id = token['user_id']
        orders = Order.objects.all().order_by('-created_at')
        data = []
        for o in orders:
            try:
                items = json.loads(o.items)
            except:
                items = []
            data.append({
                'id': o.id, 'total': float(o.total), 'status': o.get_status_display(),
                'created_at': o.created_at.strftime('%Y-%m-%d %H:%M'),
                'items': items, 'address': o.address, 'note': o.note,
            })
        return JsonResponse({'success': True, 'data': data})
    except Exception:
        return JsonResponse({'success': False, 'message': 'token 无效'}, status=401)
