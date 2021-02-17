# LGTM Hack Scripts

Collection of python helper API's for interacting with [LGTM.com](https://lgtm.com) in ways the official API doesn't support.

## Why

As a GitHub Security Lab bounty hunter the best way to run your CodeQL query against large numbers of projects is still
through the [LGTM.com](https://lgtm.com) site. However, there is still no good way to import/subscribe to large numbers
of projects on the LGTM site, nor through the official API.

However, the [LGTM.com](https://lgtm.com) enables subscriptions to projects. The query console
does allow you to run queries against large number of projects all at once. These are 'internal' APIs that are only
surfaced through UI. By utilizing these 'internal' APIs we're able to leverage bulk import and subscription to projects.

This can significantly up your LGTM BB research game.

## How

Unfortunately, because this solution isn't officially supported, there are a few pieces of API information you'll
need to extract manually while interacting with the [LGTM.com](https://lgtm.com) site.

### Using this Project

In order to extract these 'keys' for uses by these scripts, we recommend that your browser's develper tools
and inspect the various requests normally made under the 'Network' tab. This information should be put inside of a
file named `config.yml` inside the repositories root directory. This `config.yml` file is already part of the
`.gitignore` so adding it to this repository will not risk you accidentally committing it.

The format of this `config.yml` is the following:

```yaml
lgtm:
    nonce:          # From the request header `LGTM-Nonce`
    long_session:   # From the cookie named `lgtm_long_session`
    short_session:  # From the cookie named `lgtm_short_session`
    api_version:    # From a property named `api_version` inside of any JSON POST request made
github:
    api_key:        # The Github API token. You can create one here: https://github.com/settings/tokens/new. The token should have no permissions.
```

## Commands

```bash
# Finds all repositories for a specified Github organization and adds them to your LGTM's account's project list.
#
# For example, if you want to add repositories that use Java and Kotlin:
# python3 follow_org.py netflix Java,Kotlin
#
# If you want to find all CodeQL-supported repositories regardless of the language used,
# don't provide a second argument in the command:
# python3 follow_org.py netflix
#
python3 follow_org.py <GITHUB_ORG_TO_FOLLOW> <LANGUAGES_SUPPORTED>


# Finds all repositories for a specified Github organization and unfollows them from your LGTM account's project list.
python3 unfollow_org.py <GITHUB_ORG_TO_UNFOLLOW>

# Finds all repositories for a specified Github Organization and adds them to your specified LGTM account's project list.
python3 move_org_projects_under_project_list_then_unfollow.py <LGTM_PROJECT_LIST_NAME> <GITHUB_ORG>

# Finds repositories given a search term. Under the hood, the script first looks for instances in code of the search term provided and then follows the repos of those code instances
python3 follow_repos_by_search_term_via_code_instances.py <LANGUAGE> <SEARCH_TERM>

# Finds repositories given a search term. Under the hood, the script searches Github for repositories that match the provided search term.
python3 follow_repos_by_search_term.py <LANGUAGE> <SEARCH_TERM> <CUSTOM_LIST_NAME>(optional)

# Finds top repositories that have a minimum 500 stars and use the provided programming language.
python3 follow_top_repos_by_star_count.py <LANGUAGE> <CUSTOM_LIST_NAME>(optional)
```

## The Custom Projects Lists Feature
In developing these collection of scripts, we realized that when a user follows thousands of repos in their LGTM account, there is a chance that the LGTM account will break. You won't be able to use the query console and some API
calls will be broken.

To resolve this, we decided to create a feature users can opt-in. The "Custom Projects Lists" feature does the following:

- Follows all repos (aka project) in your LGTM account.
- Stores every project you follow in a txt file.
- At a later date (we suggest 24 hours), the user may run a follow-up command that will take the repos followed, add them to a LGTM custom list, and finally unfollow the projects in the user's LGTM account.

Although these steps are tedious, this is the best work-around we've found. We avoid bricking the LGTM account when projects are placed in custom lists. Also, we typically wait 24 hours since if the project is new to LGTM it will want to first process the project and projects being processed can't be added to custom lists.

Finally, by having custom lists we hope that the security researcher will have an easier time picking which repos they want to test.

### How To Run The Custom Projects Lists Feature
In some of the commands above, you will see the <CUSTOM_LIST_NAME> option. This is optional for all
commands. This CUSTOM_LIST_NAME represents the name of a LGTM project list that will be created and used to add projects to. Any projects found from that command will then be added to the LGTM custom list. Let's show an example below to get a better idea of how this works:

1. Run a command passing in the name of the custom list name. The command below will follow Javascript repos and generate a cache file of every repo you follow for the project list called "cool_javascript_projects".

    `python3 follow_top_repos_by_star_count.py javascript big_ole_js_projects`

2. Wait 1 - 24 hours.

3. Run the command below. This will take a cached file you created earlier, create a LGTM custom project list, add the projects to that project list, and finally unfollow the repositories in your LGTM account.

    `python3 move_repos_to_lgtm_lists.py`

Note: When naming a project custom list name, please use alphanumeric, dashes, and underscore characters only.

## Legal

The author of this script assumes no liability for your use of this project, including,
but not limited legal repercussions or being banned from [LGTM.com](https://lgtm.com).
Please consult the [LGTM.com](https://lgtm.com) terms of service for more information.
