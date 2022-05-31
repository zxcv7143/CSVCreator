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
    bitbucket_helper.print_all_pull_request(pull_requests)
    print('\n')


def select_number_of_pull_request():
    while True:
        try:
            user_input = input(
                "Please input a number of pull request for which you want to create a Pivotal story or input u to update and q to exit: ")
            if user_input == 'u':
                break
            elif user_input == 'q':
                SaverClass.delete_default_type()
                break
            else:
                numberOfStory = int(user_input) - 1
                return numberOfStory
        except:
            continue


def get_selected_type():
    selected_type = SaverClass.load_default_type()
    if not selected_type:
        while True:
            print("1. Mobile \n")
            print("2. Web \n")
            print("3. Backend \n")
            selected_type = int(
                input("Please select default type of stories "))
            if selected_type <= 3 and selected_type > 0:
                SaverClass.save_default_type(selected_type)
                break
    return selected_type


if __name__ == "__main__":
    main()
