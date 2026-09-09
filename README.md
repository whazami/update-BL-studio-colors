## Description

This repo ensures correct color mapping when importing LDraw files into BrickLink Studio, so your parts no longer show up black.

## Usage

Copy the latest `LDConfig.ldr` file to the root of the repo.

Copy your `C:\Program Files\Studio 2.0\data\StudioColorDefinition.txt` file to the root of the repo.

Create venv, activate it and launch `main.py`:

```bash
python -m venv venv
source venv/bin/activate
python main.py
```

This will generate `StudioColorDefinition_updated.txt`. Copy it to `C:\Program Files\Studio 2.0\data` and rename it to `StudioColorDefinition.txt`.

> Disclaimer: Colors are not mapped to their correct BrickLink/LDD codes and names. The purpose of this tool is to provide an accurate visual representation of the set when importing and rendering it.

## License

This project is licensed under the GPLv3 (see COPYING), because it
includes code adapted from
[python-ldraw](https://github.com/rienafairefr/python-ldraw)
(see `parser.py`), which is itself licensed under the GPLv3.
