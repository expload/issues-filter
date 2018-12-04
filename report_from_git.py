#!/usr/local/bin/python3
import os
import subprocess
import re
from collections import defaultdict
import sys
import argparse
import requests
import json

parser = argparse.ArgumentParser()

parser.add_argument("--repos", nargs='+', required=True, help="Organization and repository name. " + \
                                                               "Only commits from these repositories will be printed. Example: expload/pravda")
parser.add_argument("--since", required=False, help="Starting date. " + \
                                                    "Only commits after this date will be printed. Example: 2018-10-20")
parser.add_argument("--until", required=False, help="Finishing date. " + \
                                                    "Only commits before this date will be printed. Example: 2018-10-20")
parser.add_argument("--users", nargs='+', required=False, help="Github logins of users. " + \
                                                               "Only commits of these users will be printed.")
parser.add_argument("--reverse", action="store_true", help="Reverse the order of commits.")
parser.add_argument("--token", required=False, help="Oauth github token.")

args = parser.parse_args()

def download_commits(repo, user):
    page = 1
    commits = []
    while True:
        params = {"until": args.until, "since": args.since, "per_page": 100, "page": page, "author": user}
        if args.token is not None:
            params["access_token"] = args.token
        raw_commits = json.loads(requests.get("https://api.github.com/repos/{}/commits".format(repo), params=params).text) 
        if not isinstance(raw_commits, list):
            break
        if len(raw_commits) == 0:
            break
        for rw in raw_commits:
            sha = rw["sha"]
            msg = rw["commit"]["message"]
            commits.append((sha, msg))
        
        page += 1

    if args.reverse:
        commits = commits[::-1]

    return commits

commit_number = re.compile('#(\\d+)')

for user in args.users:
    print()
    print(user)
    for repo in args.repos:        
        print()
        print(repo)
        issues = defaultdict(list)
        for commit in download_commits(repo, user):    
            issue = commit_number.search(commit[1])
            if issue is not None:
                issue = issue.group(0)
            else:
                issue = "none"
            issues[issue].append(commit[0])

        for (issue, shas) in issues.items():
            print()
            if issue != "none":
                print("https://github.com/{}/issues/{}".format(repo, issue[1:]))
            else:
                print("none issue")
            print()
            for sha in shas:
                print("https://github.com/{}/commit/{}".format(repo, sha))


    

