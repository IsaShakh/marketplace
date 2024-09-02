from collections.abc import Iterable
from typing import Dict, TYPE_CHECKING

from rest_framework import mixins, status as rest_status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rules.contrib.rest_framework import AutoPermissionViewSetMixin

__all__ = [
    'AppViewSet',
    'ReadOnlyAppViewSet',
    'ReadCreateAppViewSet',
    'MultiSerializerMixin',
    'ResponseWithRetrieveSerializerMixin',
    'AppUpdateModelMixin',
    'AppCreateModelMixin',
    'ReadCreateDeleteViewSet',
    'ReadCreateUpdateViewSet',
    'ListCreateDeleteViewSet',
]

if TYPE_CHECKING:
    GenericViewSetMixin = GenericViewSet
else:
    GenericViewSetMixin = object


class DefaultViewSetMixin(AutoPermissionViewSetMixin):
    """
    django_rules's default permission map allows `list` action w/out any permissions.
    However in most cases, this doesn't work for us:
    we usually need some sort for restriction for `list` (at least to logged in users).
    So we tie `list` action to `view` permission as a default.
    """

    permission_type_map = {
        **AutoPermissionViewSetMixin.permission_type_map,
        "list": "view",
    }

    def get_object(self):
        if not hasattr(self, '_object'):
            self._object = super().get_object()  # noqa
        return self._object


class MultiSerializerMixin(GenericViewSetMixin):
    """
    Picks serializer class from serializer_action_classes attribute defining directly for actions.
    """
    serializer_action_classes: Dict[str, Serializer]

    def get_serializer_class(self, action=None):
        """
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:
        class MyViewSet(MultiSerializerViewSetMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_action_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }
            @action
            def my_action:
                ...
        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.
        Thanks gonz: https://stackoverflow.com/a/22922156/11440
        """
        if action is None:
            action = self.action

        try:
            return self.serializer_action_classes[action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class ResponseWithRetrieveSerializerMixin(MultiSerializerMixin):
    """
    Extends MultiSerializerMixin with the 'response' method which allows
    serializing response data to any request with retrieve or default serializer.
    """

    def response(self, serializer, instance, status):
        """
        Provide response data with default or retrieve serializer
        """
        retrieve_serializer_class = self.get_serializer_class(action='retrieve')
        retrieve_serializer = retrieve_serializer_class(instance,
                                                        many=isinstance(instance, Iterable),
                                                        context=self.get_serializer_context())
        headers = self.get_success_headers(serializer.data)
        return Response(retrieve_serializer.data, status=status, headers=headers)

    def get_success_headers(self, *args, **kwargs):
        return None


class AppCreateModelMixin(ResponseWithRetrieveSerializerMixin):
    """
    Rewrite rest_framework.mixins.CreateModelMixin with ability
    serialize response data to create request with retrieve or default serializer
    """
    bulk_create = False

    def create(self, request, *args, **kwargs):
        create_serializer = self.get_serializer(data=request.data,
                                                many=self.bulk_create)  # Here we specify many if this is a bulk-creation
        create_serializer.is_valid(raise_exception=True)
        instance = self.perform_create(create_serializer)
        return self.response(create_serializer, instance,
                             status=rest_status.HTTP_201_CREATED)  # Return detail-serialized created instance

    def perform_create(self, serializer):
        return serializer.save()

    def get_success_headers(self, data):
        """
        copy of rest_framework.mixins.CreateModelMixin get_success_headers method
        """
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class AppUpdateModelMixin(ResponseWithRetrieveSerializerMixin):
    """
    Rewrite rest_framework.mixins.UpdateModelMixin with ability
    serialize response data to update request with retrieve or default serializer
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        update_serializer = self.get_serializer(instance, data=request.data, partial=partial)
        update_serializer.is_valid(raise_exception=True)
        instance = self.perform_update(update_serializer)

        if getattr(instance, '_prefetched_objects_cache', None):  # ↓ DRF comment
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return self.response(update_serializer, instance,
                             status=rest_status.HTTP_200_OK)  # Return detail-serialized updated instance

    def perform_update(self, serializer):
        return serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class ReadOnlyAppViewSet(DefaultViewSetMixin, MultiSerializerMixin, ReadOnlyModelViewSet):
    """
    Patch rest_framework.viewsets.ReadOnlyModelViewSet with MultiSerializerMixin mixin
    """


class ReadCreateAppViewSet(DefaultViewSetMixin,
                           AppCreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    """
    Patch rest_framework.viewsets.ReadOnlyModelViewSet with MultiSerializerMixin and AppCreateModelMixin mixins
    """


class ReadCreateDeleteViewSet(
    DefaultViewSetMixin,
    AppCreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    pass


class ReadCreateUpdateViewSet(
    DefaultViewSetMixin,
    AppCreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):
    pass


class CRUDViewSet(
    DefaultViewSetMixin,
    AppCreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    pass


class ListCreateDeleteViewSet(
    DefaultViewSetMixin,
    AppCreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    pass


class AppListViewSet(DefaultViewSetMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    pass


class AppViewSet(
                 AppCreateModelMixin,
                 mixins.RetrieveModelMixin,
                 AppUpdateModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.ListModelMixin,
                 GenericViewSet):
    """
    Patch rest_framework.viewsets.ModelViewSet with mixins: MultiSerializerMixin, AppCreateModelMixin and AppUpdateModelMixin.
    Allows create and update instances with corresponding create and update serializers,
    but always serialize response with serializer_class retrieve or default serializer.
    """
