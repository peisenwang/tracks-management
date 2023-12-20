#!/usr/bin/env python3
import os
import argparse

import gpxpy
from tqdm import tqdm


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Merge multi gpx files into one with simplification')
    parser.add_argument('tracks', nargs='+', help='Paths to gpx file to merge')
    parser.add_argument(
        '-d', '--dist', default=10, help='Distance for simplying tracks')
    parser.add_argument('-o', '--out', required=True, help='Output gpx path')
    parser.add_argument(
        '--nameless', action='store_true',
        help='Don\'t name tracks for better visualization in google earth')
    parser.add_argument(
        '--extensions', action='store_true',
        help='Keep trackpoint extensions (speed etc.) from tracks')
    args = parser.parse_args()

    # assert len(args.tracks) > 1, 'Need more than one gpx files to merge '

    tracks = []
    nsmap = {}
    for path in tqdm(args.tracks):
        with open(path) as f:
            gpx = gpxpy.parse(f)

        assert len(gpx.tracks) == 1
        track = gpx.tracks[0]

        if args.extensions:
            nsmap |= gpx.nsmap
        else:
            for s in track.segments:
                for p in s.points:
                    p.extensions = []

        if args.dist > 0:
            track.simplify(args.dist)

        if args.nameless:
            name = ''
        else:
            name, _ = os.path.splitext(os.path.basename(path))
        track.name = name
        tracks.append(track)

    gpx = gpxpy.gpx.GPX()
    gpx.nsmap = nsmap
    gpx.tracks = tracks

    with open(args.out, 'w') as f:
        f.write(gpx.to_xml())
