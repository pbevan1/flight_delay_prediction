import argparse


# See help for information on how to use arguments to run experiments
def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--api_key', type=str, help='Enter your flightlabs API key')

    args, _ = parser.parse_known_args()
    return args