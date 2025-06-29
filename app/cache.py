from aiocache import caches

# ✅ Configure aiocache to use in-memory cache
caches.set_config({
    "default": {
        "cache": "aiocache.SimpleMemoryCache",
        "serializer": {
            "class": "aiocache.serializers.JsonSerializer"
        },
        "ttl": 600  # Optional default TTL (10 minutes)
    }
})