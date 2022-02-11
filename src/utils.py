from typing import Dict, Optional

from discord import Color, Embed

from .orm import Note


def get_metadata(chapter: Optional[str] = None, page: Optional[str] = None, panel: Optional[str] = None,
                 bubble: Optional[str] = None) -> Dict[str, str]:
    metadata = {}
    if chapter:
        metadata["Chapter"] = chapter
    if page:
        metadata["Page"] = page
    if panel:
        metadata["Panel"] = panel
    if bubble:
        metadata["Bubble"] = bubble
    return metadata


def metadata_representation(metadata: Dict[str, str]):
    if not metadata:
        return "No Metadata"
    else:
        return "; ".join(f"{k}: {v}" for k, v in sorted(metadata.items(), key=lambda item: item[0]))


def note_representation(note: Note) -> Embed:
    embed = Embed(title=f"Note #{note.id}", description=note.text,
                  color=Color.green() if not note.resolved else Color.red())
    embed.add_field(name="Status", value='Unresolved' if not note.resolved else 'Resolved')
    if note.chapter:
        embed.add_field(name="Chapter", value=note.chapter)
    if note.page:
        embed.add_field(name="Page", value=note.page)
    if note.panel:
        embed.add_field(name="Panel", value=note.panel)
    if note.bubble:
        embed.add_field(name="Bubble", value=note.bubble)
    return embed
