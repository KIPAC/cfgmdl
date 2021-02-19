#!/usr/bin/env python
"""
Test the model build
"""
import numpy as np

from cfgmdl import Model, Parameter

from collections import OrderedDict as odict

def test_parameter():
    try:
        class TestClass(Model):
            vv = Parameter(dummy=3)
    except AttributeError: pass
    else: raise AttributeError("Failed to catch AttributeError")

    class TestClass(Model):
        vv = Parameter()

    test_obj = TestClass()
    assert np.isnan(test_obj.vv)

    import pdb
    #pdb.set_trace()
    test_obj.vv = 0.3
    assert test_obj.vv == 0.3
    test_obj.vv = [0.3, 0.2, 0.4]
    assert np.allclose(test_obj.vv, [0.3, 0.2, 0.4])

    help(test_obj._vv)
    
    class TestClass(Model):
        vv = Parameter(default=0.3)

    test_obj = TestClass()

    assert test_obj.vv == 0.3
    test_obj.vv = 0.4
    assert test_obj.vv == 0.4
    test_obj.vv = [0.3, 0.2, 0.4]
    assert np.allclose(test_obj.vv, [0.3, 0.2, 0.4])

    test_obj.vv += 0.1
    assert np.allclose(test_obj.vv, [0.4, 0.3, 0.5])

    try: test_obj._vv.update(3.3, value=3.3)
    except ValueError: pass
    else: raise ValueError("Failed to catch value error")

    try: test_obj._vv.update(3.3, 5.3)
    except ValueError: pass
    else: raise ValueError("Failed to catch value error")

    test_obj._vv.update(dict(value=3.3))
    assert test_obj.vv == 3.3
    
    test_obj = TestClass(vv=[0.3, 0.2, 0.4])    
    assert np.allclose(test_obj.vv, [0.3, 0.2, 0.4])

    test_obj.vv += 0.1
    assert np.allclose(test_obj.vv, [0.4, 0.3, 0.5])

    class TestClass(Model):
        vv = Parameter(default=(3.3))
    test_obj = TestClass(vv=3.5)
    assert test_obj.vv == 3.5
