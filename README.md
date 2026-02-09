# AFS - Android Flashing Shortcuts

A PyQt5-based GUI application for simplifying Android device flashing and debugging operations through ADB and Fastboot commands.

## Overview

AFS (Android Flashing Shortcuts) provides a user-friendly graphical interface for common Android device operations that typically require command-line knowledge. The tool streamlines tasks like installing APKs, flashing system images, unlocking bootloaders, and managing device partitions.

### I AM NOT RESPONSIBLE FOR BRICKED DEVICES, LOST DATA, WW3, YOUR HOUSE CATCHING FIRE OR ANYTHING ELSE! YOU ARE RESPONSIBLE FOR EVERY CLICK YOU MAKE

## Features

### USB Debugging
- Reboot device to different modes (system, recovery, bootloader, fastboot)
- Install APK files directly to connected devices

### Flashing & Sideloading
- ADB sideload for ROM installation
- Flash images to specific partitions (boot, recovery, system, vendor, vbmeta, userdata, super)
- Flash vbmeta with verification disabled

### Device Information
- Detect fastboot devices
- Retrieve detailed device information via getvar

### Boot Operations
- Reboot to various partitions from fastboot mode
- Temporarily boot images without flashing

### Partition Management
- Erase specific partitions
- Factory reset via userdata formatting

### Bootloader Operations
- Unlock bootloader (supports both modern and legacy methods)
- Relock bootloader

### Additional Tools
- Magisk installation via ADB sideload
- File browser for selecting images and packages

## Requirements
-Fastboot drivers

## Safety Features

- Confirmation dialogs for critical operations
- Process state checking to prevent concurrent operations
- Clear error messaging
- Real-time command output display

## Supported File Types

- `.zip` - ROM packages, updates
- `.img` - System images, boot images
- `.apk` - Android application packages

## Important Notes

⚠️ **Warning**: Flashing operations can potentially brick your device if performed incorrectly. Always ensure you have proper backups and understand the commands before executing them.

- Bootloader unlocking will erase all device data
- Only use images compatible with your specific device model
- Some operations require an unlocked bootloader
- Developer options and USB debugging must be enabled on your device

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

please no copy :(

## Disclaimer

This tool is provided as-is without warranty. The authors are not responsible for any damage to devices resulting from the use of this software. Users assume all risks associated with flashing operations.
