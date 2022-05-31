import sys
import bitbucket_helper


def main():
    tokens = sys.argv[1:3]
    bitbucket_token = tokens[0] if len(tokens) > 0 else input(
        "Please input Bitbucket token ")
    branch_name = tokens[1] if len(
        tokens) > 1 else "audit-final"

    pull_requests = []
    repo_names = bitbucket_helper.parse_bitbucket_repositories(
        bitbucket_helper.get_bitbucket_repositories(bitbucket_token, "WZAPP"))

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
