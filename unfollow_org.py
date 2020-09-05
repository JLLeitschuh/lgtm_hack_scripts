from lgtm import LGTMSite
import sys

org_to_delete = sys.argv[1]
print('Unfollowing Org: %s' % org_to_delete)

site = LGTMSite.create_from_file()
site.unfollow_repository_by_org(org_to_delete)
