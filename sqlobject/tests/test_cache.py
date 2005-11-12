from sqlobject import *
from dbtest import *
from sqlobject.cache import CacheSet

class Something(object):
    pass

def test_purge1():
    x = CacheSet()
    y = Something()
    obj = x.get(1, y.__class__)
    assert obj is None
    x.put(1, y.__class__, y)
    x.finishPut(y.__class__)
    j = x.get(1, y.__class__)
    assert j == y
    x.expire(1, y.__class__)
    j = x.get(1, y.__class__)
    assert j == None
    x.finishPut(y.__class__)
    j = x.get(1, y.__class__)
    assert j == None
    x.finishPut(y.__class__)


class CacheTest(SQLObject):
    name = StringCol(alternateID=True)

def test_cache():
    setupClass(CacheTest)
    s = CacheTest(name='foo')
    obj_id = id(s)
    s_id = s.id
    assert CacheTest.get(s_id) is s
    assert not s.sqlmeta.expired
    CacheTest.sqlmeta.expireAll()
    assert s.sqlmeta.expired
    del s
    CacheTest.sqlmeta.expireAll()
    s = CacheTest.get(s_id)
    # We should have a new object:
    assert id(s) != obj_id
    obj_id2 = id(s)
    del s
    CacheTest._connection.expireAll()
    s = CacheTest.get(s_id)
    assert id(s) != obj_id and id(s) != obj_id2
    
