import monobit
import frequency
import runs
import utility

import argparse


def perform_test():
    available_modes = {
        'all': run_all,
        'monobit': monobit.perform_monobit_test,
        'frequency': frequency.perform_block_frequency_test,
        'runs': runs.perform_runs_test,
    }

    args = parse_arguments()
    test = determine_test(args.mode, available_modes)
    bits = utility.get_text(args.file_path)
    test(bits)
    # test(bits, 123)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', dest='mode', type=str)
    parser.add_argument('--path', dest='file_path', type=str)
    parser.set_defaults(mode='all')
    return parser.parse_args()


def determine_test(mode, available_modes):
    test = available_modes.get(mode, 'all')
    return test


def run_all():
	monobit.perform_monobit_test()
	frequency.perform_block_frequency_test()
	runs.perform_runs_test()


perform_test()
