import logging
from typing import Optional, Sequence, List

from sqlalchemy import select, delete, update, desc, bindparam, text, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio.engine import AsyncConnection
from sqlalchemy.engine.row import RowMapping

from tgbot.database import User, Admin, Address, Comment

logger = logging.getLogger(__name__)


class Repo:
    """Db abstraction layer"""

    def __init__(self, conn: AsyncConnection):
        self.conn = conn

    # users
    async def add_user(
        self,
        user_id: int,
        firstname: str,
        lastname: Optional[str] = None,
        username: Optional[str] = None,
    ) -> None:
        """Store user in DB, on conflict updates user information"""
        stmt = (
            insert(User)
            .values(
                id=user_id,
                firstname=firstname,
                lastname=lastname,
                username=username,
            )
            .on_conflict_do_update(
                constraint=User.__table__.primary_key,
                set_=dict(
                    firstname=firstname,
                    lastname=lastname,
                    username=username,
                ),
            )
        )

        await self.conn.execute(stmt)
        await self.conn.commit()
        return

    async def get_user(self, user_id: int) -> Optional[RowMapping]:
        """Returns user from DB by user id"""
        stmt = select(User).where(User.id == user_id)

        res = await self.conn.execute(stmt)
        return res.mappings().one_or_none()

    async def list_users(self) -> Sequence[RowMapping]:
        """List all bot users"""
        stmt = select(User).order_by(User.created_on)

        res = await self.conn.execute(stmt)
        return res.mappings().all()

    # admins
    async def add_admin(self, user_id: int, sudo: bool = False) -> None:
        """Store admin in DB, ignore duplicates

        :param user_id: User telegram id
        :type user_id: int
        :param sudo: Super user privileges
        :type sudo: bool
        """
        stmt = insert(Admin).values(id=user_id, sudo=sudo).on_conflict_do_nothing()

        await self.conn.execute(stmt)
        await self.conn.commit()
        return

    async def set_admin_sudo(self, user_id: int, sudo: bool) -> None:
        """Set admin sudo status

        :param user_id: User telegram id
        :type user_id: int
        :param sudo: Super user privileges
        :type sudo: bool
        """
        stmt = update(Admin).values(sudo=sudo).where(Admin.id == user_id)

        await self.conn.execute(stmt)
        await self.conn.commit()
        return

    async def is_admin(self, user_id: int) -> Optional[RowMapping]:
        """Checks user is admin or not

        :param user_id: User telegram id
        :type user_id: int
        :return: User is admin boolean
        :rtype: bool
        """
        stmt = select(Admin).where(Admin.id == user_id)

        res = await self.conn.execute(stmt)
        res = res.mappings().one_or_none()
        return res

    async def del_admin(self, user_id: int) -> None:
        """Delete admin from DB by user id

        :param user_id: User telegram id
        :type user_id: int
        :return: Deleted row count
        :rtype: int
        """
        stmt = delete(Admin).where(Admin.id == user_id)

        await self.conn.execute(stmt)
        await self.conn.commit()

    async def get_admin(self, user_id: int) -> Optional[RowMapping]:
        """Returns admin from DB by user id"""
        stmt = select(Admin).where(Admin.id == user_id)

        res = await self.conn.execute(stmt)
        return res.mappings().one_or_none()

    async def list_admins(self) -> Sequence[RowMapping]:
        """List all bot admins"""
        stmt = (
            select(Admin).order_by(Admin.sudo.desc()).order_by(Admin.updated_on.desc())
        )

        res = await self.conn.execute(stmt)
        return res.mappings().all()

    # Comment
    async def add_comment(self, user_id: int, address_id: int, text: str) -> None:
        stmt = insert(Comment).values(user_id=user_id, address_id=address_id, text=text)

        await self.conn.execute(stmt)
        await self.conn.commit()
        return

    async def list_comment(self, address_id: int) -> Sequence[RowMapping]:
        stmt = (
            select(Comment, User.firstname, User.lastname, User.username)
            .join(User, Comment.user_id == User.id)
            .where(Comment.address_id == address_id)
            .order_by(desc(Comment.created_on))
            .limit(5)
        )

        res = await self.conn.execute(stmt)
        return res.mappings().all()

    # Address
    async def add_address(self, addresses: List[dict]) -> None:
        stmt = (
            insert(Address)
            .values(
                id=bindparam("id"),
                tip=bindparam("tip"),
                number=bindparam("number"),
                place=bindparam("place"),
                birka=bindparam("birka"),
                comment=bindparam("comment"),
                gps=bindparam("gps"),
                copy_box_number=bindparam("copy_box_number"),
            )
            .on_conflict_do_update(
                constraint=Address.__table__.primary_key,
                set_=dict(
                    tip=bindparam("tip"),
                    number=bindparam("number"),
                    place=bindparam("place"),
                    birka=bindparam("birka"),
                    comment=bindparam("comment"),
                    gps=bindparam("gps"),
                    copy_box_number=bindparam("copy_box_number"),
                ),
            )
        )

        await self.conn.execute(stmt, addresses)
        await self.conn.commit()
        return

    async def get_address(self, address_id: int) -> Optional[RowMapping]:
        stmt = select(Address).where(Address.id == address_id)

        res = await self.conn.execute(stmt)
        return res.mappings().one_or_none()

    async def search_address(self, query: str) -> Sequence[RowMapping]:
        stmt = text(
            """
            SELECT 
                *, 
                SIMILARITY(address.place, :query) as place_score 
            FROM address
            WHERE 
                address.place ILIKE :query || '%' OR
                SIMILARITY(address.place, :query) > 0.1
            ORDER BY place_score DESC NULLS LAST;
            """
        ).params(query=query)

        res = await self.conn.execute(stmt)
        return res.mappings().all()
