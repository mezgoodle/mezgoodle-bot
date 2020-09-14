"""All constants in project"""

ADMIN_NICKNAME = 'mezgoodle'
NO_ASSOCIATION = 'NONE'
LABEL_NAME = 'needs review'
BOT_NAME = 'mezgoodle-bot'
TEST_REF = 'backport-17ab8f0-3.7'
TEST_REPO_NAME = 'some_name'
TEST_NUMBER = 5772
ISSUE_URL = 'https://api.github.com/issue/123'
TEST_DATA_PR = {
    'action': 'opened',
    'pull_request': {
        'number': TEST_NUMBER,
        'author_association': 'owner',
        'issue_url': ISSUE_URL,
        'state': 'closed',
        'labels': 'labels'
    },
    'sender': {'login': ADMIN_NICKNAME}
}
TEST_DATA_PR_1 = {
    'action': 'closed',
    'pull_request': {
        'number': TEST_NUMBER,
        'user': {'login': BOT_NAME},
        'merged': True,
        'merged_by': {'login': ADMIN_NICKNAME},
        'head': {
            'ref': TEST_REF, 'user': {'login': ADMIN_NICKNAME},
            'repo': {'name': TEST_REPO_NAME}
        },
        'issue_url': ISSUE_URL,
        'state': 'closed',
    },
}
TEST_DATA_PR_2 = {
    'action': 'closed',
    'pull_request': {
        'number': TEST_NUMBER,
        'user': {'login': BOT_NAME},
        'merged': False,
        'merged_by': {'login': None},
        'head': {
            'ref': TEST_REF, 'user': {'login': ADMIN_NICKNAME},
            'repo': {'name': TEST_REPO_NAME}
        },
        'issue_url': ISSUE_URL,
        'state': 'closed',
    },
}
TEST_DATA_ISSUES = {
    'action': 'created',
    'comment': {
        'url': ISSUE_URL,
    },
    'sender': {'login': ADMIN_NICKNAME}
}
TEST_DATA_INSTALLATION = {
    'action': 'created',
    'repositories': [{'full_name': BOT_NAME}],
    'sender': {'login': ADMIN_NICKNAME}
}
HEADERS = {'x-github-event': 'ping', 'x-github-delivery': '1234'}
