from Entity import Entity

def test_create_entity():
    entity = Entity("asset", 0, 0, 'right')
    assert entity.direction == 'right'
    assert entity.rect.x == 0
    assert entity.rect.y == 0

def test_get_position():
    entity = Entity("asset", 0, 0, 'right')
    assert entity.get_position == (0,0)

def test_set_position():
    entity = Entity("asset", 0, 0, 'right')
    assert entity.get_position == (0,0)
    entity.set_position(10,10)
    assert entity.get_position == (10,10)

def test_get_direction():
    entity = Entity("asset", 0, 0, 'right')
    assert entity.get_direction() == 'right'

def test_set_direction():
    entity = Entity("asset", 0, 0, 'right')
    assert entity.get_direction() == 'right'
    entity.set_direction('left')
    assert entity.get_direction() == 'left'