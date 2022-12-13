# `yamerge`: YAML file preprocessor



## Usage

```
usage: main.py [-h] [-o OUTPUT] [-p PATHS] [-d] input

Preprocessor for YAML files. Merge data from other YAML files via tags:
`MERGE: file/path.yml` (absolute / same YAML structure) `MERGE-SNIPPET:
path/to/snippet.yml` (relative / merge full YAML).

positional arguments:
  input                 YAML input filepath

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        YAML output filepath (If this is not specified result
                        will be printed to console)
  -p PATHS, --paths PATHS
                        Source directories for yaml files. Default: Working
                        directory (Seperate multiple with `|`. E.g.:
                        `/some/folder|../another/one`)
  -d, --debug           Print debug information
```

### Absolute merge (`MERGE`)

Merge specific branch from other *completely defined* YAML file into input YAML.

- Both files have to have the same structure
- Will only merge all child-nodes from where the `MERGE` tag is nested 
- Caveat: Does not work nested within lists (as there is no stable key/index in lists) <br/> 
  &rarr; *Relative merge* is a list-compatible alternative


```yaml
# file_1.yml

foo:
  MERGE: file_2.yml
  a: 1
  b: 7
  x:
    y: baz
```

```yaml
# file_2.yml

foo:
  b: 999
  c: 42
  x:
    z: bar

this_will_not_be_merged: because MERGE was nested under 'foo'
```

```yaml
# yamerge file_1.yml

foo:
  a: 1
  b: 7   # <- this was already defined in 'file_1.yml' 
  c: 42  # <- this was merged from 'file_2.yml'
  x:
    y: baz
    z: bar
```

### Relative merge (`MERGE-SNIPPET`)

Merge specific branch from a config ‘snippet’ file into input YAML.

- Merge complete YAML file at the location of the `MERGE-SNIPPET` tag.
- Works within lists.

```yaml
# some_file.yml

steps:
  - step-1:
    a: 1
    b: 1
  - step-2:
    MERGE-SNIPPET: some_snippet.yml
    a: 0
  - step-3:
    a: hello
    b: hi
```

```yaml
# some_snippet.yml

a: 1.61803398875
b: 3.14159265359
```

```yaml
# yamerge some_file.yml

steps:
  - step-1:
    a: 1
    b: 1
  - step-2:
    a: 0
    b: 3.14159265359  # <- this got merged
  - step-3:
    a: hello
    b: hi
```


