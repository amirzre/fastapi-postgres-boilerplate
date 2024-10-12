from uuid import UUID

from app.models import User
from core.repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    User repository provides all the database operations for the User model.
    """

    async def get_by_email(self, email: str) -> User | None:
        """
        Get user by email.

        :param email: Email.
        :return: User.
        """
        query = self._query()
        query = query.filter(User.email == email)

        return await self._one_or_none(query)

    async def get_by_uuid(self, uuid: UUID) -> User | None:
        """
        Get user by uuid.

        :param uuid: User uuid.
        :return: User.
        """
        query = self._query()
        query = query.filter(User.uuid == uuid)

        return await self._one_or_none(query)
