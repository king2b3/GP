from HereBoy import HereBoy
import argparse
import os


def parse_arguments(
    args=None
) -> None:
    """Returns the parsed arguments.

    Parameters
    ----------
    args: List of strings to be parsed by argparse.
        The default None results in argparse using the values passed into
        sys.args.
    """
    parser = argparse.ArgumentParser(
            description="Argument parsing for genetic programming system",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    #parser.add_argument("input_file", help="Path to the input file.")
    parser.add_argument("runs", help="Sets the number of runs to be averaged and saved",
            default=1)
    parser.add_argument("-hb", "--hboy", help="Chooses the hereBOY mutation system",
            default=False, action="store_true")
    parser.add_argument("-s", "--stochastic", help="Chooses the stochastic mutation system",
            default=False, action="store_true")
    parser.add_argument("-e", "--exhaustive", help="Chooses the exhaustive mutation approach",
            default=False, action="store_true")
    parser.add_argument("-r", "--random", help="Sets the number of runs to be averaged and saved",
            default=False, action="store_true")
    parser.add_argument("-ct", "--combinational_trojan", help="Sets the number of runs to be averaged and saved",
            default=False, action="store_true")
    parser.add_argument("-v", "--variant", help="Sets the number of runs to be averaged and saved",
            default=False, action="store_true")
    parser.add_argument("-i", "--in_num", help="Number of random inputs to be input",
            default=0, type=int)

    args = parser.parse_args(args=args)
    return args

def main(
    in_num=0,
    runs=1,
    hboy=False, 
    stochastic=False,
    exhaustive=False,
    random=False, 
    combinational_trojan=False,
    variant=False
) -> None:
    """ Main function.

    Parameters
    ----------
    runs: int
        Number of runs to average for testing. Default is 1 test
    here_boy: bool
        Mutation type is the software HereBOY approach. 
    stochastic: bool
        Mutation type is a stoachatic mutations check
    exhaustive: bool
        Mutation type is exhaustive mutation checking
    random: bool
        Starting circuit is randomly generated
    combinational_trojan: bool
        Random combinational trojan is inserted
    variant: bool
        A varint is created from the original ast
    ------
    FileNotFoundError
        Means that the input file was not found.
    """   
    # Error check if the file even exists
    #if not os.path.isfile(input_file):
    #    raise FileNotFoundError("File not found: {}".format(input_file))
    

    test1 = HereBoy(
        None,
        #['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel'], # ast
        None,
        #['I0','I1','Sel'], # ins
        40000, # num epochs
        0.3, # init struct fit
        in_num
    )

    if hboy:
        mutation_mode = 1
    elif exhaustive:
        mutation_mode = 2
    else:
        mutation_mode = 3

    if random:
        test_mode = 1
    elif combinational_trojan:
        test_mode = 2
    else:
        test_mode = 3

    test1.scalabilityTest(
        mutation_mode,
        test_mode,
        runs,
        in_num
    )


if __name__ == "__main__":
    import sys
    args = parse_arguments()
    try:
        main(**vars(args))
    except FileNotFoundError as exp:
        print(exp, file=sys.stderr)
        exit(-1)