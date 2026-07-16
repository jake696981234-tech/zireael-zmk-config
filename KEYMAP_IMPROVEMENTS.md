# Dao Keymap Improvements

> [!WARNING]
> Historical notes for the previous personalised keymap. Do not copy
> `config/dao.keymap.improved` over the active keymap: that snapshot is not a
> current build input and contains stale assumptions and positions. See
> `README.md` and `LAYER_ACCESS_GUIDE.md` for the active layout.

## 🎯 Key Improvements Made

### 1. **Combo Keys Added** ⚡
Makes frequently used keys easier to reach without leaving home position:

| Combo | Keys | Action | Benefit |
|-------|------|--------|---------|
| `Q+W` | Adjacent top row | ESC | No need to reach for ESC key |
| `A+S` | Home row | Caps Word | Better than CAPSLOCK - auto-disables after word |
| `Both outer thumbs` | Thumb cluster | BTL layer | Quick access to Bluetooth settings |
| `F+P` | Top row | Screenshot (⌘⇧4) | macOS screenshot shortcut |
| `F+P` on RSE | Top row | TAB | Quick tab in VSCode layer |

**Why combos?**
- Reduces finger travel
- Keeps hands on home position
- Faster than reaching for dedicated keys

### 2. **Fixed Number Keys** 🔢

**Before:**
```c
&kp KP_NUMBER_1  // Keypad numbers - may not work in all apps
```

**After:**
```c
&kp N1  // Regular numbers - work everywhere
```

**Why:** KP_NUMBER keys (numpad) don't work in many applications. Regular number keys (N1-N9, N0) are universal.

### 3. **Caps Word Instead of CAPSLOCK** 🔤

**Before:** `&kp CAPSLOCK` - Toggle that stays on forever

**After:** `&caps_word` - Smart capitalization that:
- Automatically capitalizes the next word
- Auto-disables after typing the word
- Works with `-` and `_` (for SNAKE_CASE, kebab-case)
- Prevents accidentally leaving CAPS on

**Access:**
- Combo: `A+S` (home row)
- Or: FUN layer, left side position

### 4. **Key Repeat Added** 🔁

**Location:** Bottom right corner (replaced `&sl FUN`)

**What it does:** Repeats the last key pressed
- Great for navigation (arrow keys)
- Useful for repeated characters (`====`, `----`)
- Saves having to hold keys

### 5. **Better Layer Access** 🎛️

**BTL Layer Access Improved:**

**Before:**
- Hold LWR (Space)
- Press bottom-left key
- Requires two deliberate actions

**After:**
- Press both outer thumb keys together
- Works from DEF, LWR, or RSE layers
- Much faster for Bluetooth management

### 6. **Optimized Timing** ⏱️

```c
&lt {
    flavor = "balanced";  // Better tap/hold distinction
    require-prior-idle-ms = <150>;  // Prevents accidental holds
};
```

**Benefits:**
- More reliable tap vs hold detection
- Fewer accidental layer activations
- Smoother typing experience

### 7. **Visual Layout** 🎨

Added ASCII art grid to make keymap easier to read and maintain:

```c
// ╭─────┬─────┬─────╮   ╭─────┬─────┬─────╮
    &kp Q &kp W &kp E     &kp R &kp T &kp Y
// ├─────┼─────┼─────┤   ├─────┼─────┼─────┤
```

Makes it easy to see:
- Key positions
- Left/right split
- Alignment issues

## 📊 Layer Structure Comparison

### Original:
```
DEF → Base
├─ LWR (hold Space) → Symbols
├─ RSE (hold Backspace) → VSCode
├─ FUN (LWR+RSE OR sticky) → Functions
└─ BTL (mo from LWR) → Bluetooth
```

### Improved:
```
DEF → Base + Combos
├─ LWR (hold Space) → Symbols (fixed numbers!)
├─ RSE (hold Backspace) → VSCode
├─ FUN (LWR+RSE) → Functions (added caps_word)
└─ BTL (combo: both outer thumbs) → Bluetooth (easier access!)
```

## 🎮 How to Use the Improvements

### Combos:
1. **ESC** - Press Q+W together instead of reaching for ESC
2. **Caps Word** - Press A+S to capitalize next word
3. **BTL Layer** - Press both outer thumb keys (Control + Shift positions)
4. **Screenshot** - Press F+P on base layer for ⌘⇧4

### Key Repeat:
- Bottom right corner (where sticky FUN layer was)
- Press to repeat last key
- Great after arrow keys or symbols

### Caps Word:
- Combo: A+S
- Or: FUN layer position (where CAPSLOCK was)
- Types next word in CAPS, then auto-disables
- Much better than CAPSLOCK!

## 🔄 Migration Guide

### Option 1: Use Improved Version (Recommended)
```bash
cp config/dao.keymap config/dao.keymap.backup
cp config/dao.keymap.improved config/dao.keymap
```

### Option 2: Add Improvements Gradually

Start with just the combos:
1. Add the combo definitions
2. Test for a few days
3. Add caps_word
4. Add key_repeat
5. Fix numbers last (least critical)

## 🆚 Side-by-Side Comparison

| Feature | Original | Improved |
|---------|----------|----------|
| **Numbers** | KP_NUMBER (numpad) | N1-N0 (regular) |
| **Caps** | CAPSLOCK (toggle) | caps_word (smart) |
| **ESC Access** | Dedicated key | Q+W combo |
| **BTL Access** | mo from LWR | Combo (both thumbs) |
| **Key Repeat** | ❌ None | ✅ Bottom right |
| **Visual Layout** | Plain text | ASCII art grid |
| **Layer Feel** | Good | Optimized timings |

## 💡 Pro Tips

1. **Learn combos gradually** - Start with ESC (Q+W), it's the most useful
2. **Use caps_word** for typing constants: `MY_CONSTANT` → auto-disables after
3. **BTL combo** makes switching devices much faster
4. **Key repeat** is great after ← → ↑ ↓ on RSE layer
5. **Regular numbers** on LWR now work in all apps (Slack, browsers, etc.)

## 🎯 What Wasn't Changed

- Layer structure (still 5 layers)
- VSCode macros (all preserved)
- Colemak-DH layout (untouched)
- Thumb cluster layout (same positions)
- Conditional layer (LWR+RSE = FUN)

All your muscle memory is preserved - these are **pure additions**!

## 🚀 Next Steps

1. Review the improved keymap: `config/dao.keymap.improved`
2. Test locally or push to GitHub to build
3. Flash and try combos
4. Adjust combo timing if needed (`timeout-ms = <50>`)
5. Add your own combos for frequently used shortcuts!

## 📝 Notes

- All improvements are **optional**
- You can mix and match features
- Original keymap is still excellent
- These are refinements based on ZMK best practices
