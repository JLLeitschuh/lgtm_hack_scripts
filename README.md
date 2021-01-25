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
# Finds all repositories for a specified Github organization and adds them to your LGTM's account's project list. (note: this will only follow repos that contain Kotlin, Java, and Groovy languages).
python3 follow_org.py GITHUB_ORG_TO_FOLLOW

# Finds all repositories for a specified Github organization and unfollows them from your LGTM account's project list.
python3 unfollow_org.py GITHUB_ORG_TO_UNFOLLOW

# Finds all repositories for a specified Github Organization and adds them to your specified LGTM account's project list.
python3 move_org_projects_under_project_list_then_unfollow.py LGTM_PROJECT_LIST_NAME GITHUB_ORG
```

## Legal

The author of this script assumes no liability for your use of this project, including,
but not limited legal repercussions or being banned from [LGTM.com](https://lgtm.com).
Please consult the [LGTM.com](https://lgtm.com) terms of service for more information.
