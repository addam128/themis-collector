import lddwrap as ldd
import uuid

from pathlib import Path
from zipfile import ZipFile
from argparse import ArgumentParser



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
        self._deps = None



    def collect(
        self
    ) -> 'Collector':

        self._deps = list(
            map(
                lambda dep: str(dep.path),
                ldd.list_dependencies(Path(self._path))
                )
        )

        return self




    def archive(
        self
    ) -> None:

        with ZipFile(f"{self._config.sample_dir}/{self._name}_{uuid.uuid4()}.zip", mode='x') as zf:
            for dep in self._deps:
                if dep is None or dep == "None":
                    continue
                zf.write(dep)
    


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