from DashaBot.modules.helper_funcs.chat_status import user_admin
from DashaBot.modules.disable import DisableAbleCommandHandler
from DashaBot import dispatcher

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ParseMode, Update
from telegram.ext.dispatcher import run_async
from telegram.ext import CallbackContext, Filters, CommandHandler

MARKDOWN_HELP = f"""
Markdown is a very powerful formatting tool supported by telegram. {dispatcher.bot.first_name} has some enhancements, to make sure that \
saved messages are correctly parsed, and to allow you to create buttons.

- <code>_italic_</code>: wrapping text with '_' will produce italic text
- <code>*bold*</code>: wrapping text with '*' will produce bold text
- <code>`code`</code>: wrapping text with '`' will produce monospaced text, also known as 'code'
- <code>[sometext](someURL)</code>: this will create a link - the message will just show <code>sometext</code>, \
and tapping on it will open the page at <code>someURL</code>.
<b>Example:</b><code>[test](example.com)</code>

- <code>[buttontext](buttonurl:someURL)</code>: this is a special enhancement to allow users to have telegram \
buttons in their markdown. <code>buttontext</code> will be what is displayed on the button, and <code>someurl</code> \
will be the url which is opened.
<b>Example:</b> <code>[This is a button](buttonurl:example.com)</code>

If you want multiple buttons on the same line, use :same, as such:
<code>[one](buttonurl://example.com)
[two](buttonurl://google.com:same)</code>
This will create two buttons on a single line, instead of one button per line.

Keep in mind that your message <b>MUST</b> contain some text other than just a button!
"""


@run_async
@user_admin
def echo(update: Update, context: CallbackContext):
    args = update.effective_message.text.split(None, 1)
    message = update.effective_message

    if message.reply_to_message:
        message.reply_to_message.reply_text(
            args[1], parse_mode="MARKDOWN", disable_web_page_preview=True
        )
    else:
        message.reply_text(
            args[1], quote=False, parse_mode="MARKDOWN", disable_web_page_preview=True
        )
    message.delete()


def markdown_help_sender(update: Update):
    update.effective_message.reply_text(MARKDOWN_HELP, parse_mode=ParseMode.HTML)
    update.effective_message.reply_text(
        "Try forwarding the following message to me, and you'll see, and Use #test!"
    )
    update.effective_message.reply_text(
        "/save test This is a markdown test. _italics_, *bold*, code, "
        "[URL](example.com) [button](buttonurl:github.com) "
        "[button2](buttonurl://google.com:same)"
    )


@run_async
def markdown_help(update: Update, context: CallbackContext):
    if update.effective_chat.type != "private":
        update.effective_message.reply_text(
            "Contact me in pm",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Markdown help",
                            url=f"t.me/{context.bot.username}?start=markdownhelp",
                        )
                    ]
                ]
            ),
        )
        return
    markdown_help_sender(update)


__help__ = """
*Commands for Anyone:*
- `/markdownhelp`*:* Quick summary of how markdown works in telegram - can only be called in private chats
- `/paste`*:* Saves replied content to `nekobin.com` and replies with a url

*Commands for Bot Owner:*
`/ping`*:* gets ping time of bot to telegram server
`/broadcastall`*:* Broadcasts everywhere
`/broadcastusers`*:* Broadcasts too all users
`/broadcastgroups`*:* Broadcasts too all groups
`/groups`*:* List the groups with Name, ID, members count as a txt
`/leave <ID>`*:* Leave the group, ID must have hyphen
`/stats`*:* Shows overall bot stats
`/getchats`*:* Gets a list of group names the user has been seen in.
`/ginfo username/link/ID`*:* Pulls info panel for entire group
`/ignore`*:* Blacklists a user from using the bot entirely
`/lockdown <off/on>`*:* Toggles bot adding to groups
`/notice`*:* Removes user from blacklist
`/ignoredlist`*:* Lists ignored users
`/listmodules`*:* Prints modules and their names
`/unload <name>`*:* Unloads module dynamically
`/load <name>`*:* Loads module
`/speedtest`*:* Runs a speedtest and gives you 2 options to choose from, text or image output
`/rban user group`*:* Remote ban
`/runban user group`*:* Remote un-ban
`/rkick user group`*:* Remote punch
`/rmute user group`*:* Remote mute
`/runmute user group`*:* Remote un-mute
`/reboot`*:* Restarts the bots service
`/gitpull`*:* Pulls the repo and then restarts the bots service
`/debug <on/off>`*:* Logs commands to updates.txt
`/logs`*:* Run this in support group to get logs in pm
`/eval`*:* Self explanatory
`/sh`*:* Runs shell command
`/shell`*:* Runs shell command
`/clearlocals`*:* As the name goes
`/dbcleanup`*:* Removes deleted accs and groups from db
`/py`*:* Runs python code
`/gban <id> <reason>`*:* Gbans the user, works by reply too
`/ungban`*:* Ungbans the user, same usage as gban
`/gbanlist`*:* Outputs a list of gbanned users
"""

ECHO_HANDLER = DisableAbleCommandHandler("echo", echo, filters=Filters.group)
MD_HELP_HANDLER = CommandHandler("markdownhelp", markdown_help)

dispatcher.add_handler(ECHO_HANDLER)
dispatcher.add_handler(MD_HELP_HANDLER)

__mod_name__ = "Extras"
__command_list__ = ["id", "echo"]
__handlers__ = [
    ECHO_HANDLER,
    MD_HELP_HANDLER,
]
