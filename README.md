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

## Installation

```bash
# Clone the repo
git clone https://github.com/JLLeitschuh/lgtm_hack_scripts.git

# Install the necessary python libraries
pip3 install PyGithub
pip3 install pyyaml
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

# Finds repositories given a search term. Under the hood, the script searches Github for repositories that match the provided search term.
python3 follow_repos_by_search_term.py <LANGUAGE> <SEARCH_TERM>

# Finds top repositories that have a minimum 500 stars and use the provided programming language.
python3 follow_top_repos_by_star_count.py <LANGUAGE>  

# Re-runs failed project builds in an attempt to get the build to succeed.
python3 rebuild_all_following_projects.py
```

## Legal

The author of this script assumes no liability for your use of this project, including,
but not limited legal repercussions or being banned from [LGTM.com](https://lgtm.com).
Please consult the [LGTM.com](https://lgtm.com) terms of service for more information.
