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

def post_comment(repoName,issueNumber,username,password,comment):
    g=github.Github(username,password)
    print(g.get_user().get_repo(repoName).get_issue(issueNumber).create_comment(comment))

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
    post_comment(reponame,issuenumber,username,password,comment)



if __name__=="__main__":
    main()
