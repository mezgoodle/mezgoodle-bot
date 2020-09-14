admin_nickname = 'mezgoodle'
no_association = 'NONE'
label_name = 'needs review'
bot_name = 'mezgoodle-bot'
test_ref = 'backport-17ab8f0-3.7'
test_repo_name = 'some_name'
test_number = 5772
issue_url = 'https://api.github.com/issue/123'
test_data = {
    'action': 'closed',
    'pull_request': {
        'number': consts.test_number,
        'user': {'login': consts.bot_name},
        'merged': True,
        'merged_by': {'login': consts.admin_nickname},
        'head': {
            'ref': consts.test_ref, 'user': {'login': consts.admin_nickname},
            'repo': {'name': consts.test_repo_name}
        },
        'issue_url': consts.issue_url,
        'state': 'closed',
    },
}
