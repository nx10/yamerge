from math import pi
import pathlib as pl

from yamerge.engine import TransformerSystem
from yamerge.transformers import AbsoluteMergeTransformerGenerator, RelativeMergeTransformerGenerator
from yamerge.yaml_access import load_yaml_file


DIR_DATA = pl.Path('tests_data')

def test_absolute_merge():
    yaml_data = load_yaml_file(DIR_DATA / 'file_1.yml')

    search_paths = [DIR_DATA]

    yaml_data = TransformerSystem([
        AbsoluteMergeTransformerGenerator(merge_tag_name='MERGE', paths=search_paths),
        RelativeMergeTransformerGenerator(merge_tag_name='MERGE-SNIPPET', paths=search_paths)
    ]).apply(yaml_data)

    assert yaml_data['foo']['b'] == 7
    assert yaml_data['foo']['c'] == 42
    assert 'this_will_not_be_merged' not in yaml_data


def test_relative_merge():
    yaml_data = load_yaml_file(DIR_DATA / 'some_file.yml')

    search_paths = [DIR_DATA]

    yaml_data = TransformerSystem([
        AbsoluteMergeTransformerGenerator(merge_tag_name='MERGE', paths=search_paths),
        RelativeMergeTransformerGenerator(merge_tag_name='MERGE-SNIPPET', paths=search_paths)
    ]).apply(yaml_data)

    print(yaml_data)
    assert yaml_data['steps'][1]['b'] - pi < 1e-5


def test_merge_order():

    yaml_data = load_yaml_file(DIR_DATA / 'merge_order_1.yml')

    search_paths = [DIR_DATA]

    yaml_data = TransformerSystem([
        AbsoluteMergeTransformerGenerator(merge_tag_name='MERGE', paths=search_paths),
        RelativeMergeTransformerGenerator(merge_tag_name='MERGE-SNIPPET', paths=search_paths)
    ]).apply(yaml_data)

    assert yaml_data['a']['b']['c']['x'] == 1
    assert yaml_data['a']['b']['c']['y'] == 2
    assert yaml_data['a']['b']['c']['z'] == 3
