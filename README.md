# chrome-tabs-finder

Control Chrome from the command line.
Send commands by echoing to `tmp/chrometabsfinder.pipe`:
``` bash
echo -n '{"focus":{"url":"https://mail.google.com/*"}}' > /tmp/chrometabsfinder.pipe
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
    # replace ~/bin/ below with somewhere in your PATH
    ln -s $PWD/native-messaging-host/client.py ~/bin/chrome-client
    ```
4. From Google Chrome again (from the tab we left open earlier):
    1. Click the loopy reload button in the bottom right corner of this extension

5. From Google Chrome, for each Profile, separately:
    1. Navigate to the "Options" dialog for this extension ("puzzzle" button > Chrome Tabs Finder > ⠇ > Options)
    2. Set the profile name you want to use to select this profile

## Use

From your shell:
``` bash
chrome-client '{"focus":{"url":"https://mail.google.com/*"}}'
```
If you have a tab open to Gmail, it should now have focus.
