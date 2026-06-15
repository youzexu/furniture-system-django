import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


@csrf_exempt
@require_POST
def register(request):
    """注册普通用户"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'JSON 格式错误'}, status=400)

    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    first_name = data.get('first_name', '').strip()
    email = data.get('email', '').strip()

    if not username or not password:
        return JsonResponse({'success': False, 'message': '用户名和密码不能为空'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'success': False, 'message': '用户名已存在'}, status=400)

    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            email=email,
            is_staff=False,
            is_active=True,
        )
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'success': True,
            'message': '注册成功',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'email': user.email,
            },
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'注册失败：{str(e)}'}, status=500)


@csrf_exempt
@require_POST
def login(request):
    """登录，返回 JWT token"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'JSON 格式错误'}, status=400)

    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return JsonResponse({'success': False, 'message': '用户名和密码不能为空'}, status=400)

    from django.contrib.auth import authenticate
    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({'success': False, 'message': '用户名或密码错误'}, status=401)

    if not user.is_active:
        return JsonResponse({'success': False, 'message': '账号已禁用'}, status=403)

    refresh = RefreshToken.for_user(user)
    return JsonResponse({
        'success': True,
        'message': '登录成功',
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'email': user.email,
            'is_staff': user.is_staff,
        },
    })


@csrf_exempt
@require_POST
def refresh_token(request):
    """刷新 access token"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'JSON 格式错误'}, status=400)

    refresh_str = data.get('refresh', '')
    if not refresh_str:
        return JsonResponse({'success': False, 'message': 'refresh token 不能为空'}, status=400)

    try:
        refresh = RefreshToken(refresh_str)
        return JsonResponse({
            'success': True,
            'access': str(refresh.access_token),
        })
    except Exception:
        return JsonResponse({'success': False, 'message': 'token 无效或已过期'}, status=401)


@csrf_exempt
def me(request):
    """获取当前登录用户信息"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return JsonResponse({'success': False, 'message': '未登录'}, status=401)

    token_str = auth_header[7:]
    from rest_framework_simplejwt.tokens import AccessToken
    from django.contrib.auth.models import User

    try:
        token = AccessToken(token_str)
        user_id = token['user_id']
        user = User.objects.get(id=user_id)
        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'email': user.email,
                'is_staff': user.is_staff,
            },
        })
    except Exception:
        return JsonResponse({'success': False, 'message': 'token 无效或已过期'}, status=401)


@csrf_exempt
def update_profile(request):
    """更新当前登录用户信息"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return JsonResponse({'success': False, 'message': '未登录'}, status=401)

    from rest_framework_simplejwt.tokens import AccessToken
    from django.contrib.auth.models import User

    try:
        token = AccessToken(auth_header[7:])
        user = User.objects.get(id=token['user_id'])
    except Exception:
        return JsonResponse({'success': False, 'message': 'token 无效'}, status=401)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'JSON 格式错误'}, status=400)

    first_name = data.get('first_name', '').strip()
    email = data.get('email', '').strip()

    user.first_name = first_name
    user.email = email
    user.save()

    return JsonResponse({
        'success': True,
        'message': '修改成功',
        'user': {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'email': user.email,
            'is_staff': user.is_staff,
        },
    })
