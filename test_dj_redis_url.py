# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import unittest

import dj_redis_url


class RedisTestSuite(unittest.TestCase):

    def test_redis_parsing(self):
        url = 'redis://:password4321@host.domain.com:6379/2'
        url = dj_redis_url.parse(url)

        assert url['HOST'] == 'host.domain.com'
        assert url['PASSWORD'] == 'password4321'
        assert url['PORT'] == 6379
        assert url['DB'] == 2

    def test_redis_default_parsing(self):
        url = 'redis://host.domain.com'
        url = dj_redis_url.parse(url)

        assert url['HOST'] == 'host.domain.com'
        assert url['PASSWORD'] is None
        assert url['PORT'] == 6379
        assert url['DB'] == 0

    def test_redis_socket_parsing(self):
        url = 'unix:///Path/tO/socket/redis.socket?db=3'
        url = dj_redis_url.parse(url)

        assert url['HOST'] == '/Path/tO/socket/redis.socket'
        assert url['PASSWORD'] is None
        assert url['PORT'] is None
        assert url['DB'] == 3

    def test_redis_socket_default_parsing(self):
        url = 'unix:///Path/tO/socket/redis.socket'
        url = dj_redis_url.parse(url)

        assert url['HOST'] == '/Path/tO/socket/redis.socket'
        assert url['PASSWORD'] is None
        assert url['PORT'] is None
        assert url['DB'] == 0


if __name__ == '__main__':
    unittest.main()
