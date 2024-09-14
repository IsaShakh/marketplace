import re
from rules.contrib.rest_framework import AutoPermissionViewSetMixin

nullable = dict(blank=True, null=True)

def slugify(s):
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh',
        'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts',
        'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu',
        'я': 'ya',
    }

    lower_case = s.lower()

    transliterated = ''.join([translit_dict.get(c, c) for c in lower_case])

    # Замена любых неподходящих символов на дефис
    slug = re.sub(r'\W+', '-', transliterated)

    # Удаление лишних дефисов
    slug = re.sub(r'^-+|-+$', '', slug)

    return slug

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




