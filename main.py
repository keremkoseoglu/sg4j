""" Entry point """
import os
from os import path
import json


class Main:
    """ Main class """
    def __init__(self):
        self._config = {}
        self._latest_dir = ""
        self._latest_app = ""

    def run(self):
        """ Main method """
        self._read_config()
        self._find_latest_dir()
        self._find_latest_app()
        self._launch_latest_app()

    def _read_config(self):
        self._config = {}
        config_path = os.path.join(os.getcwd(), "config.json")
        with open(config_path) as config_file:
            self._config = json.load(config_file)

    def _find_latest_dir(self):
        self._latest_dir = ""
        subfolders = [ f.path for f in os.scandir(self._config["app_root"]) if f.is_dir() ]
        
        latest_major = 0
        for subfolder in subfolders:
            major = 0
            deepest_dir = self._get_deepest_dir(subfolder)
            if len(deepest_dir) >= 8:
                major = int(deepest_dir[7:8])
            if major > latest_major:
                latest_major = major

        major_prefix = "SAPGUI " + str(major) + "."
        deletable_indices = []
        index = -1
        for subfolder in subfolders:
            index += 1
            if major_prefix not in subfolder:
                deletable_indices.append(index)
        deletable_indices.sort(reverse=True)
        for index in deletable_indices:
            subfolders.pop(index)

        if len(subfolders) == 1:
            self._latest_dir = subfolders[0]
            return

        latest_minor = 0
        for subfolder in subfolders:
            minor = 0
            deepest_dir = self._get_deepest_dir(subfolder)
            if len(deepest_dir) >= 11:
                minor = int(deepest_dir[9:11])
            if minor > latest_minor:
                latest_minor = minor

        minor_prefix = major_prefix + str(latest_minor)
        deletable_indices = []
        index = -1
        for subfolder in subfolders:
            index += 1
            if minor_prefix not in subfolder:
                deletable_indices.append(index)
        deletable_indices.sort(reverse=True)
        for index in deletable_indices:
            subfolders.pop(index)

        if len(subfolders) == 1:
            self._latest_dir = subfolders[0]
            return

        latest_rev = 0
        for subfolder in subfolders:
            rev = 0
            deepest_dir = self._get_deepest_dir(subfolder)
            split = deepest_dir.split("rev")
            if len(split) <= 1:
                continue
            rev = int(split[1])
            if rev > latest_rev:
                latest_rev = rev

        if latest_rev == 0:
            rev_prefix = minor_prefix
        else:
            rev_prefix = minor_prefix + "rev" + str(latest_rev)

        deletable_indices = []
        index = -1
        for subfolder in subfolders:
            index += 1
            if rev_prefix not in subfolder:
                deletable_indices.append(index)
        deletable_indices.sort(reverse=True)
        for index in deletable_indices:
            subfolders.pop(index)

        subfolders.sort(reverse=True)
        self._latest_dir = subfolders[0]

    def _find_latest_app(self):
        self._latest_app = ""
        for file in os.listdir(self._latest_dir):
            if file.endswith(".app"):
                self._latest_app = path.join(self._latest_dir, file)
                return

    def _launch_latest_app(self):
        cmd = "\"" + self._latest_app + "\""
        os.system("open " + cmd)

    @staticmethod
    def _get_deepest_dir(dir: str) -> str:
        dirs = dir.split("/")
        return dirs[len(dirs)-1]


if __name__ == '__main__':
    Main().run()