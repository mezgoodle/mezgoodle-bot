"""Common class for testing"""


class FakeGH:
    """Create fake GitHub object"""

    def __init__(self):
        self.post_data = None
        self.delete_url = None
        self.post_url = None
        self.patch_url = None

    async def delete(self, url):
        """Trigger delete method"""
        self.delete_url = url

    async def post(self, url):
        """Trigger post method"""
        self.post_url = url

    async def patch(self, url):
        """Trigger patch method"""
        self.patch_url = url
