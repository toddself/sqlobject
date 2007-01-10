from py.test import raises
from sqlobject import *
try:
    sorted
except NameError:
    # For Python 2.2 and 2.3:
    from sqlobject.events import sorted
from sqlobject.inheritance import InheritableSQLObject
from sqlobject.versioning import Versioning
from sqlobject.tests.dbtest import *

from datetime import datetime


class MyClass(SQLObject):
    name = StringCol()
    versions = Versioning()

class Base(InheritableSQLObject):
    name = StringCol()
    value = IntCol(default=0)
    versions = Versioning()

class Child(Base):
    toy = StringCol()

class Government(InheritableSQLObject):
    name = StringCol()

class Monarchy(Government):
    monarch = StringCol()
    versions = Versioning()

class VChild(Base):
    weapon = StringCol()
    versions = Versioning()

class HasForeign(SQLObject):
    foreign = ForeignKey("Base")
    versions = Versioning()

<<<<<<< .mine
def _set_extra():
    return "read all about it"

class Extra(SQLObject):
    name = StringCol()
    versions = Versioning(extraCols={'extra' : StringCol(default=_set_extra())})


def setup():
    for cls in [MyClass, Base, Child, Government, Monarchy, VChild, HasForeign, Extra]:
        if hasattr(cls, 'versions') and hasattr(cls, "_connection") and \
                cls._connection.tableExists(cls.sqlmeta.table):
            setupClass(cls.versions.versionClass)
        setupClass(cls)
        if hasattr(cls, 'versions'):
            setupClass(cls.versions.versionClass)
            for version in cls.versions.versionClass.select():
                version.destroySelf()

def test_versioning():

    #the simple case
    setup()
    mc = MyClass(name='fleem')
    mc.set(name='morx')
    assert len(list(mc.versions)) == 1
    assert mc.versions[0].name == "fleem"

    assert len(list(MyClass.select())) == 1

def test_inheritable_versioning():
    setup()

    #base versioned, child unversioned
    base = Base(name='fleem')
    base.set(name='morx')
    assert len(list(base.versions)) == 1
    assert base.versions[0].name == "fleem"
    assert len(list(Base.select())) == 1

    child = Child(name='child', toy='nintendo')
    child.set(name='teenager', toy='guitar')
    assert len(list(child.versions)) == 0


    #child versioned, base unversioned
    government = Government(name='canada')
    assert not hasattr(government, 'versions')

    monarchy = Monarchy(name='UK', monarch='king george iv')
    monarchy.set(name='queen elisabeth ii')
    assert len(list(monarchy.versions)) == 1
    assert monarchy.versions[0].name == "UK"
    assert len(list(Monarchy.select())) == 1

    #both parent and child versioned
    num_base_versions = len(list(base.versions))
    vchild = VChild(name='kid', weapon='slingshot')
    vchild.set(name='toon', weapon='dynamite')
    assert len(list(base.versions)) == num_base_versions
    assert len(list(vchild.versions)) == 1

def test_restore():
    setup()
    base = Base(name='fleem')
    base.set(name='morx')
    assert base.name == "morx"
    base.versions[0].restore()
    assert base.name == "fleem"

    monarchy = Monarchy(name='USA', monarch='Emperor Norton I')
    monarchy.set(name='morx')
    assert monarchy.name == "morx"
    monarchy.versions[0].restore()
    assert monarchy.name == "USA"
    assert monarchy.monarch == "Emperor Norton I"

def test_next():
    setup()
    base = Base(name='first', value=1)
    base.set(name='second')
    base.set(name='third', value=2)
    version = base.versions[0]
    assert version.nextVersion() == base.versions[1]
    assert version.nextVersion().nextVersion() == base

def test_get_changed():
    setup()
    base = Base(name='first', value=1)
    base.set(name='second')
    base.set(name='third', value=2)
    assert base.versions[0].getChangedFields() == ['Name']
    assert sorted(base.versions[1].getChangedFields()) == ['Name', 'Value']

def test_foreign_keys():
    setup()
    base1 = Base(name='first', value=1)
    base2 = Base(name='first', value=1)
    has_foreign = HasForeign(foreign = base1)
    has_foreign.foreign = base2
    assert has_foreign.versions[0].foreign == base1

def test_extra():
    setup()
    extra = Extra(name='title')
    extra.name = 'new'
    assert extra.versions[0].extra == 'read all about it'    
