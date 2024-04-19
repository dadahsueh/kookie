﻿from khl import Bot

from bot.commands import cmd_basic, cmd_rss


def register_cmds(bot: Bot):
    cmd_basic.reg_basic_cmd(bot)
    cmd_rss.reg_rss_cmd(bot)
