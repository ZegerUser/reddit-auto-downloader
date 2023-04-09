#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import os
import time
from collections.abc import Iterable
from datetime import datetime
from multiprocessing import Pool
from pathlib import Path
from time import sleep

import praw
import praw.exceptions
import praw.models
import prawcore

from bdfr import exceptions as errors
from bdfr.configuration import Configuration
from bdfr.connector import RedditConnector
from bdfr.site_downloaders.download_factory import DownloadFactory



def _calc_hash(existing_file: Path):
    chunk_size = 1024 * 1024
    md5_hash = hashlib.md5()
    with existing_file.open("rb") as file:
        chunk = file.read(chunk_size)
        while chunk:
            md5_hash.update(chunk)
            chunk = file.read(chunk_size)
    file_hash = md5_hash.hexdigest()
    return existing_file, file_hash


class RedditDownloader(RedditConnector):
    def __init__(self, args: Configuration):
        super(RedditDownloader, self).__init__(args)
        if self.args.search_existing:
            self.master_hash_list = self.scan_existing_files(self.download_directory)

    def download(self):
        for generator in self.reddit_lists:
            try:
                for submission in generator:
                    try:
                        self._download_submission(submission)
                    except prawcore.PrawcoreException as e:
                        pass
            except prawcore.PrawcoreException as e:

                sleep(60)

    def _download_submission(self, submission: praw.models.Submission):
        if submission.id in self.excluded_submission_ids:

            return
        elif submission.subreddit.display_name.lower() in self.args.skip_subreddit:

            return
        elif (submission.author and submission.author.name in self.args.ignore_user) or (
            submission.author is None and "DELETED" in self.args.ignore_user
        ):

            return
        elif self.args.min_score and submission.score < self.args.min_score:

            return
        elif self.args.max_score and self.args.max_score < submission.score:

            return
        elif (self.args.min_score_ratio and submission.upvote_ratio < self.args.min_score_ratio) or (
            self.args.max_score_ratio and self.args.max_score_ratio < submission.upvote_ratio
        ):

            return
        elif not isinstance(submission, praw.models.Submission):

            return
        elif not self.download_filter.check_url(submission.url):

            return


        try:
            downloader_class = DownloadFactory.pull_lever(submission.url)
            downloader = downloader_class(submission)

        except errors.NotADownloadableLinkError as e:

            return
        if downloader_class.__name__.lower() in self.args.disable_module:

            return
        try:
            content = downloader.find_resources(self.authenticator)
        except errors.SiteDownloaderError as e:

            return
        for destination, res in self.file_name_formatter.format_resource_paths(content, self.download_directory):
            if destination.exists():

                continue
            elif not self.download_filter.check_resource(res):

                continue
            try:
                res.download({"max_wait_time": self.args.max_wait_time})
            except errors.BulkDownloaderException as e:

                return
            resource_hash = res.hash.hexdigest()
            destination.parent.mkdir(parents=True, exist_ok=True)
            if resource_hash in self.master_hash_list:
                if self.args.no_dupes:

                    return
                elif self.args.make_hard_links:
                    try:
                        destination.hardlink_to(self.master_hash_list[resource_hash])
                    except AttributeError:
                        self.master_hash_list[resource_hash].link_to(destination)

                    return
            try:
                with destination.open("wb") as file:
                    file.write(res.content)

            except OSError as e:

                return
            creation_time = time.mktime(datetime.fromtimestamp(submission.created_utc).timetuple())
            os.utime(destination, (creation_time, creation_time))
            self.master_hash_list[resource_hash] = destination


    @staticmethod
    def scan_existing_files(directory: Path) -> dict[str, Path]:
        files = []
        for (dirpath, _dirnames, filenames) in os.walk(directory):
            files.extend([Path(dirpath, file) for file in filenames])

        pool = Pool(15)
        results = pool.map(_calc_hash, files)
        pool.close()

        hash_list = {res[1]: res[0] for res in results}
        return hash_list
