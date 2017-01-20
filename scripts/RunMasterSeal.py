from __future__ import print_function
from subprocess import PIPE, Popen

# constants
COMMAND = './programlinux.e'            # command to run
ORIG_PARAM_FILE = 'sealmaster.txt'      # original parameters file
ALT_PARAM_FILE = 'sealmaster_alt.txt'   # altered parameters file

ITERATIONS = 1                          # iterations as asked by fortran program

# parameter info
e = 'Egr_Epithelial_proliferation_rate'
a = 'ACT_BMP4_auto-activation'
p = 'Pbi_Posterior_bias'

ranges = {e: (0.0085, 0.0340, 5.0), a: (0.55, 2.2, 5.0), p: (9.0, 36.0, 5.0)}  # defines ranges & step per parameters


# reads the parameters from the specified file as key-value pairs
def read_param_file(filename):
    params = []
    with open(filename) as f:
        for line in f:
            pair = tuple(line.split())  # value-key pair
            params.append(pair)

    return params


# alters specified parameters in list with new values
def alter_params(param_list, params_to_alter):
    for i in range(len(param_list)):
        pair = param_list[i]
        if pair[1] in params_to_alter:
            param_list[i] = params_to_alter[pair[1]], pair[1]


# outputs the altered parameters file to be input to program
def output_altered_param_file(params):
    with open(ALT_PARAM_FILE, 'w') as text_file:
        for pair in params:
            text_file.write(str(pair[0]) + '\t\t' + pair[1] + '\n')


# executes the program with the specified input file
def execute(cmd, out_filename):
    args = str(ITERATIONS) + '\n' + out_filename + '\n-1'
    process = Popen(cmd, stdin=PIPE, stdout=PIPE)
    process.communicate(input=bytes(args))


# for iterating by float rather than int (INCLUSIVE)
def frange_incl(start, stop, step):
    index = 0
    while start + index * step <= stop:
        yield start + index * step
        index += 1

# main
if __name__ == '__main__':
    # get the original inputs
    input_params = read_param_file(ORIG_PARAM_FILE)

    # alter parameters and run program for every combination in specified ranges
    file_map = [('Filename', 'e', 'a', 'p')]
    counter = 1

    e_step = (ranges[e][1] - ranges[e][0]) / ranges[e][2]
    a_step = (ranges[a][1] - ranges[a][0]) / ranges[a][2]
    p_step = (ranges[p][1] - ranges[p][0]) / ranges[p][2]
    for i in frange_incl(ranges[e][0], ranges[e][1], e_step):
        for j in frange_incl(ranges[a][0], ranges[a][1], a_step):
            for k in frange_incl(ranges[p][0], ranges[p][1], p_step):
                alt_params = {e: i, a: j, p: k}
                alter_params(input_params, alt_params)
                output_altered_param_file(input_params)

                execute([COMMAND, ALT_PARAM_FILE], str(counter))

                file_map.append((counter, i, j, k))

                counter += 1

    with open('file_map.csv', 'w') as text_file:
        for data in file_map:
            text_file.write(str(data[0]) + ',' + str(data[1]) + ',' + str(data[2]) + ',' + str(data[3]) + ',' + '\n')