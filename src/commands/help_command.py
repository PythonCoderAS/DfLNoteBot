from discord import Embed
from discord.ext.commands import Bot, DefaultHelpCommand

description = """This short guide will help you get started with the bot.

Notes have metadata and the message. Metadata can be specified in the following form:

```
/note extra:name=value[;anothername=anothervalue][;...] message:The message for the note
```

There are also a few predefined metadata values that allows you to use them in a simpler way:

`chapter:<chapter>` - Used to indicate the chapter the note is for.
`page:<page>` - Used to indicate the current page the note is for.
`panel:<panel>` - Used to indicate the panel the note is for.
`bubble:<bubble>` - Used to indicate the text bubble the note is for.

For example, you could run the following command:

```
/note chapter:1 page:1 panel:1 message: Message
```

It is also possible to make notes that have no metadata.

**__Command List__**:

* `/note` - Create a new note.
* `/view` - View a note.
* `/resolve` - Resolve a note.
* `/edit` - Edit a note.
* `/delete` - Delete a note.
* `/list` - List all notes.
* `/metadata` - Set metadata for a note.
* `/metadata default` - Set default metadata for new notes created in a channel.
* `/metadata list` - List all possible metadata options.
* `dfb help` - Show this help message.
"""


class HelpCommand(DefaultHelpCommand):
    async def send_bot_help(self, mapping):
        # We want to send a predefined embed.
        embed = Embed(title="Help", description=description.strip())
        destination = self.get_destination()
        await destination.send(embed=embed)


def setup(bot: Bot):
    bot.help_command = HelpCommand()
