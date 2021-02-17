#!/usr/bin/env python
"""
Test the model build
"""
from cfgmdl import Model, Parameter, Property, Derived, Choice

from collections import OrderedDict as odict

class Parent(Model):

    x = Parameter(default=1., help='variable x')
    y = Parameter(default=2., bounds=[0.,10.], help='variable y')
    
class Child(Parent):
    
    z = Parameter(help='variable z')

class test_class(Model):

    req = Property(dtype=float, format='%.1f', required=True, help="A required parameter")
    opt = Property(dtype=float, format='%.1f', default=1.0, help="An optional parameter")
    var = Parameter(default=1.0, bounds=[0., 3.], errors=[0.1, 0.3], free=True, help="A variable parameter")
    var2 = Parameter(default=1.0, free=False, help="A fixed parameter")
    der = Derived(dtype=float, format='%.1f', help="A derived parameter")
    der2 = Derived(dtype=float, format='%.1f', loader="_loader2", help="A derived parameter")
    der3 = Derived(dtype=float, format='%.1f', loader="_loader3", help="A derived parameter")    
    choice = Choice(choices=["a", "b", "c"], default="c")
    
    def _load_der(self):
        return self.req * self.opt * self.var

    def _loader2(self):
        return self.req * self.opt * self.var

    def _loader3(self):
        return "aa"


def test_property():
    
    try:
        class ParamTest(Model):
            vv = Property(dummy=3)
    except AttributeError: pass
    else: raise AttributeError("Failed to catch AttributeError")

    class ParamTest(Model):
        vv = Property()

    pt = ParamTest()
    pt.vv = "aa"
    assert pt.vv == "aa"
    pt.vv = None
    assert pt.vv is None
    pt.vv = 1
    assert pt.vv == 1
    
    help(pt.getp('vv'))
    
    
def test_parameter():
    try:
        class ParamTest(Model):
            vv = Parameter(dummy=3)
    except AttributeError: pass
    else: raise AttributeError("Failed to catch AttributeError")

    class ParamTest(Model):
        vv = Parameter()

    pt = ParamTest()
    pt.vv = 0.3
    assert pt.vv == 0.3
    pt.vv = [0.3, 0.2, 0.4]
    assert pt.vv.size == 3

    help(pt.getp('vv'))
    pt.getp('vv').dump()

    
def test_model():

    a = Parent()

    a.x = 3.
    a.y = 4.

    b = Child()
    b.z = 100.

    t = test_class(req=2.,var=2.)

    #assert t.var2.symetric_error == 0.2
    
    print(str(t))
    
    test_val = t.req * t.opt * t.var
    check = t.der
    assert check==test_val

    check = t.der2
    assert check==test_val

    try: t.der3
    except TypeError: pass
    #else: raise TypeError("Failed to catch TypeError in Derived.__get__")
    
    t.req = 4.
    check = t.der
    assert check==8.

    try:
        t2 = test_class(var=2.)
        check = t.der
        assert False
    except ValueError:
        pass


    try: a.f == 2
    except AttributeError: pass
    else: raise TypeError("Failed to catch AttributeError in Model.__getatt__")

    params = a.get_params()
    assert len(params) == 2

    params = a.get_params(['x'])
    assert len(params) == 1

    vals = a.param_values()
    assert len(vals) == 2
    assert vals[0] == 3.

    vals = a.param_values(['x'])
    assert len(vals) == 1
    assert vals[0] == 3.

    errs = a.param_errors()
    assert len(errs) == 2
    assert errs[0] is None

    errs = a.param_errors(['x'])
    assert len(errs) == 1
    assert errs[0] is None

    a_dict = a.todict()
    a_yaml = a.dump()
    a_str = str(a)

    for key in ['name', 'x', 'y']:
        assert key in a_dict
        assert a_yaml.index(key) >= 0
    for key in ['x', 'y']:
        assert a_str.index(key) >= 0

    try: a.x = 'afda'
    except TypeError: pass
    else: raise TypeError("Failed to catch TypeError in Model.setp")

    aa = Child(x=2.)
    aa.x == 2
    
    aa = test_class(req=5.3)
    assert aa.req == 5.3
    aa.choice = "b"
    assert aa.choice == "b"

    try: aa.choice = "d"
    except ValueError: pass
    else: raise ValueError("Failed to catch ValueError in Choice")
    
    try: bad = test_class(req="aa")
    except TypeError: pass
    else: raise TypeError("Failed to catch TypeError in Model.set_attributes")

    try: bad = Child(vv=dict(value=3))
    except KeyError: pass
    else: raise KeyError("Failed to catch KeyError in Model.set_attributes")
