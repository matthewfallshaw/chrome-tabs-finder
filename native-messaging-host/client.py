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

BASE_PATH = '/tmp/'
PIPE_PATTERN = BASE_PATH + 'chrometabsfinder.*.pipe'
REPLY_TIMEOUT = 60  # seconds
PIPE_READ_WAIT = 0.1


class TimeoutError(StandardError):
    pass


def converse_with_host(message, pipe_name):
    # Parse message
    try:
        json.loads(message)
    except ValueError:
        message = json.dumps(message)

    # Send to host then wait for reply
    pipe = get_pipe(pipe_name, os.O_WRONLY)
    try:
        send_to_host(message, pipe)
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
def send_to_host(message, pipe):
    os.write(pipe, message)


def read_from_host(pipe):
    while True:
        message = pipe.read()
        if message:
            break
        time.sleep(PIPE_READ_WAIT)
    return message


def get_pipe(pipe_name, mode):
    return os.open(pipe_name, mode | os.O_NONBLOCK)


def join_all(threads, timeout):
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


def Main():
    message = ' '.join(sys.argv[1:])

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
