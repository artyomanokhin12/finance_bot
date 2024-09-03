from aiogram import Bot
from aiogram.types import BotCommand

commands: dict[str, str] = {
    "/income": "Внесение строки дохода",
    "/spending": "Внесение строки расхода",
    "/limit": "Добавление или изменение лимита",
    "/stat": "Вывод статистики доходов и расходов за указанный период",
    "/reset": "Удаляет всю инофрмацию о Вас и о ваших доходах/расходах",
    "/saving": "Добавление цели для накоплений",
    "/show_savings": "Показать ваши текущие цели для накопления",
    "/add_saving_money": "Внести сбережения на одну из текущих целей для накопления",
    "/delete_goal": "Удалить одну из текущих целей для накопления",
    "/cancel": "Отмена действия",
}


async def set_main_menu(bot: Bot) -> None:
    main_menu_commands: list[BotCommand] = [
        BotCommand(command=key, description=value) for key, value in commands.items()
    ]
    await bot.set_my_commands(main_menu_commands)
