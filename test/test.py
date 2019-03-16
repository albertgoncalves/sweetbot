#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.utils import check_float


def test_check_float():
    assert check_float(4.0) == 4
    assert check_float(4.1) == 4.1
