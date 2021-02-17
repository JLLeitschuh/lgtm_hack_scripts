from lgtm import LGTMSite
lgtm_site = LGTMSite.create_from_file()

repo_url: str = 'https://github.com/google/jax'

result = lgtm_site.follow_repository(repo_url)
print("---------------")
print("---------------")
print("---------------")
print(result)
