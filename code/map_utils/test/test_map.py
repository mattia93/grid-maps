from map_utils import Map
import numpy as np
import sys


def test_map():
    map = Map(3, 3, 30)
    assert map.width == 3
    assert map.height == 3
    assert map.obstacles_perc == 30
    assert map.jump_perc == 25
    assert map.shuffle_edges == True
    assert map.array.shape == (3, 3)
    assert np.sum(map.array) == 3
    assert map.g.vcount() == 9
    assert map.g.ecount() == 12
    assert map.g.is_connected() == True


    map = Map(5, 5, 40)
    map1 = Map.from_array(map.array)
    assert f'{map1}' == f'{map}'


    map = Map(3, 3, 100)
    assert map.width == 3
    assert map.height == 3
    assert map.obstacles_perc == 100
    assert map.jump_perc == 25
    assert map.shuffle_edges == True
    assert map.array.shape == (3, 3)
    assert np.sum(map.array) == 9
    assert map.g.vcount() == 9


    map = Map.from_array(np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]))
    assert map.width == 3
    assert map.height == 3
    assert map.obstacles_perc == 0
    assert map.jump_perc == 25
    assert map.shuffle_edges == True
    assert map.array.shape == (3, 3)
    assert np.sum(map.array) == 0
    assert map.g.vcount() == 9
    assert map.g.ecount() == 12
    assert map.g.is_connected() == True

    map = Map.from_array(np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]))
    assert map.width == 3
    assert map.height == 3
    assert map.obstacles_perc == 100
    assert map.jump_perc == 25
    assert map.shuffle_edges == True
    assert map.array.shape == (3, 3)
    assert np.sum(map.array) == 9
    assert map.g.vcount() == 9


def test_generate_graph():
    map = Map(3, 3, 30)
    map.generate_graph()
    assert map.g.vcount() == 9
    assert map.g.ecount() == 12
    assert map.g.is_connected() == True

    map = Map(3, 3, 30)
    map.generate_graph()
    assert map.g.vcount() == 9
    assert map.g.ecount() == 12
    assert map.g.is_connected() == True

    map = Map.from_array(np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]))
    map.generate_graph()
    assert map.g.vcount() == 9
    assert map.g.ecount() == 12
    assert map.g.is_connected() == True

    map = Map.from_array(np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]))
    map.generate_graph()
    assert map.g.vcount() == 9
    assert map.g.ecount() == 12
    assert map.g.is_connected() == True


def test_create_obstacles():
    map = Map(3, 3, 30)
    map.create_obstacles()
    assert np.sum(map.array) == 3

    map = Map(3, 3, 100)
    map.create_obstacles()
    assert np.sum(map.array) == 9

    map = Map.from_array(np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]))
    map.create_obstacles()
    assert np.sum(map.array) == 0

    map = Map.from_array(np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]))
    map.create_obstacles()
    assert np.sum(map.array) == 9


# write test for select_source_target

def test_select_source_target():
    map = Map(3, 3, 30)
    for _ in range(10):
        source, target = map.select_source_target()
        assert source != target
        assert map.g.vs[source]['crossable'] == True
        assert map.g.vs[target]['crossable'] == True


def test_select_sources_targets():
    map = Map(3, 3, 30)
    tuples = map.select_sources_targets(10)
    assert len(tuples) == 10
    for source, target in tuples:
        assert source != target
        assert map.g.vs[source]['crossable'] == True
        assert map.g.vs[target]['crossable'] == True
    assert len(set(tuples)) == 10


