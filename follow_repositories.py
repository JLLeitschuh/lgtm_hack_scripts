import argparse

from lgtm import LGTMSite


def main():
    parser = argparse.ArgumentParser(
        description='follow repositories from a list of newline delimited repositories'
    )
    parser.add_argument('-i', '--infile', dest='in_file', required=True, type=argparse.FileType('r'))
    args = parser.parse_args()
    site = LGTMSite.create_from_file()
    for line in args.in_file:
        line_clean = line.strip()
        print('Following: %s' % line_clean)
        site.follow_repository(line_clean)


if __name__ == "__main__":
    main()
