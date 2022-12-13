import argparse

from yamerge.engine import TransformerSystem
from yamerge.yaml_access import load_yaml_file, save_yaml_str, save_yaml_file
from yamerge.transformers import AbsoluteMergeTransformerGenerator, RelativeMergeTransformerGenerator


def _cli_parse_args():
    parser = argparse.ArgumentParser(description="Preprocessor for YAML files. Merge data from other YAML files "
                                                 "via tags: `MERGE: file/path.yml` (absolute / same YAML structure)  "
                                                 "`MERGE-SNIPPET: path/to/snippet.yml` (relative / merge full YAML).")
    parser.add_argument('input', type=str, help='YAML input filepath')
    parser.add_argument('-o', '--output', type=str,
                        help='YAML output filepath (If this is not specified result will be printed to console)')
    parser.add_argument('-p', '--paths', type=str, default='.',
                        help='Source directories for yaml files. Default: Working directory (Seperate multiple with '
                             '`|`. E.g.: `/some/folder|../another/one`)')
    parser.add_argument('-d', '--debug', action='store_true', help='Print debug information')
    return parser.parse_args()


def main():
    cli_args = _cli_parse_args()

    if cli_args.debug:
        print('args:', cli_args)

    yaml_data = load_yaml_file(cli_args.input)

    if cli_args.debug:
        print('input data:', yaml_data)
        print(f'--- input yaml ---\n{save_yaml_str(yaml_data)}\n---')

    search_paths = cli_args.paths.split('|')

    yaml_data = TransformerSystem([
        AbsoluteMergeTransformerGenerator(merge_tag_name='MERGE', paths=search_paths),
        RelativeMergeTransformerGenerator(merge_tag_name='MERGE-SNIPPET', paths=search_paths)
    ]).apply(yaml_data)

    if cli_args.debug:
        print('output data:', yaml_data)
        print('---')

    if cli_args.output is None:
        print(save_yaml_str(yaml_data))
    else:
        save_yaml_file(yaml_data, cli_args.output)


if __name__ == '__main__':
    main()
