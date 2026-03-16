import redis
from django.db import connection
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    health = {
        'status': 'healthy',
        'database': 'ok',
        'redis': 'ok',
    }

    try:
        connection.ensure_connection()
    except Exception:
        health['database'] = 'error'
        health['status'] = 'unhealthy'

    try:
        r = redis.from_url(settings.REDIS_URL)
        r.ping()
    except Exception:
        health['redis'] = 'error'
        health['status'] = 'unhealthy'

    status_code = 200 if health['status'] == 'healthy' else 503
    return Response(health, status=status_code)