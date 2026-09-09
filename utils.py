from parser import LDrawColorParser

from math import sqrt
from collections import Counter


def color_attributes_to_category(
    attributes: list[LDrawColorParser.ColorAttributes],
):
    if len(attributes) < 1:
        return "Solid Colors"

    match attributes[0]:
        case LDrawColorParser.ColorAttributes.CHROME:
            return "Chrome Colors"
        case LDrawColorParser.ColorAttributes.PEARLESCENT:
            return "Pearl Colors"
        case LDrawColorParser.ColorAttributes.RUBBER:
            return "Rubber Colors"
        case (
            LDrawColorParser.ColorAttributes.MATTE_METALLIC
            | LDrawColorParser.ColorAttributes.METAL
        ):
            return "Metallic Colors"

    return "Solid Colors"


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return (
        int(value[0:2], 16),
        int(value[2:4], 16),
        int(value[4:6], 16),
    )


def color_distance(
    rgb1: tuple[int, int, int],
    rgb2: tuple[int, int, int],
) -> float:
    return sqrt(
        (rgb1[0] - rgb2[0]) ** 2 + (rgb1[1] - rgb2[1]) ** 2 + (rgb1[2] - rgb2[2]) ** 2
    )


def find_color_group(
    rgb: str,
    rows: list[dict[str, str | None]],
    k: int = 5,
) -> int:
    target = hex_to_rgb(rgb)

    candidates = []

    for row in rows:
        row_rgb = row["RGB value"]
        group = row["Color Group Index"]

        if not row_rgb or not group:
            continue

        try:
            group_index = int(group)
        except ValueError:
            continue

        distance = color_distance(target, hex_to_rgb(row_rgb))

        candidates.append((distance, group_index))

    candidates.sort()

    nearest = candidates[:k]

    group = Counter(group for _, group in nearest).most_common(1)[0][0]

    return group


def rgb_to_cmyk(rgb: str) -> str:
    r, g, b = hex_to_rgb(rgb)

    rf, gf, bf = r / 255, g / 255, b / 255

    k = 1 - max(rf, gf, bf)

    if k == 1:
        c = m = y = 0
    else:
        c = (1 - rf - k) / (1 - k)
        m = (1 - gf - k) / (1 - k)
        y = (1 - bf - k) / (1 - k)

    cmyk = ",".join(str(round(x * 100)) for x in (c, m, y, k))

    return cmyk
