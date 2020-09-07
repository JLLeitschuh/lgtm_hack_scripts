from lgtm import LGTMSite
import sys

project_list_name = sys.argv[1]
github_org = sys.argv[2]
print(
    'Moving code under GH org `%s` to project list `%s`, then unfollowing org' %
    (github_org, project_list_name)
)

site = LGTMSite.create_from_file()

project_list_id = site.get_project_list_by_name(project_list_name)
if project_list_id is not None:
    print('Found Project List with name: %s' % project_list_name)
else:
    print('Creating Project List with name: %s' % project_list_name)
    project_id = site.create_project_list(project_list_name)

site.add_org_to_project_list_by_list_key(github_org, project_list_id)
site.unfollow_repository_by_org(github_org)
