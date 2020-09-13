from gidgethub import sansio

from webservice import pr


class FakeGH:
    def __init__(self):
        self.post_data = None

    async def delete(self, url):
        self.delete_url = url


async def test_branch_deleted_when_pr_merged():
    data = {
        "action": "closed",
        "pull_request": {
            "number": 5722,
            "user": {"login": "mezgoodle-bot"},
            "merged": True,
            "merged_by": {"login": "mezgoodle"},
            "head": {"ref": "backport-17ab8f0-3.7"},
        },
    }
    event = sansio.Event(data, event="pull_request", delivery_id="1")

    gh = FakeGH()
    await pr.router.dispatch(event, gh)
    assert gh.post_data is None  # does not leave a comment
    assert (
        gh.delete_url
        == f"/repos/{owner}/{repo}/git/refs/heads/{ref}"
    )
