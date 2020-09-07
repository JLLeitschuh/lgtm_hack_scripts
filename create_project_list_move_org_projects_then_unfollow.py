from lgtm import LGTMSite
import sys

project_list_to_create_name = sys.argv[1]
print('Creating Project List with name: %s' % project_list_to_create_name)
github_org = sys.argv[2]
print(
    'Moving code under GH org `%s` to project list `%s`, then unfollowing' %
    (github_org, project_list_to_create_name)
)

site = LGTMSite.create_from_file()

project_id = site.create_project_list(project_list_to_create_name)
site.add_org_to_project_list_by_list_key(github_org, project_id)
site.unfollow_repository_by_org(github_org)
