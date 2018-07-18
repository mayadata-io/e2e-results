import argparse,github

def get_credentials(fileName):
    file=open(fileName,"r")
    username=file.readline()
    password=file.readline()
    file.close()
    return username.strip(),password.strip()

def get_comment(fileName):
    file=open(fileName,"r")
    comment=file.read()
    file.close()
    return comment.strip()

def main():
    parser = argparse.ArgumentParser(description='Issuer cli used to comment on github issues')
    parser.add_argument('-crf', '--credential', help='Credential file contains authentication information for github api', required=True)
    parser.add_argument('-rn', '--reponame' ,help='Repository name' ,required=True)
    parser.add_argument('-in', '--issuenumber' ,help='Issue Number to be commented' , type=int, required=True)
    parser.add_argument('-cof', '--comment', help='Comment file contains comment to posted on github issue',required=True)
    args = vars(parser.parse_args())
    username,password=get_credentials(fileName=args['credential'])
    comment=get_comment(fileName=args['comment'])
    reponame=args['reponame']
    issuenumber=args['issuenumber']
    g=github.Github(username,password)
    print(g.get_user().get_repo(reponame).get_issue(issuenumber).create_comment(comment))


if __name__=="__main__":
    main()
