#!/usr/bin/env python3
from pathlib import Path

import click
import gpxpy
from tqdm import tqdm


@click.group
def commands():
    pass


@commands.command()
@click.argument('paths', nargs=-1)
def walk(paths):
    for gpx_path in tqdm(paths):
        with open(gpx_path) as f:
            try:
                gpx = gpxpy.parse(f)
            except Exception as e:
                if isinstance(e, KeyboardInterrupt):
                    raise e
                print(f'Exception occurred parsing {gpx_path}: \n{e}')
                continue

        assert len(gpx.tracks) == 1
        track = gpx.tracks[0]
        if len(track.segments) > 1:
            tqdm.write(gpx_path)


def merge_segments(track, thres):
    base_seg = track.segments[0]
    for seg in track.segments[1:]:
        if base_seg.points[-1].distance_2d(seg.points[0]) > thres:
            raise ValueError(
                f'Segment different too large: {thres}, merge aborted.')
        base_seg.join(seg)
    track.segments = [base_seg]
    return track


@commands.command()
@click.argument('path')
@click.option('--thres', type=int, help='Threshold for merging, in meters')
def merge(path, thres=200):
    path = Path(path)
    with path.open() as f:
        gpx = gpxpy.parse(f)

    track = gpx.tracks[0]
    merge_segments(track, thres)

    with path.open('r') as f:
        f.write(gpx.to_xml())


if __name__ == '__main__':
    commands()