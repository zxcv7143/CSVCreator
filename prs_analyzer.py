import argparse
import sys
import bitbucket_helper


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', help='Bitbucket token')
    parser.add_argument('--project', help='Bitbucket project')
    parser.add_argument('--branch', help='Repo branch')

    args = parser.parse_args()

    bitbucket_token = args.token if args.token != None else input(
        "Please input Bitbucket token ")
    project_name = args.project if args.project != None else "WZAPP"
    branch_name = args.branch if args.branch != None else "audit-final"

    pull_requests = []
    repo_names = bitbucket_helper.parse_bitbucket_repositories(
        bitbucket_helper.get_bitbucket_repositories(bitbucket_token, project_name))

    for repo_name in repo_names:
        reponse_data = bitbucket_helper.get_pull_requests(
            bitbucket_token, repo_name.slug, branch_name)
        prs = bitbucket_helper.parse_pull_requests(reponse_data)
        for pr in prs:
            comments_data = bitbucket_helper.get_pull_request_comments(
                bitbucket_token, repo_name.slug, pr.pull_request_id)
            comments = bitbucket_helper.parse_pull_request_comments(
                comments_data)
            pr.comments = comments
        if len(prs) > 0:
            pull_requests.extend(prs)

    bitbucket_helper.print_all_pull_request(pull_requests)
    print('\n')


if __name__ == "__main__":
    main()
