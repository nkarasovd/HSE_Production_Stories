import argparse

from monotone_conjugation import MonotoneConjugationTest


def test_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Monotone Conjugation Test')
    parser.add_argument("--data_in", type=str, default="data/in.txt",
                        help="Path to file with input data")
    parser.add_argument("--data_out", type=str, default="data/out.txt",
                        help="Path to file where to save results of test")
    parser.add_argument("--axis", type=int, default=0,
                        help="On which axis to order observations")
    parser.add_argument("--compare_with_pearson", type=lambda x: (str(x).lower() in ['true', '1', 'yes']),
                        default=True,
                        help="Compare conjugation measure with pearson or not")

    return parser.parse_args()


if __name__ == '__main__':
    args = test_parser()

    solver = MonotoneConjugationTest()
    solver.test(args.data_in, args.data_out, args.axis, args.compare_with_pearson)
