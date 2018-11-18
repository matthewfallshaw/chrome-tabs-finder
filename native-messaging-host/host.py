#!/usr/bin/env python
# Copyright (c) 2012 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file [included below -- M@]
#
# Modified by Matthew Fallshaw, 2018-11-06

# A simple native messaging host.

import json
import logging
import os
import Queue
import struct
import sys
import threading
import time

PIPE_PATH = '/tmp/chrometabsfinder.pipe'
LOG_PATH = '/tmp/chrometabsfinder.log'

logging.basicConfig(filename=LOG_PATH, level=logging.DEBUG)


# Helper function that sends a message to the webapp.
def send_message(message):
    # Write message size.
    sys.stdout.write(struct.pack('I', len(message)))
    # Write the message itself.
    sys.stdout.write(message)
    sys.stdout.flush()


# Thread that reads messages from the webapp.
def read_thread_func(queue):
    while True:
        # Read the message length (first 4 bytes).
        text_length_bytes = sys.stdin.read(4)

        if len(text_length_bytes) == 0:
            logging.warning('Read 0 bytes from stdin; connection is closed, '
                            'so exiting.')
            queue.put(None)
            sys.exit(0)

        # Unpack message length as 4 byte integer.
        text_length = struct.unpack('i', text_length_bytes)[0]

        # Read the text (JSON object) of the message.
        text = sys.stdin.read(text_length).decode('utf-8')
        logging.debug("Read message: %s" % text)

        queue.put(text)


def Main():
    queue = Queue.Queue()

    thread = threading.Thread(target=read_thread_func, args=(queue,))
    thread.daemon = True
    thread.start()

    if not os.path.exists(PIPE_PATH):
        os.mkfifo(PIPE_PATH)
    # Open the fifo. We need to open in non-blocking mode or it will stalls
    # until someone opens it for writting
    pipe_fd = os.open(PIPE_PATH, os.O_RDONLY | os.O_NONBLOCK)
    with os.fdopen(pipe_fd) as pipe:
        logging.warning("Opening pipe; listening for messages.")
        while True:
            message = pipe.read()
            if message:
                try:
                    logging.debug("Sending message: %s" % json.loads(message))
                    send_message(json.dumps({"msg": json.loads(message)}))
                except Exception:
                    logging.debug("bad_msg: %s" % message)
            time.sleep(0.5)

    logging.warning('Exited the FIFO loop that should not exit; exiting the '
                    'daemon now?!')
    sys.exit(0)


if __name__ == '__main__':
    Main()


# Modified from
# https://chromium.googlesource.com/chromium/src/+/master/chrome/common/extensions/docs/examples/api/nativeMessaging/host/native-messaging-example-host
# Original LICENSE follows:
#
# Copyright 2015 The Chromium Authors. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#    * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#    * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
