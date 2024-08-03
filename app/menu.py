from aiogram import Bot
from aiogram.types import BotCommand

commands: dict[str, str] = {
    '/income': 'Внесение строки дохода',
    '/spending': 'Расписание матчей на сегодня',
    '/change_limit': 'Список лучших бомбардиров чемпионата',
    '/stat': 'Выбор любимой команды, информация о которой будет приходить в уведомлениях',
    '/cancel': 'Отмена действия'
}

async def set_main_menu(bot: Bot) -> None:
    main_menu_commands: list[BotCommand]=[
        BotCommand(command=key, description=value) for key, value in commands.items()
    ]
    await bot.set_my_commands(main_menu_commands)