import sys
import bitbucket_helper
from saver_class import SaverClass


def main():
    tokens = sys.argv[1:4]
    bitbucket_token = tokens[0] if len(tokens) > 0 else input(
        "Please input Bitbucket token ")
    repo_name = tokens[1] if len(
        tokens) > 1 else input("Please input repo name ")
    branch_name = tokens[2] if len(
        tokens) > 2 else "refs/heads/audit-final"

    reponse_data = bitbucket_helper.get_pull_requests(
        bitbucket_token, repo_name, branch_name)
    pull_requests = bitbucket_helper.parse_pull_requests(reponse_data)
    print('\n')
    for pr in pull_requests:
        comments_data = bitbucket_helper.get_pull_request_comments(
            bitbucket_token, repo_name, pr.pull_request_id)
        comments = bitbucket_helper.parse_pull_request_comments(comments_data)
        pr.comments = comments
    bitbucket_helper.print_all_pull_request(pull_requests)
    print('\n')


if __name__ == "__main__":
    main()
