# Critical Firmware Runtime Fixes

> [!WARNING]
> Historical account of earlier board-migration work. Paths, build status, and
> keymap details below may no longer match the active repository. The custom
> board definitions under `modules/dao` remain authoritative.

## Problem: Firmware Built Successfully But Didn't Run

After flashing the firmware to both keyboard halves, they displayed "SETTINGS ERASE" on Bluetooth instead of running the keyboard application. The build succeeded without errors, but the firmware failed at runtime.

## Root Cause: Incorrect HWMv2 Devicetree Structure

The devicetree organization violated Zephyr 4.x Hardware Model v2 (HWMv2) requirements, preventing the firmware from initializing properly.

---

## Critical Fix #1: Devicetree Structure

### What Was Wrong:

**dao.dtsi (shared file) incorrectly contained:**
```c
/dts-v1/;  // Should NOT be in shared file!
#include <nordic/nrf52840_qiaa.dtsi>  // Should NOT be in shared file!

#include <dt-bindings/zmk/matrix_transform.h>

/ {
    model = "Dao";
    // ...
```

**dao_left_nrf52840.dts and dao_right_nrf52840.dts were missing:**
```c
// Missing /dts-v1/;
// Missing #include <nordic/nrf52840_qiaa.dtsi>

#include "../dao.dtsi"  // Only had this
```

### Why This Broke Firmware:

In Zephyr 4.x HWMv2 format:
- **Board-specific DTS files** must contain `/dts-v1/;` and SoC includes
- **Shared DTSI files** should contain only devicetree fragments (no headers)
- Violating this causes the firmware to fail hardware initialization at boot

### The Fix:

**config/boards/dao/dao.dtsi** - Now a proper fragment:
```c
/*
 * Copyright (c) 2021 Rafael Yumagulov
 * SPDX-License-Identifier: MIT
 */

#include <dt-bindings/zmk/matrix_transform.h>

/ {
    model = "Dao";
    // ... (rest of shared devicetree)
```

**config/boards/dao/dao_left/dao_left_nrf52840.dts** - Now complete:
```c
/*
 * Copyright (c) 2021 Rafael Yumagulov
 * SPDX-License-Identifier: MIT
 */

/dts-v1/;
#include <nordic/nrf52840_qiaa.dtsi>
#include "../dao.dtsi"

&kscan0 {
    col-gpios = /* ... */;
};
```

**config/boards/dao/dao_right/dao_right_nrf52840.dts** - Same pattern

---

## Critical Fix #2: Kconfig Architecture Configuration

### What Was Wrong:

Initial attempt removed too much from Kconfig files:
```conf
# Kconfig.defconfig was missing:
config SOC
config ARM
```

This caused build error: `ARCH not defined`

### Why This Was Needed:

Even in HWMv2 format, Zephyr requires Kconfig to define:
- **SOC**: Which SoC variant to build for
- **ARM**: Which CPU architecture to use

The `board.yml` provides *metadata*, but Kconfig drives the actual build.

### The Fix:

**config/boards/dao/dao_left/Kconfig.defconfig:**
```conf
if BOARD_DAO_LEFT

config BOARD
	default "dao_left"

config SOC
	default "nrf52840_qiaa"  # Required for SoC selection

config ARM
	default y  # Required for architecture

config ZMK_KEYBOARD_NAME
	default "Dao"

# ... rest of config
endif
```

**config/boards/dao/dao_right/Kconfig.defconfig:** Same pattern with "Dao Right"

---

## Critical Fix #3: Board Metadata

### What Was Added:

**config/boards/dao/dao_left/board.yml:**
```yaml
board:
  name: dao_left
  vendor: dao
  socs:
    - name: nrf52840
      variants:         # Added variant specification
        - name: qiaa    # Matches nrf52840_qiaa SoC
```

**config/boards/dao/dao_right/board.yml:** Same pattern

---

## Complete HWMv2 Board Structure

For each board (dao_left and dao_right), we now have:

```
config/boards/dao/
├── dao.dtsi                           # Shared devicetree fragment
├── dao_left/
│   ├── board.yml                      # HWMv2 metadata with variant
│   ├── dao_left_nrf52840.dts         # Complete DTS with /dts-v1/ + SoC include
│   ├── dao_left_nrf52840.defconfig   # Hardware config (from defconfig files)
│   ├── Kconfig.dao_left              # Board selection (depends on SOC)
│   ├── Kconfig.defconfig             # Board defaults (SOC + ARM configs)
│   └── board.cmake                   # Build system integration
└── dao_right/
    └── (same structure)
```

---

## Key Takeaways: HWMv2 Format Requirements

### ✅ Correct Pattern:

1. **board.yml**: Hardware metadata (name, vendor, SoC, variants)
2. **{board}_{soc}.dts**: Complete devicetree WITH `/dts-v1/;` and SoC include
3. **{board}.dtsi**: Shared fragments WITHOUT `/dts-v1/;` or SoC includes
4. **Kconfig.{board}**: Use `depends on SOC_*` not `select SOC_*`
5. **Kconfig.defconfig**: MUST set `config SOC` and `config ARM` defaults

### ❌ Common Mistakes:

- ❌ Putting `/dts-v1/;` in shared DTSI file
- ❌ Omitting `/dts-v1/;` from board DTS file
- ❌ Removing SOC/ARM configs from Kconfig.defconfig
- ❌ Using `select SOC_*` instead of `depends on` in Kconfig.board
- ❌ Omitting variant specification in board.yml

---

## Testing the Fix

After pushing these changes, GitHub Actions will build new firmware:
- `dao_left.uf2`
- `dao_right.uf2`

### Expected Behavior After Flashing:

**Before fix:**
- Left BLE name: "SETTINGS ERASE"
- Right BLE name: "SETTINGS ERASE"
- Keyboard didn't work

**After fix:**
- Left BLE name: "Dao"
- Right BLE name: "Dao Right"
- Full keyboard functionality with all 5 layers
- All combos and macros working

---

## Files Changed

### Devicetree Structure:
- `config/boards/dao/dao.dtsi` - Removed /dts-v1/ and SoC include
- `config/boards/dao/dao_left/dao_left_nrf52840.dts` - Added /dts-v1/ and SoC include
- `config/boards/dao/dao_right/dao_right_nrf52840.dts` - Added /dts-v1/ and SoC include

### Kconfig Configuration:
- `config/boards/dao/dao_left/Kconfig.dao_left` - Changed to `depends on`
- `config/boards/dao/dao_left/Kconfig.defconfig` - Restored SOC and ARM configs
- `config/boards/dao/dao_right/Kconfig.dao_right` - Changed to `depends on`
- `config/boards/dao/dao_right/Kconfig.defconfig` - Restored SOC and ARM configs

### Board Metadata:
- `config/boards/dao/dao_left/board.yml` - Added variant specification
- `config/boards/dao/dao_right/board.yml` - Added variant specification

---

## Commits Applied

1. **bb40a13** - Fix critical HWMv2 devicetree structure for Zephyr 4.x compatibility
2. **ef28590** - Restore ARM architecture config in Kconfig.defconfig
3. **e1793a3** - Add SOC config and variant specification for complete HWMv2 support

---

## Next Steps

1. **Push to GitHub**: `git push` to trigger firmware build
2. **Download firmware**: Get dao_left.uf2 and dao_right.uf2 from GitHub Actions
3. **Flash both halves**: Use UF2 bootloader to flash new firmware
4. **Verify**: Check BLE names show "Dao" and "Dao Right" (not "SETTINGS ERASE")
5. **Test**: Verify all layers, combos, and functionality work correctly

The firmware should now run properly! 🎉
