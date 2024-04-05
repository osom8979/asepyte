# -*- coding: utf-8 -*-

from dataclasses import dataclass
from io import BytesIO
from struct import pack, unpack
from typing import List, Tuple


class OldPalette4:

    @dataclass
    class Packet:
        number_of_palette_entries: int
        """
        Number of palette entries to skip from the last packet (start from 0)
        """

        colors: List[Tuple[int, int, int]]
        """
        Red (0-255)
        Green (0-255)
        Blue (0-255)
        """

    def __init__(self, packets: List[Packet]):
        self.packets = packets

    def encode(self) -> bytes:
        buffer = BytesIO()
        buffer.write(pack(b"<H", len(self.packets)))
        for packet in self.packets:
            number_of_palette_entries = packet.number_of_palette_entries
            real_colors_size = len(packet.colors)
            # Number of colors in the packet (0 means 256)
            number_of_colors = 0 if real_colors_size == 256 else real_colors_size
            buffer.write(pack(b"<BB", number_of_palette_entries, number_of_colors))
            for color in packet.colors:
                buffer.write(pack(b"<BBB", *color))
        return buffer.getvalue()

    @classmethod
    def decode(cls, data: bytes):
        buffer = BytesIO(data)
        number_of_packets = unpack(b"<H", buffer.read(2))[0]
        assert isinstance(number_of_packets, int)

        packets = list()
        for pi in range(number_of_packets):
            number_of_palette_entries, number_of_colors = unpack(b"<BB", buffer.read(2))
            assert isinstance(number_of_palette_entries, int)
            assert isinstance(number_of_colors, int)

            # Number of colors in the packet (0 means 256)
            real_colors_size = 256 if number_of_colors == 0 else number_of_colors

            colors = list()
            for ci in range(real_colors_size):
                r, g, b = unpack(b"<BBB", buffer.read(3))
                colors.append((r, g, b))

            packets.append(cls.Packet(number_of_palette_entries, colors))

        return cls(packets)
