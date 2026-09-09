"""
parser.py - Parsing of LDraw LDConfig.ldr color definitions.

Adapted from parts.py in the python-ldraw package
(https://github.com/rienafairefr/python-ldraw).

Original copyright (C) 2008 David Boddie <david@boddie.org.uk>
Modifications Copyright (C) 2026 Waël Hazami <wl.hazami@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import codecs

from enum import Enum


class LDrawColorParser:
    class ColorAttributes(Enum):
        CHROME = "CHROME"
        PEARLESCENT = "PEARLESCENT"
        RUBBER = "RUBBER"
        MATTE_METALLIC = "MATTE_METALLIC"
        METAL = "METAL"

    def __init__(self, path):
        self.colors = {}
        self.alpha_values = {}
        self.color_attributes = {}

        self.colors_by_name = {}
        self.colors_by_code: dict[int, Color] = {}

        self.load(path)

    def load(self, path):
        try:
            colors_part = Part(path)
        except PartError:
            return
        for obj in colors_part.objects:
            if not isinstance(obj, MetaCommand) or not obj.type == "COLOUR":
                continue
            pieces = obj.text.split()
            try:
                name = pieces[0]
                code = int(pieces[pieces.index("CODE") + 1])
                rgb = pieces[pieces.index("VALUE") + 1]

                self.colors[name] = rgb
                self.colors[code] = rgb

                color = Color(code, name, rgb)
                self.colors_by_name[name] = color
                self.colors_by_code[code] = color

            except (ValueError, IndexError):
                continue
            try:
                alpha_at = pieces.index("ALPHA")
                alpha = int(pieces[alpha_at])
                self.alpha_values[name] = alpha
                self.alpha_values[code] = alpha
            except (IndexError, ValueError):
                pass

            color_attributes = []
            for attribute in LDrawColorParser.ColorAttributes:
                if attribute.value in pieces:
                    color_attributes.append(attribute)

            self.color_attributes[name] = color_attributes
            self.color_attributes[code] = color_attributes

            alpha = self.alpha_values.get(name, 255)
            color = Color(code, name, rgb, alpha, color_attributes)
            self.colors_by_name[name] = color
            self.colors_by_code[code] = color


class Color:
    """a Color, uniquely identified by a code"""

    def __init__(
        self,
        code=None,
        name: str | None = None,
        rgb=None,
        alpha=None,
        color_attributes=None,
    ):
        self.code = code
        self.name = name
        self.rgb = rgb
        self.alpha = alpha
        self.color_attributes = color_attributes

    def __eq__(self, other):
        if isinstance(other, Color):
            return self.code == other.code
        return self.code == other

    def __hash__(self):
        return hash(self.code)


class PartError(Exception):
    """An exception happening during Part file processing"""

    pass


class Part:
    """
    Contains data from a LDraw part file
    """

    def __init__(self, path):
        self.path = path

    @property
    def lines(self):
        try:
            for line in codecs.open(self.path, "r", encoding="utf-8"):
                yield line
        except IOError:
            raise PartError("Failed to read part file: %s" % self.path)

    @property
    def objects(self):
        """Load the Part from its path"""
        for number, line in enumerate(self.lines):
            pieces = line.split()
            if not pieces:
                continue
            try:
                handler = HANDLERS[pieces[0]]
            except KeyError:
                raise PartError(
                    "Unknown command (%s) in %s at line %i"
                    % (self.path, pieces[0], number)
                )
            try:
                yield handler(pieces[1:])
            except PartError as parse_error:
                raise PartError(
                    str(parse_error) + " in %s at line %i" % (self.path, number)
                )


class MetaCommand:
    """a metacommand"""

    def __init__(self, type, text):
        self.type = type
        self.text = text


class Comment:
    """a comment"""

    def __init__(self, text):
        self.text = text


def _comment_or_meta(pieces):
    if not pieces:
        return Comment("")
    elif pieces[0][:1] == "!":
        return MetaCommand(pieces[0][1:], " ".join(pieces[1:]))
    return Comment(" ".join(pieces))


HANDLERS = {
    "0": _comment_or_meta,
    "1": lambda: None,
    "2": lambda: None,
    "3": lambda: None,
    "4": lambda: None,
    "5": lambda: None,
}
