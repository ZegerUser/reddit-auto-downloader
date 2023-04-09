#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from collections.abc import Iterable
from time import sleep

import prawcore

from bdfr.archiver import Archiver
from bdfr.configuration import Configuration
from bdfr.downloader import RedditDownloader


class RedditCloner(RedditDownloader, Archiver):
    def __init__(self, args: Configuration):
        super(RedditCloner, self).__init__(args)

    def download(self, submission):
        try:
            self._download_submission(submission)
            self.write_entry(submission)
            return 1
        except:
            return 1