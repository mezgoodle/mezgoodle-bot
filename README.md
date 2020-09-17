# mezgoodle-bot

[![Language](https://img.shields.io/badge/language-python-brightgreen?style=flat-square)](https://www.python.org/)

Hello everyone! This is the repository of my GitHub bot on Python.

## Table of contents

- [Table of contents](#table-of-contents)
- [Motivation](#motivation)
- [Build status](#build-status)
- [Badges](#badges)
- [Code style](#code-style)
- [Tech/framework used](#techframework-used)
- [Features](#features)
- [Code Example](#code-example)
- [API Example](#api-example)
- [Tests](#tests)
- [Installation](#installation)
- [Fast usage](#fast-usage)
- [API](#api)
- [Contribute](#contribute)
- [Credits](#credits)
- [License](#license)

## Motivation

Once upon a time I was at a lecture in Kyiv where I was shown how to do GitHub bot, but then nothing came of it. So I decided to try **again**. Here the bot is :relaxed:

## Build status

Here you can see build status of [continuous integration](https://en.wikipedia.org/wiki/Continuous_integration):

[![Build Status](https://travis-ci.com/mezgoodle/mezgoodle-bot.svg?branch=master)](https://travis-ci.com/mezgoodle/mezgoodle-bot)
![Lint Markdown files](https://github.com/mezgoodle/mezgoodle-bot/workflows/Lint%20Markdown%20files/badge.svg)

## Badges

Other badges

[![Platform](https://img.shields.io/badge/Platform-GitHub-brightgreen?style=flat-square)](https://www.github.com)
![GitHub last commit](https://img.shields.io/github/last-commit/mezgoodle/mezgoodle-bot?style=flat-square)
[![API](https://img.shields.io/badge/GitHub_API-v3-brightgreen?style=flat-square)](https://developer.github.com/v3/)


## Code style

I'm using [Codacy](https://www.codacy.com/) for automate my code quality.

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/a2953a4086c847fa80278ffd2dc4186b)](https://www.codacy.com/manual/mezgoodle/mezgoodle-bot?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mezgoodle/mezgoodle-bot&amp;utm_campaign=Badge_Grade)

## Tech/framework used

**Built with**

- [Python](https://www.python.org/)
- [AIOHTTP](https://docs.aiohttp.org/en/stable/)
- [gidgethub](https://gidgethub.readthedocs.io/en/latest/)

## Features

Bot can **response** on *installation*, *opening* and *closing* pull-requests and issues.

## Code Example

- Response on installation

```python
"""Installation the bot trigger"""

import gidgethub.routing

from .utils import get_info

router = gidgethub.routing.Router()


@router.register('installation', action='created')
async def repo_installation_added(event, gh, *args, **kwargs):
    """Installed bot to repository"""
    token = await get_info(event, gh)
    sender_name = event.data['sender']['login']
    for repo in event.data['repositories']:

        repo_full_name = repo['full_name']
        if token is not None:
            response = await gh.post(
                f'/repos/{repo_full_name}/issues',
                data={
                    'title': 'Thanks for installing me!',
                    'body': f'You are the best! @{sender_name}\n Also my creator is @mezgoodle. \
                    There you can find my body)'
                },
                oauth_token=token['token'],
            )
            issue_url = response['url']
            await gh.patch(
                issue_url,
                data={'state': 'closed'},
                oauth_token=token['token'],
            )
        else:
            await gh.post(f'/repos/{repo_full_name}/issues')
```

## API Example

In the folder `examples` you can see how to work with **GitHub API** directly *without* **GitHub App**. [Link](https://github.com/mezgoodle/mezgoodle-bot/blob/master/examples) to the folder.

## Tests

All tests are in [tests](https://github.com/mezgoodle/mezgoodle-bot/tree/master/tests) folder. The results from **Travis CI** are [here](https://travis-ci.com/github/mezgoodle/mezgoodle-bot).

## Installation

1. Clone this repository

```bash
git clone https://github.com/mezgoodle/mezgoodle-bot.git
```

2. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages.

```bash
pip install -r requirements.txt
```

3. Rename `.env_sample` to `.env` and set environment variables like or export them like:

- In Unix / Mac OS:

```bash
export GH_AUTH=your token
```

- In Windows:

```bash
set GH_AUTH=your token
```

## Fast usage

Firstly, add or change functions in `__main__.py`, change some values, such as messages or emojies. Then launch the script:

- Linux, MacOS:

```bash
python3 -m webservice
```

- Windows:

```bash
python -m webservice
```

## API

Here I am using [GitHub API](https://developer.github.com/v3/). Also look at the [Webhook event payloads](https://developer.github.com/webhooks/event-payloads/).

## Contribute

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Also look at the [CONTRIBUTING.md](https://github.com/mezgoodle/mezgoodle-bot/blob/master/CONTRIBUTING.md).

## Credits

Links to video and repos which inspired me to build this project:

- [Video](https://www.youtube.com/watch?v=JWhywJHIMfs)
- [Documentation](https://github-app-tutorial.readthedocs.io/en/latest/index.html)
- [Tutorial repository](https://github.com/Mariatta/github-app-tutorial)

## License

MIT © [mezgoodle](https://github.com/mezgoodle)
