# Dao Miryoku-Style Layer Access Guide

This guide documents the active `config/dao.keymap`. The diagrams use the
physical Dao order: six keys on each half per alpha row, then three thumb keys
per half. `·` means the key is unavailable on that layer.

## Layer access

| Layer | How to enter | Release/exit |
|---|---|---|
| BASE | Default | Always underneath other layers |
| NAV | Hold Space thumb, position 38 | Release Space |
| MOUSE | Hold Tab thumb, position 37 | Release Tab |
| MEDIA | Hold Escape thumb, position 36 | Release Escape |
| NUM | Hold Backspace thumb, position 39 | Release Backspace |
| SYM | Hold Enter thumb, position 40 | Release Enter |
| FUN | Hold Delete thumb, position 41 | Release Delete |
| BT | Hold thumb positions 36 and 41 together | Release either thumb |
| GAME | On BT, press the bottom-right outer key | Press bottom-right outer again |

## Thumb tap/hold behavior

```text
Left, outer -> inner                         Right, inner -> outer
Esc / MEDIA    Tab / MOUSE    Space / NAV   Bspc / NUM    Enter / SYM    Del / FUN
position 36    position 37    position 38   position 39   position 40    position 41
```

## Home-row modifiers

```text
GUI/A  Alt/R  Ctrl/S  Shift/T  G   || M  Shift/N  Ctrl/E  Alt/I  GUI/O
```

The hold-taps only use the opposite hand as a positional hold trigger. Fast
same-hand rolls are biased toward letters rather than accidental modifiers.

## Six outer-column keys

Most momentary layers use transparent outer bindings, so these BASE fallbacks
remain available:

```text
Tab       ... alpha row ...       Backspace
Left Ctrl ... home row  ...       Enter
Left Shift... bottom row...       Delete
```

NAV changes bottom-right Delete to Repeat. SYM, GAME, and BT deliberately
override outer keys as shown below.

## BASE - Colemak-DH

```text
Tab   | Q       W       F       P       B     || J       L       U       Y       '       | Bspc
LCtrl | GUI/A   Alt/R   Ctrl/S  Shift/T G     || M       Shift/N Ctrl/E  Alt/I   GUI/O   | Enter
LShft | Z       X       C       D       V     || K       H       ,       .       /       | Del

              Esc/Media  Tab/Mouse  Space/Nav || Bspc/Num  Enter/Sym  Del/Fun
```

## NAV - navigation and editing

```text
Tab   | ·     ·     ·     ·     ·     || Insert   Home    Up      End     PgUp | Bspc
LCtrl | GUI   Alt   Ctrl  Shift ·     || CapsWord Left    Down    Right   PgDn | Enter
LShft | ·     RAlt  ·     ·     ·     || Redo     Paste   Copy    Cut     Undo | Repeat

                    ·     ·     ·     || Bspc     Enter   Del
```

Clipboard outputs are Ctrl+Y, Ctrl+V, Ctrl+C, Ctrl+X, and Ctrl+Z. Hold a
left-hand modifier on NAV while pressing a right-hand navigation key to create
modified navigation chords.

## NUM - numbers

```text
Tab   | [     7     8     9     ]     || ·       ·       ·       ·       ·   | Bspc
LCtrl | ;     4     5     6     =     || ·       Shift   Ctrl    Alt     GUI | Enter
LShft | `     1     2     3     \     || ·       ·       ·       RAlt    ·   | Del

                    .     0     -     || ·       ·       ·
```

## SYM - programming symbols

```text
~     | [     {     (     <     +     || !       @       #       $       ^   | '
`     | ]     }     )     >     =     || ·       Shift   Ctrl    Alt     GUI | "
|     | \     /     *     &     %     || ·       ·       ·       RAlt    ·   | :

                    _     -     ;     || ·       ·       ·
```

Bracket and operator pairs are vertical. Symbol output assumes the host uses a
US ANSI keyboard layout.

## FUN - function and system keys

```text
Tab   | F12   F7    F8    F9    PrtSc || ·       ·       ·       ·       ·   | Bspc
LCtrl | F11   F4    F5    F6    ScrLk || ·       Shift   Ctrl    Alt     GUI | Enter
LShft | F10   F1    F2    F3    Pause || ·       ·       ·       RAlt    ·   | Del

                    App   Space Tab   || ·       ·       ·
```

## MEDIA

```text
Tab   | ·     ·     ·     ·     ·     || ·       ·       VolUp   ·       ·   | Bspc
LCtrl | GUI   Alt   Ctrl  Shift ·     || ·       Prev    VolDn   Next    ·   | Enter
LShft | ·     RAlt  ·     ·     ·     || ·       ·       ·       ·       ·   | Del

                    ·     ·     ·     || Stop    Play    Mute
```

## MOUSE

```text
Tab   | ·     ·     ·     ·     ·     || ·       WheelL  MouseUp WheelR  WheelUp | Bspc
LCtrl | GUI   Alt   Ctrl  Shift ·     || ·       MouseL  MouseDn MouseR  WheelDn | Enter
LShft | ·     RAlt  ·     ·     ·     || Redo    Paste   Copy    Cut     Undo    | Del

                    ·     ·     ·     || Button2 Button1 Button3
```

These are ZMK-generated mouse reports. The keyboard has no physical pointing
device and this configuration does not add one.

## GAME - plain QWERTY

```text
Esc   | Q     W     E     R     T     || Y       U       I       O       P   | Bspc
Ctrl  | A     S     D     F     G     || H       J       K       L       ;   | Enter
Shift | Z     X     C     V     B     || N       M       ,       .       /   | Exit

                    GUI   Alt   Space || Space   RAlt    RCtrl
```

GAME is toggled, not momentary. Its bottom-right outer key is always the direct
exit. BT is intentionally the highest layer, so the BT chord still works while
GAME is active.

## BT - Bluetooth, recovery, and GAME entry

```text
Boot  | ·     ·     ·     ·     ·     || ·       ·       ·       ·       ·   | ·
Clear | Sel0  Sel1  Sel2  Sel3  Sel4  || Sel4    Sel3    Sel2    Sel1    Sel0| Clear
Reset | ·     ·     ·     ·     ·     || ·       ·       ·       ·       ·   | GAME

                    ·     ·     ·     || ·       ·       ·
```

Keep both outer thumbs held while selecting a BT action:

- `Sel0`-`Sel4` selects one of five host profiles.
- `Clear` clears the selected host profile.
- `Boot` enters the central half's UF2 bootloader.
- `Reset` resets the firmware.
- `GAME` toggles the QWERTY gaming layer.

For a new host, choose an unused profile and pair with `Dao`. `Dao Right` is the
split peripheral, not the host-facing keyboard. Use the right half's physical
double-reset action when its bootloader is needed.

## Combos

| Physical positions | Active layers | Result | Timeout |
|---|---|---|---:|
| 36 + 41 | BASE, GAME | Momentary BT layer | 50 ms |

There are no alpha-key combos, avoiding conflicts with Colemak-DH rolls. Escape
is a thumb tap and Caps Word is a NAV key.

## Recovery and initial testing

Do not flash firmware unless both `dao_left` and `dao_right` GitHub Actions jobs
have passed. For a verified keymap-only build, test `dao_left.uf2` first because
the left central interprets the shared keymap. A physical double-reset always
provides the UF2 recovery path, and the previous keymap remains available in Git
history.
