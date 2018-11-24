#!/usr/bin/env python
# Copyright (c) 2018 Matthew Fallshaw. All rights reserved.
# Use of this source code is governed by the MIT license, which can be
# found at the end of this file.

# A simnple client that communicates with a simple native messaging host.

import errno
import glob
import os
import sys

BASE_PATH = '/tmp/'
PIPE_PATTERN = BASE_PATH + 'chrometabsfinder.*.pipe'


# Helper function that sends a message to all running instances of the host.
def send_to_hosts(message):
    for pipe_name in glob.glob(PIPE_PATTERN):
        try:
            pipe = os.open(pipe_name, os.O_WRONLY | os.O_NONBLOCK)
        except OSError as exc:
            if exc.errno == errno.ENXIO:
                pipe = None
            else:
                raise
        if pipe is not None:
            try:
                os.write(pipe, message)
            except OSError as exc:
                if exc.errno == errno.EPIPE:
                    pass
                else:
                    raise
            os.close(pipe)


def Main():
    # import pdb; pdb.set_trace()
    send_to_hosts(' '.join(sys.argv[1:]))


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
