# -*- encoding: utf-8 -*-

__author__ = 'Mohanson'

import os
import shutil
import datetime
import inspect
import sys
import fnmatch

import saika.paramscheck


class Error(Exception):
    pass


class ErrorPath(Error):
    def __init__(self, des):
        self.des = des

    def __str__(self):
        return self.des


def define_path():
    return os.path.normcase(os.path.abspath(os.path.dirname(inspect.stack()[0][1])))


def caller_path():
    return os.path.normcase(os.path.abspath(os.path.dirname(inspect.stack()[1][1])))


def relpath(relpath, startpath=None):
    if not startpath:
        path = os.path.realpath(sys.path[0])
        if os.path.isfile(path):
            path = os.path.abspath(os.path.dirname(path))
        else:
            caller_file = inspect.stack()[1][1]
            path = os.path.abspath(os.path.dirname(caller_file))
        startpath = path

    if relpath.startswith('./'):
        if relpath[2:] == '':
            return os.path.normcase(os.path.abspath(startpath))
        return os.path.normcase(os.path.join(startpath, relpath[2:]))
    elif relpath.startswith('../'):
        while relpath.startswith('../'):
            relpath = relpath[3:]
            if startpath[-1] == '\\' or startpath[-1] == '/':
                startpath = startpath[:-1]
            while startpath[-1] != '\\' and startpath[-1] != '/':
                startpath = startpath[:-1]
        return os.path.normcase(os.path.abspath(os.path.join(startpath, relpath)))


def globbing(filename, patterns):
    if isinstance(patterns, str):
        patterns = [patterns]
    for pattern in patterns:
        if fnmatch.fnmatch(filename, pattern):
            return True
    return False


class PathBase(object):
    def __init__(self, path):
        self.path = os.path.normcase(os.path.abspath(path))
        self.dirname = os.path.dirname(self.path)
        self.basename = os.path.basename(self.path)

    def __str__(self):
        return "PathBase('%s')" % self.path

    def refresh(self, path):
        os.path.normcase(os.path.abspath(path))
        self.dirname = os.path.dirname(self.path)
        self.basename = os.path.basename(self.path)

    @property
    def atime(self):
        """
        return the last access time of path
        """
        return datetime.datetime.fromtimestamp(os.path.getatime(self.path))

    @property
    def mtime(self):
        """
        return the last modify time of path
        """
        return datetime.datetime.fromtimestamp(os.path.getmtime(self.path))

    @property
    def ctime(self):
        """
        return the create time of path
        """
        return datetime.datetime.fromtimestamp(os.path.getctime(self.path))

    @property
    def size(self):
        return None

    def delete(self):
        pass

    def copy(self, dpath):
        pass

    def rename(self, newname):
        newpath = os.path.join(self.dirname, newname)
        os.rename(self.path, newpath)
        self.refresh(newpath)

    def move(self, dpath):
        return shutil.move(self.path, os.path.abspath(dpath))

    def chmod(self, mode):
        """
        所有者的读、写和执行权限；同组的用户的读、写和执行权限；系统中其他用户的读、写和执行权限。
        r为4，w为2，x为1，-为0
        若要rwx属性则4+2+1=7；
        若要rw-属性则4+2=6；
        若要r-x属性则4+1=5。
        如 777 则表示, 所有用户对该文件都具有读写可执行权限
        """
        return os.chmod(self.path, mode)

    def pathjoin(self, *args):
        return os.path.join(self.path, *args)


class File(PathBase):
    @saika.paramscheck.paramscheck(path=os.path.isfile)
    def __init__(self, path):
        PathBase.__init__(self, path)

    def __str__(self):
        return "File('%s')" % self.path

    @property
    def size(self):
        return os.path.getsize(self.path)

    def delete(self):
        return os.remove(self.path)

    @saika.paramscheck.paramscheck(path=os.path.isdir)
    def copy(self, dpath):
        newpath = os.path.join(os.path.abspath(dpath), self.basename)
        return shutil.copy(self.path, newpath)


class Folder(PathBase):
    @saika.paramscheck.paramscheck(path=os.path.isdir)
    def __init__(self, path):
        PathBase.__init__(self, path)

    def __str__(self):
        return "Folder('%s')" % self.path

    @property
    def size(self):
        def get_folder_size(folder):
            total_size = os.path.getsize(folder)
            for item in os.listdir(folder):
                itempath = os.path.join(folder, item)
                if os.path.isfile(itempath):
                    total_size += os.path.getsize(itempath)
                elif os.path.isdir(itempath):
                    total_size += get_folder_size(itempath)
            return total_size

        return get_folder_size(self.path)

    def delete(self):
        return shutil.rmtree(self.path)

    @saika.paramscheck.paramscheck(path=os.path.isdir)
    def copy(self, dpath):
        newpath = os.path.join(os.path.abspath(dpath), self.basename)
        return shutil.copytree(self.path, newpath)

    def files(self, glob='*.*', key=None):
        """
        :param glob: use as Unix globbing, it accept a string '*.*' or list ['*.txt', '*.js']
        :param key: callback function, that accept a File klass parameter
        :return: File klass iterator
        """
        if key is None:
            key = lambda _: True
        condition = lambda _: globbing(_.basename, glob) and key(_)

        for i in os.listdir(self.path):
            fullpath = os.path.join(self.path, i)
            if os.path.isfile(fullpath):
                file = File(fullpath)
                if condition(file):
                    yield file

    def allfiles(self, glob='*.*', key=None):
        """
        :param glob: use as Unix globbing, it accept a string '*.*' or list ['*.txt', '*.js']
        :param key: callback function, that accept a File klass parameter
        :return: File klass iterator
        """
        if key is None:
            key = lambda _: True
        condition = lambda _: globbing(_.basename, glob) and key(_)

        for parent, dirnames, filenames in os.walk(self.path):
            for filename in filenames:
                fullname = os.path.join(parent, filename)
                file = File(fullname)
                if condition(file):
                    yield file

    def folders(self, glob='*.*', key=None):
        """
        :param glob: use as Unix globbing, it accept a string '*.*' or list ['*.txt', '*.js']
        :param key: callback function, that accept a File klass parameter
        :return: Folder klass iterator
        """
        if key is None:
            key = lambda _: True
        condition = lambda _: globbing(_.basename, glob) and key(_)

        for i in os.listdir(self.path):
            fullpath = os.path.join(self.path, i)
            if os.path.isdir(fullpath):
                folder = Folder(fullpath)
                if condition(folder):
                    yield folder

    def allfolders(self, glob='*.*', key=None):
        """
        :param glob: use as Unix globbing, it accept a string '*.*' or list ['*.txt', '*.js']
        :param key: callback function, that accept a File klass parameter
        :return: Folder klass iterator
        """
        if key is None:
            key = lambda _: True
        condition = lambda _: globbing(_.basename, glob) and key(_)

        for parent, dirnames, filenames in os.walk(self.path):
            for dirname in dirnames:
                fullpath = os.path.join(parent, dirname)
                folder = Folder(fullpath)
                if condition(folder):
                    yield folder


def file(path):
    return File(path)


def folder(path):
    return Folder(path)