# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Chrome Tabs Finder is a Chrome extension that allows command-line control of Chrome tabs. It consists of:
- Chrome extension (manifest v3) with service worker and options page
- Python native messaging host that creates named pipes for IPC
- Python client for sending commands from command line

## Architecture

### Chrome Extension Components
- **background_scripts/background.js**: Service worker with main extension logic, handles tab finding/focusing, connects to native host via `chrome.runtime.connectNative()`
- **pages/options.html + options.js**: Configuration UI for setting profile names
- **manifest.json**: Extension manifest v3 with permissions for tabs, nativeMessaging, storage

### Native Messaging Host
- **native-messaging-host/host.py**: Creates named pipes (`/tmp/chrometabsfinder.PID.pipe`), bridges between client and Chrome extension
- **native-messaging-host/client.py**: Command-line client that writes to named pipes
- **native-messaging-host/com.matthewfallshaw.chrometabsfinder.json**: Native messaging host configuration

### Communication Flow
1. Client sends JSON command to named pipe
2. Host reads from pipe and forwards to Chrome extension via native messaging
3. Extension processes command (focus tab, get tabs, etc.) and sends reply
4. Host forwards reply back through pipe

## Development Commands

```bash
# Linting
npx eslint background_scripts/background.js

# Testing (basic structure exists)
npm test
```

## Key APIs and Commands

### Supported Commands
- `{"focus": {"url": "pattern", "title": "pattern"}}` - Focus matching tab
- `{"focusWindowContaining": {"url": "pattern", "title": "pattern"}}` - Focus window containing matching tab  
- `"getAllTabs"` - Get all open tabs
- `"help"` - Show available commands

### Profile System
Extension supports multiple Chrome profiles via `chrome.storage.sync` with profile names set in options page.

## Installation Requirements

1. Load unpacked extension in Chrome
2. Update `com.matthewfallshaw.chrometabsfinder.json` with extension ID
3. Symlink native messaging host config to `~/Library/Application Support/Google/Chrome/NativeMessagingHosts/`
4. Symlink `client.py` to PATH as `chrome-client`

## File Patterns
- JavaScript follows Standard style (`.eslintrc.json` extends "standard")
- Python files use type hints where available
- All communication uses JSON messaging protocol