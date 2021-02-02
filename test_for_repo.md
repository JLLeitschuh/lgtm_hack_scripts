Here are the scripts I ran:

```
python3 follow_top_repos_by_star_count.py Javascript

# to run (searches for repos)
python3 follow_repos_by_search_term.py Javascript express

# to run
python3 follow_repos_by_search_term_via_code_instances.py Javascript express

```


## What Does This PR Do

Resolves #5.

This PR introduces three new scripts. Each of these scripts search and follow repositories based on conditions provided by the user:

1. follow_repos_by_search_term_via_code_instances.py

This script takes a search term and a programming language as input and finds code instances that contain the search term and the programming language used. When we find a code instance, we then follow the repo that the code instance belongs to on LGTM.com.

2. follow_repos_by_search_term.py

This script takes a search term and a programming language as input. It then finds repositories that contain the search term and the programming language used. When we find a repository, we then follow it on LGTM.com.

3. follow_top_repos_by_star_count.py

This script takes a programming language as input. It then finds repositories that contain more than 500 stars and uses the programming language provided in the input.


## Anything Else We Should Know

- These scripts all contain a simple throttle on HTTP requests. This throttle feature is used to ensure that users do not send too many requests at once.
- I've tested each script on my local machine. Each script ran successfully.
- I've structured the code so that once a Github repo is found, we immediately add it follow it on LGTM. I think this is a better approach than first collecting all Github repos and then following them on lgtm.com because if an internet connection breaks midway through the script running, we may never have actually followed any repos on LGTM. All that work would have been lost. Here at least we have some results than no results at all.
- I've introduced a new technique in searching for repos in these scripts. By default, Github will only return the first 1,000 results in any search query. To handle this limitation, we limit searches to specific date-times for when the repo was first created. This allows us to retrieve almost all repositories that match the query.*


/ * This is easier to explain with the following example. Let's say we want to find repositories for a given programming language that have more than 500 stars. Normally, Github only retrieves the first 1,000 results. We can break this query up into multiple queries like so:

- Find repositories with more than 500 stars for a given programming language where the repository was created between 2008 - 2009
- Find repositories with more than 500 stars for a given programming language where the repository was created between 2009 - 2010
- Find repositories with more than 500 stars for a given programming language where the repository was created between 2010 - 2011
- Etc.

Even though each query is limited to the first 1,000 results, by breaking up the queries we are much more likely to get all results instead of the first 1,000 repositories created from 2008 till now.
