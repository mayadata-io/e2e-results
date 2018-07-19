# Issuer

The function of the issuer is to read the status of the playbook execution in /tmp/<YYYY-MM-DD-unique-run-id>/status file and creates a new comment at the issue http://github.com/openebs/e2e-results/issues/[unique-test-case-id]. The comment(status) to be commented and credentials need to be provided through their respective files as command line argument to the program. Apart from these the issuer also takes issue number and repository name as the argument. The program has following flags for providing arguments.

           Flag name                Shorthand                                     Argument Objective
     1.  --credentials                -crf                    For providing the path of the credential file to the program.
     2.  --comment                    -cof                    For providing the path of the comment file to the program.
     3.  --reponame                   -rn                     For providing the repository name containing the issue.
     4.  --issuenumber                -in                     For providing the issue number to be commented.


