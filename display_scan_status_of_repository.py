import argparse

from lgtm import LGTMSite


def main():
    parser = argparse.ArgumentParser(
        description='display the build status of the specified repositories'
    )
    parser.add_argument('-i', '--infile', dest='in_file', required=True, type=argparse.FileType('r'))
    args = parser.parse_args()
    unloaded_count = 0
    total_count = 0
    for line in args.in_file:
        line_clean: str = line.strip()
        total_count += 1
        gh_project_path = line_clean.lstrip('https://github.com/')
        print('Checking status for %s' % gh_project_path)
        result = LGTMSite.retrieve_project(gh_project_path)
        print(result)
        if 'code' in result:
            unloaded_count += 1
    print('%d/%d projects loaded' % (total_count - unloaded_count, total_count))


if __name__ == "__main__":
    main()
