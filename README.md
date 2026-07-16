# ZMK Firmware for the Dao/Zireael Keyboard

This repository builds ZMK firmware for a custom 42-key wireless split keyboard
using two nRF52840 controllers. The left half is the USB/Bluetooth central and
the right half is a Bluetooth peripheral. The custom hardware definitions,
battery monitoring, sleep support, and UF2 bootloader layout live under
`modules/dao`.

The active keymap is `config/dao.keymap`. It uses a Windows-oriented,
Miryoku-style architecture with Colemak-DH alphas, mirrored home-row modifiers,
six thumb layer-taps, and six outer-column fallback keys. The complete usage
reference is also available in [LAYER_ACCESS_GUIDE.md](LAYER_ACCESS_GUIDE.md).
Printable visual references are available for the
[primary layers](docs/keymap/dao-primary.svg) and
[secondary layers](docs/keymap/dao-secondary.svg).

## Build stability

Both the West manifest and reusable GitHub workflow are pinned to ZMK commit
`354cff9c36b49eee6abbb8a61e6b927539aebbf2`. This is the revision used by the
repository's last known successful build on January 28, 2026. Do not change the
pin casually: following ZMK's moving `main` branch previously allowed the same
repository commit to fail without a source change.

GitHub Actions builds both targets:

- `dao_left` -> `dao_left.uf2`
- `dao_right` -> `dao_right.uf2`

Only treat firmware as flashable after both jobs pass in GitHub Actions.

## Physical conventions

Every diagram is shown in the Dao's physical binding order: 12 keys per alpha
row followed by six thumb keys. `·` means unavailable on that layer.

Unless a layer explicitly overrides them, the six outer-column keys fall
through to these BASE functions:

```text
Left outer column:  Tab / Left Ctrl / Left Shift
Right outer column: Backspace / Enter / Delete
```

## BASE

```text
Tab   | Q       W       F       P       B     || J       L       U       Y       '       | Bspc
LCtrl | GUI/A   Alt/R   Ctrl/S  Shift/T G     || M       Shift/N Ctrl/E  Alt/I   GUI/O   | Enter
LShft | Z       X       C       D       V     || K       H       ,       .       /       | Del

              Esc/Media  Tab/Mouse  Space/Nav || Bspc/Num  Enter/Sym  Del/Fun
```

Home-row modifiers use opposite-hand positional triggers. They are
tap-preferred with a 200 ms tapping term, 175 ms quick-tap window, 150 ms
prior-idle guard, and `hold-trigger-on-release`.

| Key | Tap | Hold |
|---|---|---|
| A | A | GUI |
| R | R | Alt |
| S | S | Ctrl |
| T | T | Shift |
| N | N | Shift |
| E | E | Ctrl |
| I | I | Alt |
| O | O | GUI |

| Position | Tap | Hold |
|---:|---|---|
| 36 | Escape | MEDIA |
| 37 | Tab | MOUSE |
| 38 | Space | NAV |
| 39 | Backspace | NUM |
| 40 | Enter | SYM |
| 41 | Delete | FUN |

## NAV

Hold the Space thumb. Clipboard shortcuts use Windows/Linux Ctrl bindings.
Caps Word is on the physical `M` position; Repeat is the bottom-right outer key.

```text
Tab   | ·     ·     ·     ·     ·     || Insert   Home    Up      End     PgUp | Bspc
LCtrl | GUI   Alt   Ctrl  Shift ·     || CapsWord Left    Down    Right   PgDn | Enter
LShft | ·     RAlt  ·     ·     ·     || Redo     Paste   Copy    Cut     Undo | Repeat

                    ·     ·     ·     || Bspc     Enter   Del
```

## NUM

Hold the Backspace thumb.

```text
Tab   | [     7     8     9     ]     || ·       ·       ·       ·       ·   | Bspc
LCtrl | ;     4     5     6     =     || ·       Shift   Ctrl    Alt     GUI | Enter
LShft | `     1     2     3     \     || ·       ·       ·       RAlt    ·   | Del

                    .     0     -     || ·       ·       ·
```

## SYM

Hold the Enter thumb. The left-hand layout uses vertical pairs for brackets and
operators; the right home row remains available for modifiers.

```text
~     | [     {     (     <     +     || !       @       #       $       ^   | '
`     | ]     }     )     >     =     || ·       Shift   Ctrl    Alt     GUI | "
|     | \     /     *     &     %     || ·       ·       ·       RAlt    ·   | :

                    _     -     ;     || ·       ·       ·
```

Symbols assume a US ANSI host keyboard layout.

## FUN

Hold the Delete thumb.

```text
Tab   | F12   F7    F8    F9    PrtSc || ·       ·       ·       ·       ·   | Bspc
LCtrl | F11   F4    F5    F6    ScrLk || ·       Shift   Ctrl    Alt     GUI | Enter
LShft | F10   F1    F2    F3    Pause || ·       ·       ·       RAlt    ·   | Del

                    App   Space Tab   || ·       ·       ·
```

## MEDIA

Hold the Escape thumb.

```text
Tab   | ·     ·     ·     ·     ·     || ·       ·       VolUp   ·       ·   | Bspc
LCtrl | GUI   Alt   Ctrl  Shift ·     || ·       Prev    VolDn   Next    ·   | Enter
LShft | ·     RAlt  ·     ·     ·     || ·       ·       ·       ·       ·   | Del

                    ·     ·     ·     || Stop    Play    Mute
```

## MOUSE

Hold the Tab thumb. These are generated mouse keys; no pointing hardware is
enabled or required.

```text
Tab   | ·     ·     ·     ·     ·     || ·       WheelL  MouseUp WheelR  WheelUp | Bspc
LCtrl | GUI   Alt   Ctrl  Shift ·     || ·       MouseL  MouseDn MouseR  WheelDn | Enter
LShft | ·     RAlt  ·     ·     ·     || Redo    Paste   Copy    Cut     Undo    | Del

                    ·     ·     ·     || Button2 Button1 Button3
```

## GAME

GAME is plain QWERTY with direct modifiers and no home-row hold-taps. Enter it
through BT and the bottom-right outer key. Exit by pressing that bottom-right
outer key directly.

```text
Esc   | Q     W     E     R     T     || Y       U       I       O       P   | Bspc
Ctrl  | A     S     D     F     G     || H       J       K       L       ;   | Enter
Shift | Z     X     C     V     B     || N       M       ,       .       /   | Exit

                    GUI   Alt   Space || Space   RAlt    RCtrl
```

## Bluetooth and system controls

Hold physical thumb positions 36 and 41 together, then press a BT-layer key
while continuing to hold both thumbs. This is the only combo in the keymap and
is active from BASE and GAME.

```text
Boot  | ·     ·     ·     ·     ·     || ·       ·       ·       ·       ·   | ·
Clear | Sel0  Sel1  Sel2  Sel3  Sel4  || Sel4    Sel3    Sel2    Sel1    Sel0| Clear
Reset | ·     ·     ·     ·     ·     || ·       ·       ·       ·       ·   | GAME

                    ·     ·     ·     || ·       ·       ·
```

To pair a new computer or phone:

1. Hold both outer thumb keys.
2. Select an unused profile from 0-4.
3. Pair with `Dao` on the host. Do not pair the host with `Dao Right`.
4. If a slot is occupied, select it and use either Clear key before pairing.

Bootloader, reset, and GAME require the deliberate BT-layer chord. The
bootloader behavior acts on the central half; use the right half's physical
double-reset action to enter its UF2 bootloader.

## Changing, building, and flashing

1. Edit `config/dao.keymap`.
2. Commit and push the branch to trigger `.github/workflows/build.yml`.
3. Confirm both board jobs pass.
4. Download and extract the `firmware` artifact.
5. For a keymap-only test, flash `dao_left.uf2` first because the left half is
   the central that interprets the shared keymap.
6. Only flash `dao_right.uf2` when its firmware or shared board configuration
   also needs updating.

To flash a half, connect it by USB-C, double-press its physical reset button,
and copy the matching UF2 file to the mounted bootloader drive. A final file
transfer warning can be harmless if the drive disconnects after accepting the
firmware.

## Miryoku adaptation notes

This keymap was designed using the official Miryoku ZMK repository as a
read-only reference. It adapts Miryoku's hold-taps, opposite-hand layers,
number/function organization, mouse behavior, and thumb concepts to the Dao's
native 42-key matrix rather than importing a Corne shield or Miryoku build
system.

Differences from standard Miryoku include:

- Six dedicated outer-column fallback keys.
- Dao-specific physical thumb ordering.
- A programming-complete SYM layer.
- Separate BT and plain-QWERTY GAME layers.
- No Extra, Tap, or Button layers and no RGB, display, encoder, sensor, or
  physical pointing-device support.
- Windows clipboard shortcuts instead of macOS Command shortcuts.

The `*.improved`, `*.pre_improvements`, and `*.original_backup` keymap files are
historical snapshots only. They are not build inputs and may contain stale or
invalid positions. The active source of truth is always `config/dao.keymap`.
