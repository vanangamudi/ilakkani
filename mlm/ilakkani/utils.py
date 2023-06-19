import gzip
import pdb

def openfile(filepath, mode='rt', *args, **kwargs):
    if filepath.endswith('.gz'):
        return gzip.open(filepath, mode, *args, **kwargs)
    else:
        return open(filepath, mode, *args, **kwargs)


def compare_dict(dict1, dict2, debug=0):
    if isinstance(dict1, dict) and isinstance(dict1, dict):
        dict1keys = sorted(dict1.keys())
        dict2keys = sorted(dict2.keys())

        assert dict1keys == dict2keys
        nested_score = []
        for k in dict1keys:
            _score = compare_dict(dict1[k], dict2[k], debug+1)
            nested_score.append(_score)
            
        return all(nested_score)


    else:
        return dict1 == dict2
