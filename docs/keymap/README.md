# Dao keymap visual reference

These diagrams are generated from the active [`config/dao.keymap`](../../config/dao.keymap),
using the 42-key physical order in `modules/dao/boards/dao/dao.dtsi` and the
terminology in [`LAYER_ACCESS_GUIDE.md`](../../LAYER_ACCESS_GUIDE.md).

- [`dao-primary.svg`](dao-primary.svg) contains BASE, NAV, NUM, and SYM.
- [`dao-secondary.svg`](dao-secondary.svg) contains FUN, MEDIA, MOUSE, GAME, and BT.

The large centered legend on a key is its tap action. Text along the bottom is
its hold or layer action. Blue keys show the key held to activate the displayed
layer. Faded, dashed keys inherit the displayed action from BASE; an empty key
has no action on that layer.

The BT chord joins physical thumb positions 36 and 41. Hold both keys from BASE
or GAME to use the momentary BT layer. Symbol labels assume a US ANSI host
keyboard layout.

## Regenerate

From the repository root, install the pinned documentation dependency and run
the generator:

```shell
python -m pip install -r requirements-keymap.txt
python tools/render_keymap.py
```

The script validates the layer count, 42 bindings per layer, physical Dao
transform, thumb positions, combo, and human-readable behavior labels before
writing the normalized YAML and both SVGs. `dao-keymap.yaml` is generated for
reviewability and must not be edited by hand.
