#!/usr/bin/env python
# Copyright (c) 2018 Matthew Fallshaw. All rights reserved.
# Use of this source code is governed by the MIT license, which can be
# found at the end of this file.

# A simnple client that communicates with a simple native messaging host.

import errno
import glob
import json
import os
import sys
import time
import threading
from typing import List

BASE_PATH = '/tmp/'
PIPE_PATTERN = BASE_PATH + 'chrometabsfinder.*.pipe'
REPLY_TIMEOUT = 60  # seconds
PIPE_READ_WAIT = 0.1


class TimeoutError(Exception):
    pass


def converse_with_host(message: str, pipe_name: str) -> None:
    # Parse message
    try:
        json.loads(message)
    except ValueError:
        message = json.dumps(message)

    # Send to host then wait for reply
    pipe = get_pipe(pipe_name, os.O_WRONLY)
    try:
        send_to_host(message.encode(), pipe)
    except OSError as e:
        if e.errno == errno.EPIPE:
            pass
        else:
            raise
    # reply = read_from_host(pipe)
    # pipe.close()

    # Return reply to stdout
    # sys.stdout.write(reply)
    # sys.stdout.flush()

    return


# Helper function that sends a message to all running instances of the host.
def send_to_host(message: bytes, pipe: int) -> None:
    os.write(pipe, message)


def read_from_host(pipe: int) -> str:
    while True:
        message = os.read(pipe, 1024)
        if message:
            break
        time.sleep(PIPE_READ_WAIT)
    return message.decode()


def get_pipe(pipe_name: str, mode: int) -> int:
    return os.open(pipe_name, mode | os.O_NONBLOCK)


def join_all(threads: List[threading.Thread], timeout: int) -> None:
    """
    Args:
        threads: a list of thread objects to join
        timeout: the maximum time to wait for the threads to finish
    Raises:
        RuntimeError: if not all the threads have finished by the timeout
    """
    start_time = time.time()
    while time.time() <= (start_time + timeout):
        for thread in threads:
            if thread.is_alive():
                thread.join(timeout=0)
        if all(not t.is_alive() for t in threads):
            break
        time.sleep(PIPE_READ_WAIT)
    else:
        still_running = [t for t in threads if t.is_alive()]
        num = len(still_running)
        names = [t.name for t in still_running]
        raise TimeoutError('Timeout on {0} threads: {1}'.format(num, names))


def show_help():
    help_text = """chrome-client - Control Chrome tabs from the command line

USAGE:
    chrome-client '{"focus": {"url": "pattern", "title": "pattern", "profile": "name"}}'
    chrome-client '{"focusWindowContaining": {"url": "pattern", "title": "pattern", "profile": "name"}}'
    chrome-client '"getAllTabs"'
    chrome-client '"help"'

COMMANDS:
    focus                    Focus a tab matching the criteria
    focusWindowContaining    Focus the window containing a tab matching the criteria
    getAllTabs              Get information about all open tabs
    help                    Show available commands from the extension

SEARCH CRITERIA:
    url       URL pattern (wildcards supported: *gmail.com*, https://example.com/*)
    title     Title pattern (wildcards supported: *Google Drive*, My Document*)  
    profile   Chrome profile name (must match name set in extension options)

EXAMPLES:
    # Focus Gmail tab in any profile
    chrome-client '{"focus": {"url": "*gmail.com*"}}'
    
    # Focus Google Drive tab in specific profile  
    chrome-client '{"focus": {"url": "*drive.google.com*", "profile": "work"}}'
    
    # Focus window containing a specific document
    chrome-client '{"focusWindowContaining": {"title": "*My Document*"}}'
    
    # Get all tabs
    chrome-client '"getAllTabs"'

SETUP:
    1. Install Chrome extension and configure profile names in extension options
    2. Make sure native messaging host is running (loads automatically with extension)
    3. Ensure this script is in your PATH as 'chrome-client'
"""
    print(help_text)

def Main():
    args = sys.argv[1:]
    
    if not args or args[0] in ['-h', '--help']:
        show_help()
        sys.exit(0)
    
    message = ' '.join(args)

    chrome_host_threads = []
    for pipe_name in glob.glob(PIPE_PATTERN):
        thread = threading.Thread(target=converse_with_host,
                                  args=(message, pipe_name))
        thread.daemon = True
        thread.start()
        chrome_host_threads.append(thread)

    # Timeout if any threads fail to return
    try:
        join_all(chrome_host_threads, REPLY_TIMEOUT)
    except TimeoutError:
        pass
    sys.exit()


if __name__ == '__main__':
    Main()


# MIT License

# Copyright (c) 2018 Matthew Fallshaw

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
