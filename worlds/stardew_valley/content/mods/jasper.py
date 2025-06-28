from ..game_content import ContentPack
from ..mod_registry import register_mod_content_pack
from ..override import override
from ...data import villagers_data
from ...mods.mod_data import ModNames

register_mod_content_pack(ContentPack(
    ModNames.jasper,
    villagers=(
        villagers_data.jasper,
        villagers_data.marlon,
        villagers_data.gunther,
    )
))
