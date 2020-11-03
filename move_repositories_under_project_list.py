import argparse

from lgtm import LGTMSite


def main():
    parser = argparse.ArgumentParser(
        description='moves the specified list of projects under a project list'
    )
    parser.add_argument('-l', '--list-name', dest='list_name', required=True)
    parser.add_argument('-i', '--infile', dest='in_file', required=True, type=argparse.FileType('r'))
    args = parser.parse_args()

    site = LGTMSite.create_from_file()

    project_list_id = site.get_or_create_project_list(args.list_name)

    ids = []
    for line in args.in_file:
        line_clean: str = line.strip()
        gh_project_path = line_clean.lstrip('https://github.com/')
        the_id = LGTMSite.retrieve_project_id(gh_project_path)
        if the_id is not None:
            print('Loaded: %s' % gh_project_path)
            ids.append(str(the_id))

    site.load_into_project_list(project_list_id, ids)


if __name__ == "__main__":
    main()
