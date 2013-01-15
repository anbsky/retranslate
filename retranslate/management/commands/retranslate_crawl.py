#encoding: utf-8
from __future__ import print_function

import logging
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

from retranslate.utils import crawl_folder

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '<folder_path>'
    help = 'Find literals in all .py files in given folder and put them into DB'

    option_list = BaseCommand.option_list + (
        make_option('-x', '--exclude',
            action='store',
            dest='exclude',
            default=None,
            help='List of files or directories to exclude, comma-separated'
        ),
    )

    def handle(self, *args, **options):
        folder_path = args[0]
        print('Crawling {}...'.format(folder_path),)
        exclude = options['exclude'] and options['exclude'].split(',') or None
        files_count = crawl_folder(folder_path, exclude=exclude)
        print('{} files processed'.format(files_count))