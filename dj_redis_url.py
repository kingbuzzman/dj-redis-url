# -*- coding: utf-8 -*-

import os

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


# Register database schemes in URLs.
urlparse.uses_netloc.append("redis")

DEFAULT_ENV = "REDIS_URL"


def config(env=DEFAULT_ENV, default=None, **overrides):
    """Returns configured REDIS dictionary from REDIS_URL."""

    config = {}

    s = os.environ.get(env, default)

    if s:
        config = parse(s)

    overrides = dict([(k.upper(), v) for k, v in overrides.items()])

    config.update(overrides)

    return config


def parse(url):
    """Parses a database URL."""

    config = {}

    url = urlparse.urlparse(url)

    netloc = url.netloc
    if "@" in netloc:
        netloc = netloc.rsplit("@", 1)[1]
    if ":" in netloc:
        netloc = netloc.split(":", 1)[0]
    hostname = netloc or ''
    if url.scheme == 'unix':
        hostname = url.path
        db = (urlparse.parse_qs(url.query).get('db', []) + [''])[0]
        port = None
    else:
        # Remove query strings.
        db = url.path[1:]
        db = db.split('?', 2)[0]
        port = int(url.port or 6379)

    # Update with environment configuration.
    config.update({
        "DB": int(db or 0),
        "PASSWORD": url.password or None,
        "HOST": hostname or "localhost",
        "PORT": port,
    })

    return config
