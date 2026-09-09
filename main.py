import csv
from pathlib import Path

from parser import LDrawColorParser

from utils import color_attributes_to_category, find_color_group, rgb_to_cmyk

bl_color_path = Path("StudioColorDefinition.txt")

with bl_color_path.open() as f:
    bl_color_rows = list(csv.DictReader(f, delimiter="\t"))

bl_colors_by_ldraw_code = {int(row["LDraw Color Code"]): row for row in bl_color_rows}
highest_code = max(
    max(int(row["Studio Color Code"] or "0"), int(row["BL Color Code"] or "0"))
    for row in bl_colors_by_ldraw_code.values()
)

ldraw_parser = LDrawColorParser("LDConfig.ldr")

new_bl_color_rows = []

for ldraw_code, c in ldraw_parser.colors_by_code.items():
    if c.rgb is None:
        continue

    default = lambda x, d: x if x is not None else d
    name, alpha, color_attributes = (
        default(c.name, c.rgb),
        default(c.alpha, 255),
        default(c.color_attributes, []),
    )

    if ldraw_code not in bl_colors_by_ldraw_code:
        new_row = {
            "Studio Color Code": highest_code + 1,
            "BL Color Code": highest_code + 1,
            "LDraw Color Code": ldraw_code,
            "LDD color code": ldraw_code,
            "Studio Color Name": name.replace("_", " "),
            "BL Color Name": name,
            "LDraw Color Name": name,
            "LDD Color Name": name,
            "RGB value": c.rgb,
            "Alpha": f"{alpha / 255:g}",
            "CategoryName": color_attributes_to_category(color_attributes),
            "Color Group Index": find_color_group(c.rgb, bl_color_rows),
            "note": "o",
            "Ins_RGB": c.rgb,
            "Ins_CMYK": rgb_to_cmyk(c.rgb),
        }
        new_bl_color_rows.append(new_row)
        highest_code += 1

bl_color_rows = new_bl_color_rows + bl_color_rows


bl_color_out_path = Path("StudioColorDefinition_updated.txt")

with bl_color_out_path.open("w") as f:
    fieldnames = bl_color_rows[0].keys()

    writer = csv.DictWriter(f, fieldnames, delimiter="\t")

    writer.writeheader()
    writer.writerows(bl_color_rows)
