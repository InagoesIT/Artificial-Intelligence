import glob
import logging
import os
from ast import literal_eval

logging.basicConfig(filename='results.log', level=logging.INFO)


class Tester:
    def __init__(self, folder_name):
        self.folder_name = folder_name

    def test(self):
        for file_name in glob.glob(f'{self.folder_name}/*.txt'):
            logging.info(f"~~~~~~ The result for the file with the name = {file_name} ~~~~~~~~~")
            print(file_name)
            with open(file_name) as file:
                file_contents = file.read().split('\n')
                n = int(file_contents[0])
                blocks = literal_eval(file_contents[1])

                script_caller = f"python n_queens.py -n {n} "
                for block in blocks:
                    script_caller += f"-b {block[0] - 1} {block[1] - 1} "

                os.system(script_caller)

                logging.info(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


def main():
    tester = Tester(folder_name='instances')
    tester.test()


if __name__ == "__main__":
    main()
