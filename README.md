# Android Flashing Shortcuts
##Moved from https://github.com/broke-tech/android-flashing-shortcuts-legacy
<img width="868" height="634" alt="Screenshot 2026-09-21 215622" src="https://github.com/user-attachments/assets/dbc676b2-bd24-4de6-b319-7f9cdc827f14" />
<img width="868" height="634" alt="Screenshot 2026-09-21 215607" src="https://github.com/user-attachments/assets/e1909f76-556a-47ff-a753-b54fc26efcef" />
<img width="868" height="634" alt="Screenshot 2026-09-21 215628" src="https://github.com/user-attachments/assets/5ee9ac63-3fe6-4144-821a-7aa9b6c8400c" />

Fastboot and ADB are great until you're on your fifth flash of the night, retyping the same commands and hoping you didn't typo a partition name.

I built Android Flashing Shortcuts (AFS) to fix that. It's a small GUI that wraps the commands you actually use, so you can click a button instead of digging through your terminal history.

## What it does

- Runs common ADB and fastboot commands from a simple window
- Shows you what's happening, so you're never guessing whether something worked
- Saves you from typing the same thing over and over
- Works with whatever device you're tinkering with
- You can also manage apps (including system apps) so you can debloat your device as much as you want

<!-- CHECK: replace or extend this list with the exact buttons/features in the app -->

## A quick word of caution

Flashing can brick a device. AFS makes the commands easier to run, not safer to run. Before you flash anything:

1. Make sure it's the right file for your exact device
2. Back up your data
3. Know how to get back to a working state if it goes wrong

You're responsible for what you flash. I'm just trying to save you some typing.

## Something broke?

Open an [issue](https://github.com/broke-tech/android-flashing-shortcuts/issues) and tell me:

- What you clicked
- What you expected to happen
- What happened instead (a screenshot or the output log helps a lot)
- Your OS and device

## Contributing

Pull requests and ideas are welcome. If you're planning something big, open an issue first so we don't step on each other's toes.

## Release notes

See [`releasenotes.json`](releasenotes.json) for what's changed between versions.

## License

MIT. See [LICENSE](LICENSE).
