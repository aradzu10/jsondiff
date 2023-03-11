#!/usr/bin/env python3
from absl import app, flags

FLAGS = flags.FLAGS
flags.DEFINE_bool("color", True, "Print lines with colors.")


def main(argv):
    pass


if __name__ == '__main__':
    app.run(main)
