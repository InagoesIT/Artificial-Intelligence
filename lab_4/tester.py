import glob
import logging
import os
from ast import literal_eval
import re

logging.basicConfig(filename='results.log', level=logging.INFO)


class Tester:
    def __init__(self, folder_name):
        self.folder_name = folder_name

    def test(self):
        files_tested = 0
        files_passed = 0

        for file_name in glob.glob(f'{self.folder_name}/*.txt'):
            logging.info(f"~~~~~~ The result for the file with the name = {file_name} ~~~~~~~~~")
            with open(file_name) as file:
                file_contents = file.read().split('\n')
                n = int(re.sub("letting n =..", "", file_contents[0]))
                blocks = literal_eval(re.sub("letting blocks =..", "", file_contents[1]))

                script_caller = f"python n_queens.py -n {n} "
                for block in blocks:
                    script_caller += f"-b {block[0] - 1} {block[1] - 1} "

                result = os.system(f"{script_caller}")
                files_tested += 1
                if result == 0:
                    files_passed += 1
                logging.info(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        logging.info(f"TESTS PASSED: {files_passed}/{files_tested}")
        logging.info(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


def main():
    tester = Tester(folder_name='instances')
    tester.test()


if __name__ == "__main__":
    main()
