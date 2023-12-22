import gettext
from db import check_locale


async def get_translation(user_id):
    """set gettext.translation to user's language"""
    language = await check_locale(user_id)
    language = ''.join(language)
    language_translations = gettext.translation(domain="bbot", localedir="locale",
                                                languages=[language])
    _ = language_translations.gettext
    return _
