Simple tool to show commits grouped by issues. You can filter commits by date, user and reverse the commits order (by default they are listed from last to first). 

Commits have to include substring `#<number-of-issue>` to be considered connected with the issue. 

## Examples

`./report_from_git.py --repo <full link to git repo>`
will show all commits grouped by issue. 

`./report_from_git.py --repo <full link to git repo> --from 2018-10-20 --to 2018-10-30`
will show commits from 20th of October 2018 to 30th of October 2018.


`./report_from_git.py --repo <full link to git repo> --from 2018-10-20 --to 2018-10-30 --user vovapolu`
will show commits from 20th of October 2018 to 30th of October 2018 from user with name "vovapolu". 


