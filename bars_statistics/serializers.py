from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework import exceptions

from utils import get_redis, redis_keys


class UsersRankingSerializer(serializers.BaseSerializer):
	def to_representation(self, bar):
		r = get_redis()

		return {
			'ranking': r.zrevrange(redis_keys['USER_RANKINGS'] % bar.id,0,-1)
		}
