import requests
import json
import re


# *** Globals
server_regex = re.compile(
    '[{"translated_theme_name":"[\s\S]*","urlWs":"https:\\\/\\\/srv[0-9]+\.akinator\.com:[0-9]+\\\/ws","subject_id":"[0-9]+"}]'
)


def auto_get_region():
    """Automatically get the `uri` and `server` from akinator.com for the specified language and theme"""

    uri_ = "ru.akinator.com"

    response = requests.get("https://" + uri_)
    match = server_regex.search(response.text)

    parsed = json.loads(match.group().split("'arrUrlThemesToPlay', ")[-1])

    return {
        "uri": uri_,
        "server": next((i for i in parsed if i["subject_id"] == "1"), None)[
            "urlWs"
        ],
    }


def init_akinator():
    """Initialize global variables, that contain Akinator `uri` and `server` information"""
    global uri, server
    region_info = auto_get_region()
    if region_info:
        uri, server = region_info["uri"], region_info["server"]

# Globals ***


# *** Game settings
# Answer texts ---
ANSWER_YES_TEXT = "Да"
ANSWER_YES_TEXT_LOWER = ANSWER_YES_TEXT.lower()
ANSWER_YES_NUM = "1"

ANSWER_NO_TEXT = "Нет"
ANSWER_NO_TEXT_LOWER = ANSWER_NO_TEXT.lower()
ANSWER_NO_NUM = "2"

ANSWER_DONT_KNOW_TEXT = "Не знаю"
ANSWER_DONT_KNOW_TEXT_LOWER = ANSWER_DONT_KNOW_TEXT.lower()
ANSWER_DONT_KNOW_NUM = "3"

ANSWER_PROBABLY_YES_TEXT = "Возможно, частично"
ANSWER_PROBABLY_YES_TEXT_LOWER = ANSWER_PROBABLY_YES_TEXT.lower()
ANSWER_PROBABLY_YES_NUM = "4"

ANSWER_PROBABLY_NO_TEXT = "Скорее нет, не совсем"
ANSWER_PROBABLY_NO_TEXT_LOWER = ANSWER_PROBABLY_NO_TEXT.lower()
ANSWER_PROBABLY_NO_NUM = "5"

ANSWER_BACK_TEXT = "Назад"
ANSWER_BACK_TEXT_LOWER = ANSWER_BACK_TEXT.lower()
ANSWER_BACK_NUM = "6"
ANSWER_BACK = [ANSWER_BACK_TEXT, ANSWER_BACK_TEXT_LOWER, ANSWER_BACK_NUM]

ANSWER_RESTART_TEXT = "Начать заново"
ANSWER_RESTART_TEXT_LOWER = ANSWER_RESTART_TEXT.lower()
ANSWER_RESTART_NUM = "7"

ANSWER_CONTINUE_TEXT = "Продолжить"
ANSWER_CONTINUE_TEXT_LOWER = ANSWER_CONTINUE_TEXT.lower()
ANSWER_CONTINUE_NUM = "8"

ANSWER_START_TEXT = "Начать"
ANSWER_RESTART_UPPER = [ANSWER_START_TEXT, ANSWER_RESTART_TEXT, "Заново", "Играть", "Давай", "Привет", "Го", "Гоу", "Поехали"]
ANSWER_RESTART_LOWER = [item.lower() for item in ANSWER_RESTART_UPPER]
ANSWER_RESTART_OTHER = [ANSWER_RESTART_NUM]

# List of answers for Restart
ANSWER_RESTART = ANSWER_RESTART_UPPER + ANSWER_RESTART_LOWER + ANSWER_RESTART_OTHER

ANSWER_WRONG_TEXT = "Неправильно"
ANSWER_CONTINUE_UPPER = [ANSWER_CONTINUE_TEXT, ANSWER_WRONG_TEXT]
ANSWER_CONTINUE_LOWER = [item.lower() for item in ANSWER_CONTINUE_UPPER]
ANSWER_CONTINUE_OTHER = [ANSWER_CONTINUE_NUM]

# List of answers for Start
ANSWER_CONTINUE = ANSWER_CONTINUE_UPPER + ANSWER_CONTINUE_LOWER + ANSWER_CONTINUE_OTHER

# Human answers related to Akinator answer codes
ANSWERS = {
    ANSWER_YES_TEXT: "0",
    ANSWER_YES_TEXT_LOWER: "0",
    ANSWER_YES_NUM: "0",

    ANSWER_NO_TEXT: "1",
    ANSWER_NO_TEXT_LOWER: "1",
    ANSWER_NO_NUM: "1",

    ANSWER_DONT_KNOW_TEXT: "2",
    ANSWER_DONT_KNOW_TEXT_LOWER: "2",
    ANSWER_DONT_KNOW_NUM: "2",

    ANSWER_PROBABLY_YES_TEXT: "3",
    ANSWER_PROBABLY_YES_TEXT_LOWER: "3",
    ANSWER_PROBABLY_YES_NUM: "3",

    ANSWER_PROBABLY_NO_TEXT: "4",
    ANSWER_PROBABLY_NO_TEXT_LOWER: "4",
    ANSWER_PROBABLY_NO_NUM: "4",
}
# --- Answer texts

# Message texts ---
MESSAGE_INTERFACE = f"1) {ANSWER_YES_TEXT}\n" \
                    f"2) {ANSWER_NO_TEXT}\n" \
                    f"3) {ANSWER_DONT_KNOW_TEXT}\n" \
                    f"4) {ANSWER_PROBABLY_YES_TEXT}\n" \
                    f"5) {ANSWER_PROBABLY_NO_TEXT}\n\n" \
                    f"6) {ANSWER_BACK_TEXT}\n" \
                    f"7) {ANSWER_RESTART_TEXT}"


TEXT_VICTORY = "Я думаю... Это:\n" \
               "{name} ({description})\n\n" \
              f"6) {ANSWER_BACK_TEXT}\n" \
              f"7) {ANSWER_RESTART_TEXT}\n" \
              f"8) {ANSWER_WRONG_TEXT}, {ANSWER_CONTINUE_TEXT_LOWER}\n"

TEXT_VICTORY_WO_CONTINUE = "Я думаю... Это:\n" \
                           "{name} ({description})\n\n" \
                          f"6) {ANSWER_BACK_TEXT}\n" \
                          f"7) {ANSWER_RESTART_TEXT}\n"

TEXT_QUESTION = "Вопрос №{step}\n" \
                "Прогресс: {progression}\n" \
                "➖➖➖➖➖\n" \
                "{question}\n" \
                "➖➖➖➖➖\n" \
                + MESSAGE_INTERFACE

TEXT_UNKNOWN_COMMAND = f"Неизвестная команда\n" \
                       f"Чтобы начать, напишите \"{ANSWER_START_TEXT}\""

TEXT_JOINED = "Ну что, начнём? 😏"
TEXT_CHAT_INVITE = TEXT_JOINED + "\nОбращайтесь ко мне через @{group_id}"
TEXT_LEFT = "Уже уходишь? 😢"
TEXT_DEFEATED = f"Ты победил, я принимаю поражение 🤕\n" \
                f"7) {ANSWER_RESTART_TEXT}"

TEXT_DEFEATED_CONTINUE = f"{TEXT_DEFEATED}\n" \
                         f"8) {ANSWER_CONTINUE_TEXT}"

TEXT_SESSION_EXPIRED = "Тебя слишком долго не было, и я забыл твои ответы 😞\n"
TEXT_SERVER_DOWN = "Бот приболел и ему нужно немного отдохнуть 🤒\n"
TEXT_ANSWER_ERROR = "Произошла ошибка, попробуй ещё раз 🤒\n"
# --- Message texts
# Game settings ***


# *** Session settings
SESSION_EXPIRE_TIME = 60 * 60 * 24 * 2  # 2 Days
SESSION_PROGRESS_MIN_STEP_UNSURE_VICTORY = 25  # Min step needed to win with unsure victory progression
SESSION_PROGRESS_UNSURE_VICTORY = 90  # Unsure victory progression
SESSION_PROGRESS_SURE_VICTORY = 95  # Sure victory progression
SESSION_MAX_STEPS_FIRST = 40  # First checkpoint when suggested defeat
SESSION_MAX_STEPS_SECOND = 60  # Second checkpoint when suggested defeat
SESSION_PROGRESS_DEFEAT = 60  # Defeat if step is equal either to first checkpoint or second
SESSION_MAXIMUM_PROGRESSION = 98  # If progression more or equal and guess is repeating then Defeated
# Session settings ***


# *** Akinator settings
AKINATOR_CHILD_MODE = "false"
AKINATOR_MAX_STEPS = 80

# URLs for the API requests
NEW_SESSION_URL = "https://{}/new_session?callback=jQuery331023608747682107778_{}&urlApiWs={}&partner=1&childMod={}&player=website-desktop&uid_ext_session={}&frontaddr={}&constraint=ETAT<>'AV'&soft_constraint={}&question_filter={}"
ANSWER_URL = "https://{}/answer_api?callback=jQuery331023608747682107778_{}&urlApiWs={}&childMod={}&session={}&signature={}&step={}&answer={}&frontaddr={}&question_filter={}"
BACK_URL = "{}/cancel_answer?callback=jQuery331023608747682107778_{}&childMod={}&session={}&signature={}&step={}&answer=-1&question_filter={}"
WIN_URL = "{}/list?callback=jQuery331023608747682107778_{}&childMod={}&session={}&signature={}&step={}"

# HTTP headers to use for the requests
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap"
        " Chromium/81.0.4044.92 Chrome/81.0.4044.92 Safari/537.36"
    ),
    "x-requested-with": "XMLHttpRequest",
}
# Akinator settings ***


# *** Admin settings
# Admin command texts ---
ADMIN_COMMAND_PREFIX = "//"
ADMIN_UNKNOWN_COMMAND_TEXT = "Команда должна начинаться с redis или notify\n\n" \
                             "Например:\n\n" \
                             "Очистить БД\n" \
                             "//redis.flushall()\n\n" \
                             "Получить количество записей в БД\n" \
                             "//redis.dbsize()\n\n" \
                             "Разослать сообщение\n" \
                             "//notify-{filter}-{max_users}-{min_age}-{earlier} Сообщение\n" \
                             "filter - all, unread, unanswered, important\n\n" \
                             "max_users - Количество пользователей, которым отправится сообщение\n\n" \
                             "min_age - Минимальная давность последнего сообщения пользователя в секундах\n\n" \
                             "earlier - Если 1, то отправить только тем у кого последнее собщение старше min_age. Если 0, то моложе"

ADMIN_COMMAND_START_TEXT = "Команда \"{command}\" запущена..."
ADMIN_COMMAND_END_TEXT = "Команда \"{command}\" завершена"
# --- Admin command texts

# Admin command timeouts ---
ADMIN_TIMEOUT_NOTIFY = 2  # Seconds
ADMIN_TIMEOUT_API = 5  # Seconds
# --- Admin command timeouts

# Send message command defaults ---
ADMIN_COMMAND_SEND_MESSAGE_MIN_AGE_DEFAULT = 60 * 60 * 24 * 2  # 1 Day
ADMIN_COMMAND_SEND_MESSAGE_FILTER_DEFAULT = "all"  # all, unread, unanswered, important
ADMIN_COMMAND_SEND_MESSAGE_EARLIER_DEFAULT = 1  # 0 Younger than min age, 1 Older
# --- Send message command defaults

# After startup message settings ---
ADMIN_COMMAND_SEND_MESSAGE_RESTART_MAX_USERS = 400  # Amount of users that will get restart message
ADMIN_COMMAND_SEND_MESSAGE_RESTART_FILTER = "all"  # all, unread, unanswered, important
ADMIN_COMMAND_SEND_MESSAGE_RESTART_MIN_AGE = 60 * 2  # 2 Minutes
ADMIN_COMMAND_SEND_MESSAGE_RESTART_ENDED_TEXT = "Бот перезапустился, ещё пару секунд и будет готов 🥳"  # Restart message text
ADMIN_COMMAND_SEND_MESSAGE_RESTART_EARLIER = 0  # 0 Younger than min age, 1 Older
# --- After startup message settings
# Admin settings ***


# *** Other settings
DEBUG = False
VK_GROUP_ID = "bot_jin"
if DEBUG:
    REDIS_HOST = "127.0.0.1"
else:
    REDIS_HOST = "redis"
# Other settings ***
