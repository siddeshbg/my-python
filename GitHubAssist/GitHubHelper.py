#!/usr/bin/env python3
from github import Github
import re
import os
import sys

class GitHubHelper:
    def __init__(self, token):
        self.token = token
        self.github = Github(self.token)

    def get_repositories(self):
        return [repo for repo in self.github.get_user().get_repos()]

    def get_labels(self, repo):
        r = self.github.get_repo(repo)
        return [label for label in r.get_labels()]

    def get_path_history(self, repo, path):
        r = self.github.get_repo(repo)
        return r.get_commits(path=path)

    def get_jira_issue_from_description(self, message):
        m = re.search('JIRA Issues: (.*)', message)
        if m:
            return m.group(1)


def main():
    token = os.environ['GITHUB_TOKEN']
    g = GitHubHelper(token)
    project = os.environ['GITHUB_PROJECT']
    repo = project + "/" + os.environ['GITHUB_REPO']
    path = sys.argv[1]
    repos = g.get_repositories()
    labels = g.get_labels(repo)
    print('-'*100)
    print("commit history for %s" % path)
    print('-' * 100)
    commits = g.get_path_history(repo, path)
    for commit in commits:
        jira_id = g.get_jira_issue_from_description(commit.commit.message)
        print("commit: %s author: %s jira_id: %s" % (commit.sha, commit.author.login, jira_id))

if __name__ == '__main__':
    #github_access_token = '0a1b96463b274d80051edcb350f152a5154f7003'
    main()

