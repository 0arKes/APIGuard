from django.core.cache import cache

from monitoring.models import API


def get_user_apis(user_id: int):
    cache_key = f"user:{user_id}:apis"

    user_apis = cache.get(cache_key)

    if user_apis is None:
        user_apis = list(API.objects.filter(owner_id=user_id))

        cache.set(
            cache_key,
            user_apis,
            timeout=30,
        )

    return user_apis


def invalidate_user_apis(user_id: int):
    cache_key = f"user:{user_id}:apis"

    cache.delete(cache_key)
