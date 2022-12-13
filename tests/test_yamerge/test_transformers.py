from math import pi

from yamerge.engine import TransformerSystem
from yamerge.transformers import AbsoluteMergeTransformerGenerator, RelativeMergeTransformerGenerator
from yamerge.yaml_access import load_yaml_file


def test_absolute_merge():
    yaml_data = load_yaml_file('tests_data/file_1.yml')

    search_paths = ['tests_data']

    yaml_data = TransformerSystem([
        AbsoluteMergeTransformerGenerator(merge_tag_name='MERGE', paths=search_paths),
        RelativeMergeTransformerGenerator(merge_tag_name='MERGE-SNIPPET', paths=search_paths)
    ]).apply(yaml_data)

    assert yaml_data['foo']['b'] == 7
    assert yaml_data['foo']['c'] == 42
    assert 'this_will_not_be_merged' not in yaml_data


def test_relative_merge():
    yaml_data = load_yaml_file('tests_data/some_file.yml')

    search_paths = ['tests_data']

    yaml_data = TransformerSystem([
        AbsoluteMergeTransformerGenerator(merge_tag_name='MERGE', paths=search_paths),
        RelativeMergeTransformerGenerator(merge_tag_name='MERGE-SNIPPET', paths=search_paths)
    ]).apply(yaml_data)

    print(yaml_data)
    assert yaml_data['steps'][1]['b'] - pi < 1e-5
