import glob
import logging
import os
from ast import literal_eval

logging.basicConfig(filename='results.log', level=logging.INFO)


class Tester:
    def __init__(self, folder_name):
        self.folder_name = folder_name

    def test(self):
        # for file_name in glob.glob(f'{self.folder_name}/*.txt'):
        #     logging.info("~~~~~~ The result for the file with the name =", file_name, "~~~~~~~~~")

        # TO DO
        # to test this again -> in log the test for this file kinda has queens attacking??
        with open("instances/block-10-2-4.txt") as file:
            file_contents = file.read().split('\n')
            n = int(file_contents[0])
            blocks = literal_eval(file_contents[1])

            script_caller = f"python n_queens.py -n {n} "
            for block in blocks:
                script_caller += f"-b {block[0]} {block[1]} "

            os.system(script_caller)


def main():
    tester = Tester(folder_name='instances')
    tester.test()


if __name__ == "__main__":
    main()
