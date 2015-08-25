# -*- encoding: utf-8 -*-

__author__ = 'Mohanson'

from .utils import folder

CLEAN_DEFINE = {'python': {'files': ['*.pyc'],
                           'folders': ['dist', 'build', '__pycache__', '*.egg-info']}}


def clean(path, key):
    print('\nCleaning Start in %s' % path)
    clean_folders_num, clean_files_num = 0, 0
    files_key = CLEAN_DEFINE[key]['files']
    folders_key = CLEAN_DEFINE[key]['folders']
    project = folder(path)
    for clean_folder in project.allfolders(glob=folders_key):
        clean_folder.delete()
        clean_folders_num += 1
        print('Cleaning: Folder(%s)' % clean_folder.path[len(path):])
    for clean_file in project.allfiles(glob=files_key):
        clean_file.delete()
        clean_files_num += 1
        print('Cleaning: File(%s)' % clean_file.path[len(path):])
    print('Cleaning Down, Folders(%s), Files(%s) in %s' % (clean_folders_num, clean_files_num, path))


def auto_clean(path):
    project = folder(path)
    numpy = len(list(project.files('*.py')))
    if numpy:
        clean_python(path)


def clean_python(path):
    clean(path, 'python')