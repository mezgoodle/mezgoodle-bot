# mezgoodle-bot

[![Build Status](https://img.shields.io/badge/language-python-brightgreen?style=flat-square)](https://www.python.org/)

Hello everyone! This is the repository of my GitHub bot on Python.

## Table of contents

- [Project title](#project-title)
- [Motivation](#motivation)
- [Build status](#build-status)
- [Badges](#badges)
- [Code style](#code-style)
- [Tech/framework used](#tech-framework-used)
- [Features](#features)
- [Code Example](#code-example)
- [API Example](#api-example)
- [Installation](#installation)
- [Fast usage](#fast-usage)
- [API](#api)
- [Contribute](#contribute)
- [Credits](#credits)
- [License](#license)

## Motivation

Once upon a time I was at a lecture in Kyiv where I was shown how to do GitHub bot, but then nothing came of it. So I decided to try **again**. Here the bot are :relaxed:
## Build status

Here you can see build status of [continuous integration](https://en.wikipedia.org/wiki/Continuous_integration):

![Python application](https://github.com/mezgoodle/mezgoodle-bot/workflows/Python%20application/badge.svg)

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

Bot can **response** on *installation*, *opening* pull request, issues *commenting*.

## Code Example

- Response on installation

```python
@router.register("installation", action="created")
async def repo_installation_added(event, gh, *args, **kwargs):
    installation_id = event.data["installation"]["id"]
    installation_access_token = await apps.get_installation_access_token(
        gh,
        installation_id=installation_id,
        app_id=os.environ.get("GH_APP_ID"),
        private_key=os.environ.get("GH_PRIVATE_KEY")
    )
    sender_name = event.data["sender"]["login"]
    for repo in event.data["repositories"]:

        repo_full_name = repo["full_name"]
        response = await gh.post(
            f'/repos/{repo_full_name}/issues',
            data={
                'title': 'Thanks for installing me!',
                'body': f'You are the best! @{sender_name}\n Also my creator is @mezgoodle. There you can find my body)'
            },
            oauth_token=installation_access_token["token"],
        )
        issue_url = response["url"]
        await gh.patch(issue_url,
                       data={"state": "closed"},
                       oauth_token=installation_access_token["token"],
                       )
```

## API Example

In the folder `examples` you can see how to work with **GitHub API** directly *without* **GitHub App**. [Link](https://github.com/mezgoodle/mezgoodle-bot/blob/master/examples/create_issue/create_issue.py) to the file.

## Installation

1. Clone this repository

```bash
git clone https://github.com/mezgoodle/mezgoodle-bot.git
```

2. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages.

```bash
pip install -r requirements.txt
```

3. Set environment variables like:

> Variables in [30](https://github.com/mezgoodle/mezgoodle-bot/blob/master/webservice/__main__.py#L30), [55](https://github.com/mezgoodle/mezgoodle-bot/blob/master/webservice/__main__.py#L55), [56](https://github.com/mezgoodle/mezgoodle-bot/blob/master/webservice/__main__.py#L56) lines.

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

Here I am using [GitHub API](https://developer.github.com/v3/).

## Contribute

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Also look at the [CONTRIBUTING.md](https://github.com/mezgoodle/mezgoodle-bot/blob/master/CONTRIBUTING.md).

> If you want to contribute to this project, so I have problems such as add more examples of work with API and add tests for bot.

## Credits

Links to video and repos which inspired me to build this project:

- [Video](https://www.youtube.com/watch?v=JWhywJHIMfs)
- [Documentation](https://github-app-tutorial.readthedocs.io/en/latest/index.html)

## License

MIT © [mezgoodle](https://github.com/mezgoodle)
