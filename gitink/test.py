import os
from .main import main


def test_main():
    _this_path = os.path.dirname(os.path.realpath(__file__))
    for (in_file, time_direction) in [('right', 90),
                                      ('up', 0),
                                      ('down', 180)]:
        in_file_name = os.path.join(_this_path, 'test', '{0}.txt'.format(in_file))
        ref_file_name = os.path.join(_this_path, 'test', '{0}.svg'.format(in_file))
        svg = main(1.0, in_file_name, time_direction)
        with open(ref_file_name, 'r') as f:
            reference = f.read()
            assert svg in reference, "failed to test {0}".format(in_file)
