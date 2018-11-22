#!/usr/local/bin/python3
import os
import subprocess
import re
from collections import defaultdict
import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--repo", "-r", required=True, help="target repository")
parser.add_argument("--from", "-f", required=False, help="starting date")
parser.add_argument("--to", "-t", required=False, help="finishing date")
parser.add_argument("--user", "-u", required=False, help="target user")
parser.add_argument("--reverse", action="store_true", help="reverse the order of commits in git log")

args = parser.parse_args()

commit_number = re.compile('#(\\d+)')

issues = []

for line in subprocess.check_output(['git', 'log', '--pretty=format:%H~%aN~%s~%cd', '--date=format:%Y-%m-%d']).decode("utf-8").split("\n"):
    if not "Merge pull request" in line:
        (cid, user, message, date) = line.split("~")
        issue = commit_number.search(message)
        if issue is not None:
            issues.append((user, cid, date, issue.group(0)))
        else:
            issues.append((user, cid, date, "none"))

if args.reverse:
    issues = issues[::-1]

filtered_issues = defaultdict(list)

for (user, cid, date, issue) in issues:
    ok = True
    if (args.user is not None) and (args.user != user):
        ok = False

    if (getattr(args, "from") is not None) and (getattr(args, "from") > date):
        ok = False

    if (args.to is not None) and (args.to < date):
        ok = False

    if ok:
      filtered_issues[issue].append(cid)

for (issue, cids) in filtered_issues.items():
    print()
    if issue != "none":
        print(args.repo + "/issues/" + issue[1:])
    else:
        print("none issue")
    print()
    for cid in cids:
        print(args.repo + "/commit/" + cid)


    

