#encoding: utf-8
from __future__ import print_function

from django.core.management.base import BaseCommand, CommandError
import logging

from retranslate.utils import crawl_folder

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '<folder_path>'
    help = 'Find literals in all .py files in given folder and put them into DB'

    def handle(self, *args, **options):
        folder_path = args[0]
        print('Crawling {}...'.format(folder_path),)
        files_count = crawl_folder(folder_path)
        print('{} files processed'.format(files_count))