
class UnitOfWork:
    def __init__(self, session, repository_cls):
        self._session_factory = session
        self._repository_cls = repository_cls

    async def __aenter__(self):
        self._session = self._session_factory()
        self.repo = self._repository_cls(self._session)
    
    async def __aexit__(self, *args):
        await self._session.close()
    
    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()