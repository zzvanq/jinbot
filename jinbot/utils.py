import asyncio
import typing
from concurrent.futures import TimeoutError
from json.decoder import JSONDecodeError

from aiohttp import ClientConnectionError
from aioredis.commands import Redis

from jinbot import config
from jinbot.akinator import Akinator


def get_object_key(manager, *object_path: str) -> str:
    """
    Create key for object in DB

    :param manager: Message Manager object
    :type manager: AbstractManager
    :param object_path: Unique ID of object
    :type object_path: str
    :return: Unique key for object
    """
    return "||".join([manager.prefix, *object_path])


async def create_session(
    first_try: bool = True, is_defeated: int = 0, is_started: int = 1
) -> typing.Optional[Akinator]:
    """
    Create session object and start it

    :param first_try: if True, then in case of Error try again, dont try otherwise
    :type first_try: bool, optional
    :param is_defeated: if True, then cant continue game
    :type is_defeated: int, optional
    :param is_started: if True, then game was already started, wait for first message otherwise
    :type is_started: int, optional
    :return: Session object
    :rtype: Akinator, optional
    """
    try:
        session = Akinator(is_defeated=is_defeated, is_started=is_started)
        await session.start_game()

        return session

    except (JSONDecodeError, AttributeError, ClientConnectionError, TimeoutError):
        if first_try:
            # Some problem with Akinator API. Wait a little and try again
            await asyncio.sleep(1)

            return await create_session(first_try=False)
        else:
            return None


async def save_session(session_id: str, session: Akinator, redis: Redis) -> Akinator:
    """
    Dump session object and save it in DB

    :param session_id: Unique ID that used as a key for Session object in DB
    :type session_id: str
    :param session: Session object
    :type session: Akinator
    :param redis: Connection to DB object
    :type redis: Redis
    :return: Session object
    :rtype: Akinator
    """
    session_dump = session.dump_session()
    await redis.hmset_dict(session_id, session_dump)

    return session


async def create_and_save_session(
    session_id: str, redis: Redis, is_defeated: int = 0, is_started: int = 1
) -> typing.Tuple[bool, typing.Optional[Akinator]]:
    """
    Remove session and create new one

    :param session_id: Unique ID that used as a key for Session object in DB
    :type session_id: str
    :param redis: Connection to DB object
    :type redis: Redis
    :param is_defeated: if True, then then cant continue game
    :type is_defeated: int, optional
    :param is_started: if True, then game was already started, wait for first message otherwise
    :type is_started: int, optional
    :return: True if created, False if existed and Session object
    :rtype: tuple(bool, Akinator)
    """
    session = await create_session(is_defeated=is_defeated, is_started=is_started)
    if session:
        await save_session(session_id=session_id, session=session, redis=redis)

        return True, session
    else:
        return False, None


async def get_or_create_session(
    session_id: str, redis: Redis
) -> typing.Tuple[bool, Akinator]:
    """
    Find Session object in DB, create if not founded

    :param session_id: Unique ID that used as a key for Session object in DB
    :type session_id: str
    :param redis: Connection to DB object
    :type redis: Redis
    :return: `True` if created, `False` if existed and Session object
    :rtype: tuple(bool, Akinator)
    """
    session_dump = await redis.hgetall(session_id, encoding="utf-8")

    if session_dump:
        # Founded. Load object
        session = Akinator()
        session.load_session(session_dump)
        created = False
    else:
        # Not founded. Create
        session = await create_session()
        if session:
            await save_session(session_id=session_id, session=session, redis=redis)
            created = True
        else:
            created = False

    return created, session