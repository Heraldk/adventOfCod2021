from rich.console import Console
from typing import List, Dict, Set, Optional
from collections import defaultdict


def read_input(lines: List[str]) -> Dict[str, List[str]]:
    map: Dict[str, List[str]] = defaultdict(list)
    for line in lines:
        names = line.strip().split("-")
        map[names[0]].append(names[1])
        map[names[1]].append(names[0])
    return map


def find_all_paths(
    map: Dict[str, List[str]],
    currentLoc: str,
    currentPath: List[str],
    visited: Set[str],
    visited_twice: Optional[str],
    completePaths: List[str],
):

    if currentLoc == "end":
        currentPath.append("end")
        completePaths.append(currentPath)
        return completePaths

    if currentLoc.islower():
        visited.add(currentLoc)

    for neighbour in map[currentLoc]:
        if neighbour not in visited or (
            visited_twice is None and neighbour not in ["start", "end"]
        ):
            next_path = list(currentPath)
            next_path.append(currentLoc)
            next_visited_twice = (
                visited_twice if neighbour not in visited else neighbour
            )
            find_all_paths(
                map, neighbour, next_path, visited, next_visited_twice, completePaths
            )

    if currentLoc.islower() and visited_twice != currentLoc:
        visited.remove(currentLoc)

    return completePaths


console = Console()
with open("day12.txt", "r") as file:
    console.print("[b yellow]Day 12[/b yellow]")
    map = read_input(file.readlines())
    completePaths = find_all_paths(map, "start", [], set(), "start", [])
    console.print(len(completePaths))
    completePathsWithOneRevisit = find_all_paths(map, "start", [], set(), None, [])
    console.print(len(completePathsWithOneRevisit))
