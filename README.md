# chrome-tabs-finder

Control Chrome from the command line.
Send commands by echoing to `tmp/chrometabsfinder.pipe`:
``` sh
echo -n '{"search":{"url":"https://mail.google.com/*"}}' > /tmp/chrometabsfinder.pipe
```

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
    ```
4. From Google Chrome again (from the tab we left open earlier):
    1. Click the loopy reload button in the bottom right corner of this extension
5. From your shell:
    ``` sh
    echo -n '{"search":{"url":"https://mail.google.com/*"}}' > /tmp/chrometabsfinder.pipe
    ```
    If you have a tab open to Gmail, it should now have focus.
