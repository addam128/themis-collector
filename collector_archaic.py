from asyncio.subprocess import PIPE
import uuid
import subprocess
import re

from pathlib import Path
from zipfile import ZipFile
from argparse import ArgumentParser


PATH_REGEX = re.compile(r".*=>\s*(?P<path>[^\(\s]*).*")

class Collector:
    def __init__(
        self,
        resultdir: str,
        path: str,
        name: str
    ) -> None:

        self._path = path
        self._resultdir = resultdir
        self._name = name
        self._deps = list()
        self._deps.append(path)



    def collect(
        self
    ) -> 'Collector':

        proc = subprocess.run(["ldd", self._path], stdout=PIPE)
        for line in map(lambda l: l.decode('ascii'), proc.stdout.split(b'\n')):
            ma = PATH_REGEX.match(line)
            if ma is not None:
                self._deps.append(ma.group("path"))

        return self




    def archive(
        self
    ) -> None:

        with ZipFile("{}/{}_{}.zip".format(self._resultdir, self._name, uuid.uuid4()), mode='x') as zf:
            for dep in self._deps:
                if dep is None or dep == "None":
                    continue
                try:
                    zf.write(dep, arcname=dep.split("/")[-1])
                except:
                    pass


def parse_args():
    parser = ArgumentParser("themis-collector")
    parser.add_argument("path", help="Path to binary to collect")
    parser.add_argument("--zipname", required=True, help="Name of output zip")

    return parser.parse_args()



def main():

    args = parse_args()
    Collector("./", args.path, args.zipname).collect().archive()



if __name__ == '__main__':
    main()