#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Zauberwürfel Ordnungszahl
https://www.programmieraufgaben.ch/aufgabe/ernoe-rubiks-zauberwuerfelalgorithmen/vymwb4k7
"""

# Programmieraufgabe:
#     Schreiben Sie ein Programm, das von einem Algorithmus für den Zauberwürfel
#     die Ordnugszahl ermittelt.
#         Rubiks Cube
#     Die Ordnungszahl ist diejenige Anzahl, wie oft der Algorithmus ausgeführt
#     werden muss, damit der Würfel in seinen Startzustand gelangt. Mit anderen
#     Worten: Wenn ich einen gelösten Würfel habe und immer wieder den selben
#     Algorithmus darauf anwende: Wie lange dauert es, bis der Würfel wieder
#     gelöst ist.
#
# Autor, Erstellung:
#     Ulrich Berntien, 2018-06-08
#
# Sprache:
#     Python 3.6.6


import re
from typing import *


# Der Zauberwürfel besteht außen aus 26 Steinen. Jeder Stein ist eindeutig
# durch seine Farben (ein bis drei Farben je Element) identifiziert.
# Die Steine liegen auf einem 3x3x3 Gitter im Raum.
# Von einem Stein muss seine Position und seine Orientierung beachtet werden.
# Anstelle einer farbigen Seite eines Steins könte der Stein auch eine farbige
# Kugel auf seiner Seite haben. Diese farbigen Kugeln würden auf einem 5x5x5
# Gitters im Raum liegen.
# Anstelle der Bewegungen der Steine können die Bewegungen der farbigen Kugel
# beobachtet werden. Von diesen farbigen Kugel müssen nur die Positionen, nicht
# die Orientierungen betrachtet werden.
# In der Klasse Cube wird der Raum, das 5x5x5 Gitter, in einem Feld dargestellt.
# Jede der farbigen Kugeln wird durch eine Nummer identifiziert. Die Nummer im
# Feld bedeutet eine Kugel an dem entsprechenden Ort des Gitters.
# Das 5x5x5 Gitter wird in einer Liste mit 125 dargestellt.
# Die räumlichen Positionen (x,y,z) werden dem Index in der Liste durch die Methode
# 'xyz_to_index' zugeordnet. Jede Koordinate kann die Werte 0,1,2 annehmen. Die x-Achse ist
# nach rechts, die y-Achse nach hinten und die z-Achse nach oben gerichtet.
# Im Startzustand ist im Feld mit dem Index i der Stein mit Nummer i enthalten. Beim
# Drehen verändert sich der Inhalt der Liste 'elements'.
# Für jede Seite des Würfels wird eine Drehfunktion 'rotation_up" usw. bei der
# Initialisierung erzeugt. Die Drehfunktionen arbeiten mit einfachen Tabellen
# in der Art 'von Feld i - nach Feld j'.


def xyz_to_index(xyz: Tuple[int, int, int]) -> int:
    """
    Umrechung der Koordinaten in Indexnummer in der Liste.
    :param xyz: x Koordinate x,y,z jeweils im Bereich 0 bis 4
    :return: Index in der Liste 0...124
    """
    assert all(0 <= xyz[i] < 5 for i in range(3))
    return ((xyz[2] * 5) + xyz[1]) * 5 + xyz[0]


def index_to_xyz(index: int) -> Tuple[int, int, int]:
    """
    Index in der Liste umgerechnet in x,y,z Koordinate.
    :param index: Index in der Liste
    :return: Die Koordinate x,y,z des zugeordneten Punkts
    """
    assert 0 <= index < 125
    return index % 5, index // 5 % 5, index // 25


def index_to_str(i: int) -> str:
    """
    Indexnummer in kompakte String-Darstellung 'xyz' umwandeln.
    Die kompakte String-Darstellung ist anschaulicher als die Index-Nummer.
    """
    assert 0 <= i < 125
    return str(i % 5) + str((i // 5) % 5) + str(i // 25)


def _generate_rot(source: List[int], dest90: List[int], dest180: List[int], dest270: List[int]) \
        -> Callable[[object, int], None]:
    """
    Erzeugt eine Drehfunktion basierend auf den Übertragungstabellen.
    :param source: Liste der Index-Nummer der Felder die verschoben werden.
    :param dest90: Für 90° Rotation: Liste der Index-Nummern auf die die Felder kommen.
    :param dest180: Für 180° Rotation: Liste der Index-Nummern auf die die Felder kommen.
    :param dest270: Für 200° Rotation: Liste der Index-Nummern auf die die Felder kommen.
    :return: Funktion für die Rotation des Würfels mit Drehwinkel in Grad als Argument.
    """
    assert len(source) == len(dest90) == len(dest180) == len(dest270)

    def rotation(cube: object, angle: int) -> None:
        """
        Rotation um 0, +/-90, +/-180 oder +/-270 Grad.
        :param cube: Eine Seite dieses Würfels wird gedreht.
        :param angle: Um diesen Winkel wird gedreht.
        """
        angle %= 360
        if angle == 90:
            cube.move(source, dest90)
        elif angle == 180:
            cube.move(source, dest180)
        elif angle == 270:
            cube.move(source, dest270)
        elif angle == 0:
            pass
        else:
            raise ValueError("invalid angle")

    return rotation


def rotation_plane(xyz: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """
    Rotation des Punktes xyz um 90° im Uhrzeigersinn
    um eine z-parallele Achse durch den Punkt (2,2.0).
    :param xyz: Diesen Punkt rotieren.
    :return: Die Koordinaten nach der Rotation.
    """
    return xyz[1], 4 - xyz[0], xyz[2]


def _generate_rotation(side_to_xyz: Callable[[Tuple[int, int, int]], Tuple[int, int, int]]) -> \
        Callable[[object, int], None]:
    """
    Erzeugt die Drehfunktion für eine Seite des Würfels.
    :param side_to_xyz: Liefert die Koordinaten x,y,z für einen Stein im Würfel
     als Funktion der x,y,z Koordinaten für einen Stein auf der Seite.
    :return: Funktion für die Rotation der Seite mit Parameter: Würfel, Winkel in Grad
    """
    # Die Koordinaten der Farbkugeln auf der Seite und an den Rändern der Seite
    side = [(x, y, 1) for x in range(1, 4) for y in range(1, 4)] + \
           [(x, 0, 0) for x in range(1, 4)] + \
           [(x, 4, 0) for x in range(1, 4)] + \
           [(0, y, 0) for y in range(1, 4)] + \
           [(4, y, 0) for y in range(1, 4)]
    # Die Index-Nummer der Felder in der Seite
    source = [xyz_to_index(side_to_xyz(xyz)) for xyz in side]
    # Diese Felder werden bei 90° Rotation im Uhrzeigersinn zu den Feldern
    destination90 = [xyz_to_index(side_to_xyz(rotation_plane(xyz))) for xyz in side]
    # in 90° Schritte weiterdrehen. Der Drehwinkel wird um die x,y oder z-Achse angegeben.
    # Bei positivem Winkel wird im Uhrzeigersinn gedreht.
    destination180 = [xyz_to_index(side_to_xyz(rotation_plane(rotation_plane(xyz)))) for xyz in side]
    destination270 = [xyz_to_index(side_to_xyz(rotation_plane(rotation_plane(rotation_plane(xyz))))) for xyz in side]
    return _generate_rot(source, destination90, destination180, destination270)


class Cube:
    """
    Würfel mit Drehoperationen.
    """

    # Der Index in dem Feld folgt über xyz_to_index aus ein Ort im Raum.
    # Der Wert des Elements i ist die Nummer des Objeks, der an dem Ort i ist.
    elements: ByteString

    @property
    def is_initial_state(self) -> bool:
        """
        Zustand des Würfels mit dem Startzustand vergleichen.
        :return: True genau dann, wenn der Würfel im Startzustand ist.
        """
        return self.elements == Cube._initial_state

    def __repr__(self) -> str:
        """
        Die Codenummer der farbigen Kugeln am Würel werden als kompakte Koordinate ausgegeben.
        :return: Der Zustand des Würfel. Obere, mittlere und untere Seite.
        """
        accu = ""
        for z in range(4, -1, -1):
            for y in range(4, -1, -1):
                for x in range(5):
                    if 4 <= (2 - x) ** 2 + (2 - y) ** 2 + (2 - z) ** 2 <= 6:
                        accu += index_to_str(self.elements[xyz_to_index((x, y, z))]) + " "
                    else:
                        accu += " .  "
                accu += "\n"
            accu += "\n"
        # Das \n am Stringende nicht zurückgeben
        return accu[:-2]

    def move(self, source: List[int], destination: List[int]) -> None:
        """
        Drehen einer Seite anhand einer Bewegungstabelle.
        """
        assert len(source) == len(destination)
        # Kopieren über Zwischenspeicher, weil die Bereiche überlappen.
        buffer = self.elements[:]
        for source_index, destination_index in zip(source, destination):
            self.elements[destination_index] = buffer[source_index]

    # Inhalt des elements Felds, wenn der Würfel im Start-Zustand ist.
    _initial_state = bytes(range(5 * 5 * 5))

    # Funktionen für die Rotationen der einzelnen Seiten
    rotation_up = _generate_rotation(lambda xyz: (xyz[0], xyz[1], 3 + xyz[2]))
    rotation_down = _generate_rotation(lambda xyz: (xyz[1], xyz[0], 1 - xyz[2]))
    rotation_right = _generate_rotation(lambda xyz: (3 + xyz[2], xyz[0], xyz[1]))
    rotation_left = _generate_rotation(lambda xyz: (1 - xyz[2], xyz[1], xyz[0]))
    rotation_back = _generate_rotation(lambda xyz: (xyz[1], 3 + xyz[2], xyz[0]))
    rotation_front = _generate_rotation(lambda xyz: (xyz[0], 1 - xyz[2], xyz[1]))

    def __init__(self) -> None:
        """
        Erzeugt den Würfel im Startzustand.
        """
        self.elements = bytearray(Cube._initial_state)


class CubeCodes:
    """Interpretieren der Cube Rotationen in Zeichenkette."""

    # Tabelle der Rotationsfunktionen für jeden Codebuchstaben.
    rotation_table: Dict[str, Callable[[Cube, int], None]] = {
        "F": Cube.rotation_front,
        "B": Cube.rotation_back,
        "R": Cube.rotation_right,
        "L": Cube.rotation_left,
        "U": Cube.rotation_up,
        "D": Cube.rotation_down}

    # Tabelle der Rotationswinkel für jeden Zeichencode.
    angle_table: Dict[str, int] = {"": 90, "'": -90, "2": 180, "'2": -180}

    @classmethod
    def compile_code(cls, code: str) -> Callable[[Cube], None]:
        """
        Übersetzt einen BewegungsCode in einen Aufruf einer Drehfunktion.
        Die Codes der einzelnen Rotationen nach https://speedcube.de/notation.php:
        F = front, B = back, R = right, L = left, U = up, D = down
        Dem Buchstaben für die Rotation kann ein Zeichen für den Winkel folgen:
        kein Zeichen = 90°, ' = -90°, 2 = 180°, '2 = -180°
        """
        try:
            code = code.strip()
            rotation = cls.rotation_table[code[0:1]]
            angle = cls.angle_table[code[1:]]
            return lambda cube: rotation(cube, angle)
        except KeyError:
            raise RuntimeError("falscher Bewegungscode: " + code)

    @classmethod
    def compile_algorithmus(cls, algorithm: str) -> Callable[[Cube], None]:
        """
        Übersetzt einen Algorithmus-Code in eine Funktion mit dem Drehungen.
        Einzelne Rotationen können mit einem Leerzeichen getrennt sein.
        Die Codes sind in der Funktion compile_code beschrieben.
        :param algorithm: Algorithmus als String.
        :return: Algorithmus in eine Funktion übersetzt.
        """
        program = [cls.compile_code(step) for step in re.split("([A-Z]'?2?)", algorithm) if step.istitle()]

        def run(cube: Cube) -> None:
            for step in program:
                step(cube)

        return run


def calculate_number(algorithm: Callable[[Cube], None]) -> int:
    """
    Berechnen der Ordnungszahl.
    :param algorithm: Der Algorithmus in einer Funktion auf dem Würfel.
    :return: Die Ordnungszahl des Algorithmus.
    """
    cube = Cube()
    assert cube.is_initial_state
    algorithm(cube)
    result: Int = 1
    while not cube.is_initial_state:
        algorithm(cube)
        result += 1
    return result


test_cases = ("R",  # 4
              "L",  # 4
              "U",  # 4
              "D",  # 4
              "F",  # 4
              "B",  # 4
              "R L",  # 4
              "U D",  # 4
              "F B",  # 4
              "R2 U R2",  # 4
              "R' D' R D",  # 6
              "UUR'LLDDB'R'U'B'R'U'B'R'U",  # 336
              "RUR'",  # 4
              "RULD",  # 315
              "RUF",  # 80
              "RUF2",  # 36
              "RUUFU")  # 420
for test in test_cases:
    algo = CubeCodes.compile_algorithmus(test)
    number = calculate_number(algo)
    print("Algorithmus: {:15} Ordnungszahl: {:4}".format(test, number))