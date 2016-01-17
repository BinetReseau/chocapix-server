from django.db import models

from rest_framework import decorators, serializers, viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from bars_django.utils import VirtualField, permission_logic, CurrentBarCreateOnlyDefault, CurrentUserCreateOnlyDefault
from bars_core.models.bar import Bar
from bars_core.models.user import User
from bars_core.perms import PerBarPermissions, PerBarPermissionsOrAnonReadOnly, BarRolePermissionLogic

@permission_logic(BarRolePermissionLogic())
class SuggestedItem(models.Model):
    class Meta:
        app_label = 'bars_items'

    bar = models.ForeignKey(Bar)
    name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    voters_list = models.ManyToManyField(User)
    added = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class SuggestedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestedItem

    _type = VirtualField("SuggestedItem")
    bar = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentBarCreateOnlyDefault())
    voters_list = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    def create(self, validated_data):
        si = SuggestedItem.objects.create(**validated_data)
        si.voters_list.add(self.context.get('request').user)
        return si


class SuggestedItemViewSet(viewsets.ModelViewSet):
    queryset = SuggestedItem.objects.all()
    serializer_class = SuggestedItemSerializer
    permission_classes = (PerBarPermissionsOrAnonReadOnly, )
    search_fields = ('name', )

    def create(self, request):
        s = SuggestedItemSerializer(data=request.data, context={'request': request})
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        else:
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    @decorators.detail_route(methods=['put'])
    def vote(self, request, pk=None):
        try:
            si = SuggestedItem.objects.get(pk=pk)
        except SuggestedItem.DoesNotExist:
            raise Http404("SuggestedItem (id %d) was not found." % pk)

        si.voters_list.add(request.user)
        si.save()
        s = SuggestedItemSerializer(si)

        return Response(s.data, status=status.HTTP_200_OK)

    @decorators.detail_route(methods=['put'])
    def unvote(self, request, pk=None):
        try:
            si = SuggestedItem.objects.get(pk=pk)
        except SuggestedItem.DoesNotExist:
            raise Http404("SuggestedItem (id %d) was not found." % pk)

        si.voters_list.remove(request.user)
        si.save()
        s = SuggestedItemSerializer(si)

        return Response(s.data, status=status.HTTP_200_OK)
