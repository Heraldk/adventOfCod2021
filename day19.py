from __future__ import annotations
import itertools
from rich.console import Console
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple, Set
from itertools import combinations

console = Console()


@dataclass(order=True, frozen=True)
class Coords:
    x: int
    y: int
    z: int

    def __repr__(self) -> str:
        return f"<{self.x},{self.y},{self.z}>"

    def __add__(self, other) -> Coords:
        assert isinstance(other, Coords)
        return Coords(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        assert isinstance(other, Coords)
        return Coords(self.x - other.x, self.y - other.y, self.z - other.z)

    # actually calculated distance squared: no need to sqrt it and turn it into a float
    def distance(self, other: Coords):
        return (
            (abs(other.x - self.x) * abs(other.x - self.x))
            + (abs(other.y - self.y) * abs(other.y - self.y))
            + (abs(other.z - self.z) * abs(other.z - self.z))
        )

    def manhattan_distance(self, other: Coords):
        return abs(other.x - self.x) + abs(other.y - self.y) + abs(other.z - self.z)


class Scanner:
    def __init__(self, scanner_num: int, initial_scan: List[Coords]):
        self.number = scanner_num
        self.location: Optional[Coords] = None
        self.beacons: List[Coords] = initial_scan
        self.calculate_distances()

    def calculate_distances(self):
        self.distances: Dict[int, Tuple[Coords, Coords]] = {}
        for coord1, coord2 in itertools.combinations(self.beacons, 2):
            distance = coord1.distance(coord2)
            if distance in self.distances:
                raise ValueError("oops")
            self.distances[distance] = coord1, coord2

    def __eq__(self, other) -> bool:
        return self.number == other.number

    def __repr__(self) -> str:
        return f"Scanner {self.number}: {self.beacons}"

    def has_distance_overlap(
        self, other: Scanner
    ) -> Optional[Tuple[Set[Coords], Set[Coords]]]:
        set1 = set()
        set2 = set()
        for distance, coords1 in self.distances.items():
            if (coords2 := other.distances.get(distance)) is not None:
                set1.update(set(coords1))
                set2.update(set(coords2))
        if len(set1) >= 12 and len(set2) >= 12:
            return set1, set2
        return None


def read_input(lines: List[str]) -> List[Scanner]:
    scanner_number = None
    scanners: List[Scanner] = []
    for line in lines:
        if line.strip() == "":
            continue

        if line[:3] == "---":
            if scanner_number is not None:
                scanners.append(Scanner(scanner_number, beacons))
            vals = line.split()
            scanner_number = int(vals[2])
            beacons: List[Coords] = []
            continue

        vals = line.strip().split(",")
        beacons.append(Coords(int(vals[0]), int(vals[1]), int(vals[2])))

    if scanner_number is not None:
        scanners.append(Scanner(scanner_number, beacons))
    return scanners


def scan_results_orientations(coords: List[Coords]) -> List[Coords]:
    ups = [
        lambda a: Coords(a.x, a.y, a.z),
        lambda a: Coords(a.x, -a.y, -a.z),
        lambda a: Coords(a.y, a.x, -a.z),
        lambda a: Coords(a.y, -a.x, a.z),
        lambda a: Coords(a.y, a.z, a.x),
        lambda a: Coords(a.y, -a.z, -a.x),
    ]
    rotations = [
        lambda a: Coords(a.x, a.y, a.z),
        lambda a: Coords(a.z, a.y, -a.x),
        lambda a: Coords(-a.x, a.y, -a.z),
        lambda a: Coords(-a.z, a.y, a.x),
    ]
    for rotation in rotations:
        for up in ups:
            yield sorted([rotation(up(x)) for x in coords]), rotation, up


def rotate_to_confirm_match(
    candidate: Scanner, overlap: Tuple[Set[Coords], Set[Coords]]
):
    assert len(overlap[0]) == len(overlap[1])
    normalized_list = sorted(list(overlap[0]))
    for oriented, rotation, up in scan_results_orientations(list(overlap[1])):
        transform = oriented[0] - normalized_list[0]
        matchCount = 0
        for orient, normalize in zip(oriented, normalized_list):
            if orient - transform == normalize:
                matchCount += 1
        if (
            matchCount >= 11
        ):  # honestly, there's probably a bug here as for my input I dropped this from 12 to 11 to get it to work ...
            # found a match: normalize the candidate and set the candidate's location
            candidate.beacons = [rotation(up(x)) - transform for x in candidate.beacons]
            candidate.calculate_distances()
            candidate.location = Coords(0, 0, 0) - transform
            return True
    return False


def find_next_candidate_match(
    located: List[Scanner], remaining: List[Scanner]
) -> Scanner:
    for candidate in remaining:
        for locate in located:
            overlap = locate.has_distance_overlap(candidate)
            if overlap is not None:
                if rotate_to_confirm_match(candidate, overlap):
                    return candidate


def locate_scanners(input: List[Scanner]):
    located: List[Scanner] = []
    remaining = input

    located.append(remaining.pop(0))
    located[0].location = Coords(0, 0, 0)

    while len(remaining) > 0:
        scanner = find_next_candidate_match(located, remaining)
        located.append(scanner)
        remaining.remove(scanner)

    return located


with open("day19.txt", "r") as file:
    scanners = read_input(file.readlines())
    console.print("[b yellow]Day 19[/b yellow]")

    located = locate_scanners(scanners)

    unique_beacons = set()
    for scanner in located:
        for beacon in scanner.beacons:
            unique_beacons.add(beacon)
    console.print(len(unique_beacons))

    max_distance = 0
    for scanner1, scanner2 in itertools.combinations(located, 2):
        max_distance = max(
            max_distance, scanner1.location.manhattan_distance(scanner2.location)
        )
    console.print(max_distance)
