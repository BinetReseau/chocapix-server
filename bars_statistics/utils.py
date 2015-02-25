from django.conf import settings

import redis

def get_redis():
	pool = redis.ConnectionPool(host=settings.REDIS['host'],
									port=settings.REDIS['port'],
									db=settings.REDIS['db'])
	r = redis.Redis(connection_pool=pool)

	return r

redis_keys = {
	'USER_RANKINGS' : 'users_ranking_%s',
}