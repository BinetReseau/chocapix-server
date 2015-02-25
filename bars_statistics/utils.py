from django.conf import settings

import redis

def get_redis():
	pool = redis.ConnectionPool(host=settings.REDIS['host'],
									port=settings.REDIS['port'],
									db=settings.REDIS['db'])
	r = redis.Redis(connection_pool=pool)

	return r

redis_keys = {
	'USERS_RANKING' : 'users_ranking_%s',
	'ITEMS_RANKING' : 'items_ranking_%s'
}