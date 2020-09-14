admin_nickname = 'mezgoodle'
no_association = 'NONE'
label_name = 'needs review'
bot_name = 'mezgoodle-bot'
test_ref = 'backport-17ab8f0-3.7'
test_repo_name = 'some_name'
test_number = 5772
issue_url = 'https://api.github.com/issue/123'
test_data_pr = {
    'action': 'opened',
    'pull_request': {
        'number': test_number,
        'author_association': 'owner',
        'issue_url': issue_url,
        'state': 'closed',
        'labels': 'labels'
    },
    'sender': {'login': admin_nickname}
}
test_data_pr_1 = {
    'action': 'closed',
    'pull_request': {
        'number': test_number,
        'user': {'login': bot_name},
        'merged': True,
        'merged_by': {'login': admin_nickname},
        'head': {
            'ref': test_ref, 'user': {'login': admin_nickname},
            'repo': {'name': test_repo_name}
        },
        'issue_url': issue_url,
        'state': 'closed',
    },
}
test_data_pr_2 = {
    'action': 'closed',
    'pull_request': {
        'number': test_number,
        'user': {'login': bot_name},
        'merged': False,
        'merged_by': {'login': None},
        'head': {
            'ref': test_ref, 'user': {'login': admin_nickname},
            'repo': {'name': test_repo_name}
        },
        'issue_url': issue_url,
        'state': 'closed',
    },
}
test_data_issues = {
    'action': 'created',
    'comment': {
        'url': issue_url,
    },
    'sender': {'login': admin_nickname}
}
test_data_installation = {
    'action': 'created',
    'repositories': [{'full_name': bot_name}],
    'sender': {'login': admin_nickname}
}
