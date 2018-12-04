Simple tool to show commits grouped by issues. You can filter commits by date, repos, users and reverse the commits order (by default they are listed from last to first). 

Commits have to include substring `#<number-of-issue>` to be considered connected with the issue. 

## Examples

`./report_from_git.py --repos <repo-org>/<repo-name> --since 2018-10-01 --until 2018-11-30 --users user1 user2 --token <OAuth-token>`


