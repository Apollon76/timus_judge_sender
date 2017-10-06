import sys
import os


def main():
    print(sys.argv)
    task = sys.argv[1]
    checker = sys.argv[2]
    generator = sys.argv[3]
    while True:
        os.system('{} > stress_input.txt'.format(generator))
        os.system('{} < stress_input.txt > solution_output.txt'.format(task))
        os.system('{} < stress_input.txt > checker_output.txt'.format(checker))
        with open('solution_output.txt', 'r') as f:
            solution_ans = f.read()
        with open('checker_output.txt', 'r') as f:
            checker_ans = f.read()
        if checker_ans != solution_ans:
            raise ValueError('Incorrect answer')
        print('Ok')

if __name__ == '__main__':
    main()
