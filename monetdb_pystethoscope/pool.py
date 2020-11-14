# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

"""Keeping a cache of stethoscope files. The files are compressed in the background and removed when the retention
period expires"""
import gzip
import time
import shutil
import os
from os import path
import json
import signal
from multiprocessing import Process

class StethoscopePool:
    retention = 1       # keep the logs around for 1 hour
    interval = 5        # create new file every so many minutes
    logdir = "./logs/"  # directory must exist before being used
    dbname = None
    timestamp = time.time()
    tag = None
    logfile = None      # Current log file

    def __init__(self, logdir, dbname, interval, retention):
        # remember the log template
        if not dbname or not logdir:
            raise ValueError
        self.dbname = dbname
        self.logdir = logdir
        # check existance of the log directory
        if not path.exists(logdir):
            print('Log pool directory non-existing', logdir, ' Create it first')
            exit(0)
        print('Using log pool interval', interval, ' seconds with file retention', retention, 'hours')
        self.retention = retention
        self.interval = interval
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        print('Interrupt received', signum, frame)
        if self.logfile:
            self.logfile.close()
            self.pool_cleanup()
            self.pool_process()
            self.logfile = None
        exit(0)

    def pool_switch(self):
        # check if the interval has passed and a new file is needed
        if not self.dbname or not self.logdir:
            raise ValueError
        lt = time.time()
        if not self.logfile or lt >= self.timestamp + self.interval * 60:
            if self.logfile:
                self.logfile.close()
                self.pool_cleanup()
                self.pool_process()
            self.timestamp = lt
            self.tag = self.logdir + self.dbname + '_' + time.strftime("%y-%m-%dT%H:%M:%S", time.localtime(lt))
            try:
                self.logfile = open(self.tag, "w")
            except IOError:
                print('Could not open the log file', self.tag)

    def pool_record(self, json_obj):
        # Move the json string to the latest log file
        self.pool_switch()
        if self.logfile:
            self.logfile.write(json.dumps(json_obj))
            self.logfile.write('\n')
            # self.logfile.flush()  may be too often given the speed of events arriving

    def pool_cleanup(self):
        # remove all files whose retention have passed
        files = os.listdir(self.logdir)
        lt = time.time()
        lt = lt - self.retention * 3600
        tag = self.logdir + self.dbname + '_' + time.strftime("%y-%m-%dT%H:%M:%S", time.localtime(lt))
        for f in files:
            if f < tag and f != self.tag:
                print('consider %s for removal' % f)

    @staticmethod
    def pool_compress(tag):
        with open(tag, 'rb') as f_in:
            with gzip.open(tag + '.gz', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                os.remove(tag)

    def pool_process(self):
        # Start compressing the latest log file in the background
        p = Process(target=StethoscopePool.pool_compress, args=self.tag)
        p.start()
