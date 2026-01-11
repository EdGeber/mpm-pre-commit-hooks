import io
import sys
import argparse
from typing import Sequence
from ruamel.yaml import YAML

UNITY_HEADER = (
"""%YAML 1.1
%TAG !u! tag:unity3d.com,2011:
--- !u!114 &11400000
"""
)

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args(argv)
    
    verbose: bool = args.verbose

    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    retval = 0
    for filename in args.filenames:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                no_header = "".join(f.readlines()[3:])
                data = list(yaml.load_all(no_header))

            modified = False
            for doc in data:
                container = doc.get('MonoBehaviour') if isinstance(doc, dict) else None
                
                if not container or not all(k in container for k in ('isReadonly', 'defaultValue', 'currentValue', 'newValue')):
                    continue
                
                d_val = container['defaultValue']
                
                if container['newValue'] != None and str(container['newValue']) != d_val:
                    container['newValue'] = d_val
                    modified = True
                
                if str(container['isReadonly']).strip() == "1":
                    continue
                
                if container['currentValue'] == d_val:
                    continue
                container['currentValue'] = d_val
                modified = True

            if modified:
                with open(filename, 'w', encoding='utf-8') as f:
                    stream = io.StringIO()
                    yaml.dump(data[0], stream)
                    content = stream.getvalue()
                    f.write(UNITY_HEADER + content)
                retval = 1

        except Exception as e:
            if verbose:
                print(f"Error processing {filename}: {e}")

    return retval

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
