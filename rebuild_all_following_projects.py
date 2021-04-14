from lgtm import LGTMSite

site = LGTMSite.create_from_file()
site.force_rebuild_all_proto_projects()
