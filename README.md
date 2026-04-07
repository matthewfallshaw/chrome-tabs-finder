# chrome-tabs-finder

Find and focus Chrome tabs and windows from the command line. Supports multiple Chrome profiles.

``` bash
# Focus a tab by URL
chrome-client '{"focus": {"url": "*mail.google.com*"}}'

# Focus the window containing a tab, by title and profile
chrome-client '{"focusWindowContaining": {"title": "*Google Drive*", "profile": "work"}}'
```

## Commands

### `focus` — Focus a matching tab

``` bash
chrome-client '{"focus": {"url": "pattern", "title": "pattern"}}'
```

Finds the first tab matching the criteria, focuses it, and brings its window to the front.

### `focusWindowContaining` — Focus the window containing a matching tab

``` bash
chrome-client '{"focusWindowContaining": {"url": "pattern", "title": "pattern"}}'
```

Like `focus`, but brings the window to the front without switching to the matched tab.

### `getAllTabs` — List all open tabs

``` bash
chrome-client '"getAllTabs"'
```

### `help` — Show available commands

``` bash
chrome-client '"help"'
```

## Search criteria

Both `focus` and `focusWindowContaining` accept these search parameters:

| Parameter   | Description | Pattern type |
|-------------|-------------|--------------|
| `url`       | Match tab URL | Glob (`*` wildcards) |
| `title`     | Match tab title | Glob (`*` wildcards) |
| `not_url`   | Exclude tabs by URL | JavaScript regex |
| `not_title` | Exclude tabs by title | JavaScript regex |
| `profile`   | Only match in this Chrome profile | Exact match |

At least one of `url`, `title`, `not_url`, or `not_title` is required.

`profile` must match the name configured in the extension's options page for that Chrome profile (see installation step 5).

## Installation

1. From Google Chrome:
    1. `chrome://extensions/`
    2. Developer mode: ✓
    3. Load unpacked: (this directory)
    4. Find this extension which should now be added to your list of extensions
    5. Note this extension's `ID: <ID string>` (and leave this tab open)
2. Modify `native-messaging-host/com.matthewfallshaw.chrometabsfinder.json`:
    ``` json
    "allowed_origins": [
      "chrome-extension://<ID string>/"
    ]
    ```
3. From your shell:
    ``` bash
    ln -s $PWD/native-messaging-host/com.matthewfallshaw.chrometabsfinder.json ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/
    # replace ~/bin/ below with somewhere in your PATH
    ln -s $PWD/native-messaging-host/client.py ~/bin/chrome-client
    ```
4. From Google Chrome again (from the tab we left open earlier):
    1. Click the loopy reload button in the bottom right corner of this extension

5. From Google Chrome, for each Profile, separately:
    1. Navigate to the "Options" dialog for this extension ("puzzle" button > Chrome Tabs Finder > ⠇ > Options)
    2. Set the profile name you want to use to select this profile
