from __future__ import print_function
from subprocess import PIPE, Popen

# files
COMMAND = './programlinux.e'
ORIG_PARAM_FILE = 'sealmaster.txt'
PARAM_FILE = 'sealmaster.txt'
OUT_FILE_FORMAT = 'out_'

# variables
iterations = 1000   # iterations as asked by fortran program

e = 'Egr_Epithelial_proliferation_rate'
a = 'ACT_BMP4_auto-activation'
p = 'Pbi_Posterior_bias'

ranges = {e: (0.0085, 0.034), a: (0.55, 2.2), p: (9, 36)}   # defines ranges per parameters
steps = {e: 0.0001, a: 0.01, p: 1}                          # defines increment per iteration


# functions
def read_param_file():
    print('read')


def modify_param_file():
    print('modify')


def execute(cmd, filename):
    args = str(iterations) + '\n' + filename + '\n-1'
    p = Popen(cmd, stdin=PIPE, stdout=PIPE)
    p.communicate(input=bytes(args))


# main
if __name__ == '__main__':
    execute([COMMAND, PARAM_FILE], 'test')
