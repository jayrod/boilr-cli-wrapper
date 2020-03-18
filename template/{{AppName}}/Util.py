from glob import iglob
from os import curdir
from pathlib import Path


class Util:
    def msg(self, message: str) -> str:
        return "[+] {0}".format(message)

    def err_msg(self, message: str) -> str:
        return "[!] {0}".format(message)

    def append_scan_log(self, app_name: str) -> None:
        search_path = str(Path(curdir).joinpath("**/scans/*scan_overview*.md"))
        overview_path = [f for f in iglob(search_path, recursive=True)]

        if not overview_path:
            print(self.msg("Did not locate scanning overview"))
            return

        log_string = "* {0} Scan executed\n".format(app_name)
        with open(overview_path[0], "a+") as log:
            log.write(log_string)


if __name__ == "__main__":
    print(Util().msg("test regular"))
    print(Util().err_msg("test error regular"))
    print(Util().append_scan_log("Test App"))
