#!/usr/bin/env python
"""
Tabloo -- Minimalistic dashboard app for visualizing tabular data.
"""

from __future__ import division, print_function

import argparse
import sys
import os

import pandas as pd

import tabloo


def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "file",
        metavar="<FILE>",
        help="CSV/xlsx file to load.",
    )
    parser.add_argument(
        "--sep",
        help="Separator character for CSV files.",
    )
    args = parser.parse_args(args=args)
    return args


def load_csv(args):
    loader_kwargs = dict()
    if args.sep is not None:
        loader_kwargs["sep"] = args.sep
    df = pd.read_csv(args.file, **loader_kwargs)
    return df


def load_excel(args):
    df = pd.read_excel(args.file)
    return df


FILE_LOADERS = {
    "csv": load_csv,
    "xlsx": load_excel,
}


def load_file(args):
    *_, extension = os.path.splitext(args.file)
    if not extension:
        raise ValueError(f"No File extension found in {args.file}")

    extension = extension.lower().strip(".")

    try:
        df = FILE_LOADERS[extension](args)
        return df
    except (KeyError):
        raise NotImplementedError(f"File extension {extension} currently not supported")



def main():
    args = parse_args()

    df = load_file(args)
    print(df)

    tabloo.show(
        df,
        server_logging=True,
    )


if __name__ == "__main__":
    main()
