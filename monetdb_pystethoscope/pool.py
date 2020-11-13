# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

"""Keeping a cache of stethoscope files"""
import gzip
import time
import shutil
import os


class StethoscopePool:
    retention = 1   # keep the logs around for 1 hour
    interval = 5    # create new file every so many minutes
    logdir = "./logs/"  # directory must exist
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
        self.retention = retention
        self.interval = interval

    def pool_switch(self):
        # check if the interval has passed and a new file is needed
        if not self.dbname or not self.logdir:
            raise ValueError
        lt = time.time()
        if not self.logfile or lt >= self.timestamp + self.interval:
            if self.logfile:
                self.logfile.close()
                self.pool_cleanup()
                self.pool_compress()
            self.timestamp = lt
            self.tag = self.logdir + self.dbname + '_' + time.strftime("%y-%m-%dT%H:%M:%S", time.localtime(lt))
            try:
                self.logfile = open(self.tag, "a")
            except IOError:
                raise

    def pool_record(self, json_str):
        # Move the json string to the latest log file
        self.pool_switch()
        if self.logfile:
            self.logfile.write(json_str)

    def pool_cleanup(self):
        # remove all files whose retention have passed
        files = os.listdir(self.logdir)
        lt = time.time()
        lt = lt - self.retention * 3600
        tag = self.logdir + self.dbname + '_' + time.strftime("%y-%m-%dT%H:%M:%S", time.localtime(lt))
        for f in files:
            if f < tag:
                print('consider %s for removal' % f)

    def pool_compress(self):
        # Start compressing the latest log file in the background
        with open(self.tag, 'rb') as f_in:
            with gzip.open(self.tag + '.gz', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
