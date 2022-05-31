
import urllib.request
import json
from types import SimpleNamespace
from report_class import ReportClass
from datetime import date
from datetime import datetime
import headers


class PullRequest:    

    def __init__(self, pull_request_id, repository, title, destination_branch, tasks, resolved_tasks, has_conflict, url, origin_branch, comments=None):
        self.repository = repository
        self.pull_request_id = pull_request_id
        self.title = title
        self.destination_branch = destination_branch
        self.tasks = tasks
        self.has_conflict = has_conflict
        self.url = url
        self.origin_branch = origin_branch
        self.resolved_tasks = resolved_tasks
        self.comments = comments


class PullRequestActivity:

    def __init__(self, id, text, action, commit, comment):
        self.id = id
        self.text = text
        self.action = action
        self.commit = commit
        self.comment = comment


class PullRequestComment:

    def __init__(self, id, text):
        self.id = id
        self.text = text


def get_pull_requests(token, repo, branchName='refs/heads/audit-final'):
    request = urllib.request.Request(
        'http://wzgdcvaleja01pr:7990/rest/api/1.0/projects/WZAPP/repos/{}/pull-requests?at=refs/heads/{}'.format(repo, branchName))
    request.add_header('Authorization', 'Bearer {}'.format(token))

    response = urllib.request.urlopen(request)

    return response.read().decode('utf-8')


def parse_pull_requests(json_text):
    data = json.loads(json_text, object_hook=lambda d: SimpleNamespace(**d))

    pull_request_list = list(map(lambda pr: PullRequest(
        pr.id,
        pr.fromRef.repository.name,
        pr.title,
        pr.toRef.displayId,
        pr.properties.openTaskCount,
        pr.properties.resolvedTaskCount,
        pr.properties.mergeResult.outcome != 'CLEAN',
        pr.links.self[0].href,
        pr.fromRef.displayId,
    ),
        data.values))

    return pull_request_list


def print_all_pull_request(pull_requests):
    table_data = list(map(lambda pr: [pr.repository[0:35], pr.title[0:70],
                                      pr.destination_branch[0:35], pr.origin_branch, pr.tasks, pr.resolved_tasks,
                                      len(pr.comments),  sum('#high' in elem.text for elem in pr.comments),  sum('#low' in elem.text for elem in pr.comments)], pull_requests))

    table_space = '{:<20} {:<70} {:<20} {:<50} {:<10} {:<14} {:<8} {:<4} {:<4}'
    print('All pull request')
    print('----------------\n')
    print(table_space.format(headers.HEADERS[0], headers.HEADERS[1], headers.HEADERS[2], headers.HEADERS[3], headers.HEADERS[4],
        headers.HEADERS[5],headers.HEADERS[6],headers.HEADERS[7], headers.HEADERS[8]))    
    print(table_space.format("-" * len(headers.HEADERS[0]), "-" * len(headers.HEADERS[1]), '-' * len(headers.HEADERS[2]),
        '-' * len(headers.HEADERS[3]), '-' * len(headers.HEADERS[4]), '-' * len(headers.HEADERS[5]), '-' * len(headers.HEADERS[6]),
        '-' * len(headers.HEADERS[7]), '-' * len(headers.HEADERS[8])))
    

    for row in table_data:
        print(table_space.format(*row))

    print('\n')    
        
    file_name_pattern = 'Report_{0}_{1}{2}.csv'    
    file_name = file_name_pattern.format(date.today(),datetime.today().hour, datetime.today().minute)
    file_name_created = ReportClass.create_report_file(file_name, headers.HEADERS, table_data)    
    print('File created ' + file_name_created)


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


def get_pull_request_comments(token, repo_name, pull_request_id):
    request = urllib.request.Request(
        'http://wzgdcvaleja01pr:7990/rest/ui/latest/projects/WZAPP/repos/{}/pull-requests/{}/comments?limit=1000'.format(repo_name, pull_request_id))
    request.add_header('Authorization', 'Bearer {}'.format(token))

    response = urllib.request.urlopen(request)

    return response.read().decode('utf-8')


def parse_pull_request_comments(json_text):
    data = json.loads(json_text, object_hook=lambda d: SimpleNamespace(**d))

    return list(map(lambda pr: PullRequestComment(
        pr.id,
        pr.text,
    ),
        data.values))
