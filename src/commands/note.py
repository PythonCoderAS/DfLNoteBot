from collections import defaultdict

from discord import ApplicationContext, Color, Embed, Option
from discord.ext.commands import Cog, slash_command
from discord.ext.pages import Paginator

from ..bot import defaults
from ..orm import Note
from ..utils import get_metadata, note_representation


class NoteCog(Cog):
    @slash_command(name="note", description="Add a note.")
    async def note(self, ctx: ApplicationContext,
                   message: Option(str, "The message for the note.", required=True),
                   chapter: Option(str, "The chapter for the note.", required=False) = None,
                   page: Option(str, "The page for the note.", required=False) = None,
                   panel: Option(str, "The panel for the note.", required=False) = None,
                   bubble: Option(str, "The bubble for the note.", required=False) = None,
                   image_url: Option(str, "The image URL for the note.", required=False) = None):
        complete_metadata = defaultdict(lambda: None, **defaults[ctx.channel.id],
                                        **get_metadata(chapter, page, panel, bubble))
        note = Note(channel_id=ctx.channel.id, text=message, chapter=complete_metadata["Chapter"],
                    page=complete_metadata["Page"], panel=complete_metadata["Panel"],
                    bubble=complete_metadata["Bubble"], image_url=image_url)
        await note.save()
        return await ctx.respond(f"Note {note.id} created.", embeds=[note_representation(note)])

    @slash_command(name="resolve", description="Resolve/unresolve a note.")
    async def resolve(self, ctx: ApplicationContext,
                      note_id: Option(int, "The ID of the note to resolve.", required=True)):
        note = await Note.get(id=note_id)
        if note is None:
            return await ctx.respond(f"Note {note_id} not found.")
        note.resolved = not note.resolved
        await note.save()
        return await ctx.respond(f"Note {note_id} {'resolved' if note.resolved else 'unresolved'}.")

    @slash_command(name="view", description="View a note.")
    async def view(self, ctx: ApplicationContext,
                   note_id: Option(int, "The ID of the note to resolve.", required=True)):
        note = await Note.get(id=note_id)
        if note is None:
            return await ctx.respond(f"Note {note_id} not found.")
        return await ctx.respond(embeds=[note_representation(note)])

    @slash_command(name="list", description="List all notes for the specified scope.")
    async def list(self, ctx: ApplicationContext,
                   scope: Option(str, "The scope for listing the notes.", required=False,
                                 choices=["channel", "category", "server"]) = "channel",
                   chapter: Option(str, "The chapter that listed notes should have.", required=False) = None,
                   page: Option(str, "The page that listed notes should have.", required=False) = None,
                   panel: Option(str, "The panel that listed notes should have.", required=False) = None,
                   bubble: Option(str, "The bubble that listed notes should have.", required=False) = None,
                   resolved: Option(str, "Whether to list (un)resolved notes only or both.", required=False,
                                    choices=["resolved", "unresolved", "both"]) = "unresolved"):
        base = Note.all()
        if scope != "channel":
            if not ctx.guild_id:
                return await ctx.respond("This scope can only be used in a server.")
            if scope == "category":
                channel = ctx.channel
                if ctx.channel.category is None:
                    valid_channels = list(filter(lambda channel: channel.category is None, ctx.guild.text_channels))
                else:
                    valid_channels = channel.category.text_channels
            else:
                valid_channels = ctx.guild.text_channels
            member = ctx.guild.get_member(ctx.user.id)
            viewable = [channel for channel in valid_channels if channel.permissions_for(member).read_messages]
            base = base.filter(channel_id__in=[channel.id for channel in viewable])
        else:
            base = base.filter(channel_id=ctx.channel.id)
        if chapter is not None:
            base = base.filter(chapter=chapter)
        if page is not None:
            base = base.filter(page=page)
        if panel is not None:
            base = base.filter(panel=panel)
        if bubble is not None:
            base = base.filter(bubble=bubble)
        if resolved != "both":
            base = base.filter(resolved=resolved == "resolved")
        notes = await base.order_by('-id').all()
        if len(notes) == 0:
            return await ctx.respond("No notes found.")
        lines = []
        for note in notes:
            description = note.text
            if len(description) > 25:
                description = description[:25] + "…"
            metadata = {"Chapter": note.chapter, "Page": note.page, "Panel": note.panel, "Bubble": note.bubble}
            metadata_included = [f"{k}: {v}" for k, v in metadata.items() if v is not None]
            if metadata_included:
                lines.append(f"{note.id} ({', '.join(metadata_included)}): {description}")
            else:
                lines.append(f"{note.id}: {description}")
        pages = [Embed(title="Note List", description="\n".join(lines[i:i + 25]), color=Color.green()) for i in
                 range(0, len(lines), 25)]
        paginator = Paginator(pages)
        await paginator.respond(ctx.interaction)


def setup(bot):
    bot.add_cog(NoteCog())
