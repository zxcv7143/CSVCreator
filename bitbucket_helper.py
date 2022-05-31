import urllib.request
import json
from types import SimpleNamespace


class PullRequest:

    def __init__(self, repository, title, destination_branch, tasks, has_conflict, url, origin_branch):
        self.repository = repository
        self.title = title
        self.destination_branch = destination_branch
        self.tasks = tasks
        self.has_conflict = has_conflict
        self.url = url
        self.origin_branch = origin_branch


class PullRequestActivity:

    def __init__(self, id, created_date, action, commit, comment):
        self.id = id
        self.created_date = created_date
        self.action = action
        self.commit = commit
        self.comment = comment


def get_pull_requests(token, repo, branchName='refs/heads/audit-final'):
    request = urllib.request.Request(
        'http://wzgdcvaleja01pr:7990/rest/api/1.0/projects/WZAPP/repos/{}/pull-requests?at=refs/heads/{}'.format(repo, branchName))
    request.add_header('Authorization', 'Bearer {}'.format(token))

    response = urllib.request.urlopen(request)

    return response.read().decode('utf-8')


def parse_pull_requests(json_text):
    data = json.loads(json_text, object_hook=lambda d: SimpleNamespace(**d))

    return list(map(lambda pr: PullRequest(
        pr.fromRef.repository.name,
        pr.title,
        pr.toRef.displayId,
        pr.properties.openTaskCount,
        pr.properties.mergeResult.outcome != 'CLEAN',
        pr.links.self[0].href,
        pr.fromRef.displayId
    ),
        data.values))


def print_all_pull_request(pull_requests):
    table_data = list(map(lambda pr: [pr.repository[0:35], pr.title[0:70],
                                      pr.destination_branch[0:35], pr.origin_branch, pr.tasks, 'YES' if pr.has_conflict else 'NO'], pull_requests))

    table_space = '{:<35} {:<70} {:<20} {:<50} {:<10} {:<4}'
    print('All pull request')
    print('----------------\n')
    print(table_space.format('Repository', 'Title',
                             'Destination branch', 'Origin branch', 'Open task', 'Has Conflict'))
    print(table_space.format('----------', '-----',
                             '----------------', '---------------', '---------', '------------'))

    for row in table_data:
        print(table_space.format(*row))

    print('\n')


def get_pull_request_activity(token, repo_name, pull_request_id):
    request = urllib.request.Request(
        'http://wzgdcvaleja01pr:7990/rest/api/1.0/projects/WZAPP/repos/{}/pull-requests/{}/activities'.format(repo_name, pull_request_id))
    request.add_header('Authorization', 'Bearer {}'.format(token))

    response = urllib.request.urlopen(request)

    return response.read().decode('utf-8')


def parse_pull_request_activity(json_text):
    data = json.loads(json_text, object_hook=lambda d: SimpleNamespace(**d))

    return list(map(lambda pr: PullRequestActivity(
        pr.id,
        pr.createdDate,
        pr.action,
        pr.commit,
        pr.comment
    ),
        data.values))


def print_pull_request_activity(pull_request_activity):
    table_data = list(map(lambda pr: [pr.repository[0:35], pr.title[0:70],
                                      pr.destination_branch[0:35], pr.origin_branch, pr.tasks, 'YES' if pr.has_conflict else 'NO'], pull_request_activity))

    table_space = '{:<35} {:<70} {:<20} {:<50} {:<10} {:<4}'
    print('All pull request')
    print('----------------\n')
    print(table_space.format('Repository', 'Title',
                             'Destination branch', 'Origin branch', 'Open task', 'Has Conflict'))
    print(table_space.format('----------', '-----',
                             '----------------', '---------------', '---------', '------------'))

    for row in table_data:
        print(table_space.format(*row))

    print('\n')
