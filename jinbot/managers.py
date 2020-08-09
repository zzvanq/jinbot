from abc import ABC, abstractmethod
from io import BytesIO
import typing

import aiohttp
from aioredis.commands import Redis
from vkbottle import Message, Bot
from vkbottle.utils.exceptions import VKError


class AbstractManager(ABC):
    # String that used as a prefix for key in DB
    prefix = NotImplemented

    @staticmethod
    @abstractmethod
    def send_message(bot, msg: Message, text: str):
        ...

    @staticmethod
    @abstractmethod
    def send_image(bot, msg: Message, url: str, text: str):
        ...


class VKManager(AbstractManager):
    prefix = "VK"

    @staticmethod
    async def get_or_create_image(bot: Bot, peer_id: int, url: str) -> typing.Optional[str]:
        """
        Try to find image-url cached in DB, make request and cache otherwise

        :param bot: VkBot object
        :type bot: Bot
        :param peer_id: ID of user, that will get this image
        :type peer_id: int
        :param redis: Connection to DB object
        :type redis: Redis
        :param url: URL of image
        :type url: str
        :return: VK url of image
        :rtype: str, optional
        """
        try:
            async with aiohttp.ClientSession() as sess:
                async with sess.get(url) as resp:
                    fp = BytesIO(await resp.read())
                    setattr(fp, "name", "image.png")
                    image = await bot.uploader.upload_message_photo(fp, peer_id=peer_id)
                    fp.close()

                    return image
        except VKError:
            return None

    @staticmethod
    async def send_message(bot: Bot, msg: Message, text: str):
        try:
            await msg(text)
        except VKError:
            pass

    @staticmethod
    async def send_image(bot: Bot, msg: Message, url: str, text: str = None):
        """
        Get image by url, upload it to VK and send to user

        :param bot: VkBot object
        :type bot: Bot
        :param msg: Users message object
        :type msg: Message
        :param url: Url to image
        :type url: str
        :param text: Text of users message
        :type text: str, optional
        """
        image = await VKManager.get_or_create_image(bot=bot, peer_id=msg.peer_id, url=url)
        if image:
            try:
                if text:
                    await msg(message=text, attachment=image)

                else:
                    await msg(attachment=image)

            except VKError:
                pass
