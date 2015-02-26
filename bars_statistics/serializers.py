from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework import exceptions

from utils import get_redis, redis_keys


class UsersRankingSerializer(serializers.BaseSerializer):
	def to_representation(self, bar):
		r = get_redis()

		return {
			'ranking': r.zrevrange(redis_keys['USERS_RANKING'] % bar.id, 0, -1, withscores=True)
		}


class ItemsRankingSerializer(serializers.BaseSerializer):
	def to_representation(self, bar):
		r = get_redis()

		return {
			'ranking': r.zrevrange(redis_keys['ITEMS_RANKING'] % bar.id, 0, -1, withscores=True)
		}


class TotalByHourSerializer(serializers.BaseSerializer):
	def to_representation(self, bar):
		r = get_redis()

		items_list = r.zrevrange(redis_keys['ITEMS_RANKING'] % bar.id, 0, -1, withscores=True)

		total = 0
		for item in items_list:
			total += item[1]

		return {
			'average': total
		}


class UsersRankingByItemSerializer(serializers.BaseSerializer):
	def to_representation(self, bar, item):
		r = get_redis()

		return {
			'ranking': r.zrevrange(redis_keys['ITEMS_RANKING_BY_USER'] % (bar.id, item.name), 0, -1, withscores=True)
		}
