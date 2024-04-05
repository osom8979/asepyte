# -*- coding: utf-8 -*-

from io import BytesIO
from struct import calcsize, pack, unpack
from typing import Final, List

MAGIC_NUMBER: Final[int] = 0xF1FA
MIGHT_HAVE_MORE_CHUNKS: Final[int] = 0xFFFF

# noinspection SpellCheckingInspection
FRAME_HEADER_FORMAT: Final[bytes] = b"<IHHH2pI"
FRAME_HEADER_SIZE: Final[int] = calcsize(FRAME_HEADER_FORMAT)
assert FRAME_HEADER_SIZE == 16

FRAME_CHUNK_PREFIX_FORMAT: Final[bytes] = b"<IH"
FRAME_CHUNK_PREFIX_SIZE: Final[int] = calcsize(FRAME_CHUNK_PREFIX_FORMAT)
assert FRAME_CHUNK_PREFIX_SIZE == 6


class FrameHeader:
    bytes_in_this_frame: int

    magic_number: int
    """
    Magic number (always 0xF1FA)
    """

    old_number_of_chunks: int
    """
    Old field which specifies the number of "chunks"
    in this frame. If this value is 0xFFFF, we might
    have more chunks to read in this frame
    (so we have to use the new field)
    """

    frame_duration: int
    """
    Frame duration (in milliseconds)
    """

    padding: bytes
    """
    For future (set to zero)
    """

    new_number_of_chunks: int
    """
    New field which specifies the number of "chunks"
    in this frame (if this is 0, use the old field)
    """

    def __init__(
        self,
        bytes_in_this_frame: int,
        magic_number: int,
        old_number_of_chunks: int,
        frame_duration: int,
        padding: bytes,
        new_number_of_chunks: int,
    ):
        if magic_number != MAGIC_NUMBER:
            raise ValueError(f"Invalid magic number: 0x{magic_number:02X}")

        self.bytes_in_this_frame = bytes_in_this_frame
        self.magic_number = magic_number
        self.old_number_of_chunks = old_number_of_chunks
        self.frame_duration = frame_duration
        self.padding = padding
        self.new_number_of_chunks = new_number_of_chunks

    @property
    def might_have_more_chunks(self) -> bool:
        return self.old_number_of_chunks == MIGHT_HAVE_MORE_CHUNKS

    @property
    def number_of_chunks(self):
        if self.new_number_of_chunks == 0:
            return self.old_number_of_chunks
        else:
            return self.new_number_of_chunks

    def encode(self) -> bytes:
        data = pack(
            FRAME_HEADER_FORMAT,
            self.bytes_in_this_frame,
            self.magic_number,
            self.old_number_of_chunks,
            self.frame_duration,
            self.padding,
            self.new_number_of_chunks,
        )
        assert len(data) == FRAME_HEADER_SIZE
        return data

    @classmethod
    def decode(cls, data: bytes):
        return cls(*unpack(FRAME_HEADER_FORMAT, data))


class FrameChunk:
    chunk_size: int
    chunk_type: int
    chunk_data: bytes

    def __init__(
        self,
        chunk_size: int,
        chunk_type: int,
        chunk_data: bytes,
    ):
        self.chunk_size = chunk_size
        self.chunk_type = chunk_type
        self.chunk_data = chunk_data

    def encode(self) -> bytes:
        data = pack(FRAME_CHUNK_PREFIX_FORMAT, self.chunk_size, self.chunk_type)
        assert len(data) == FRAME_CHUNK_PREFIX_SIZE
        buffer = BytesIO()
        buffer.write(data)
        buffer.write(self.chunk_data)
        return buffer.getvalue()

    @classmethod
    def decode(cls, data: bytes):
        if len(data) < FRAME_CHUNK_PREFIX_SIZE:
            raise ValueError(f"Invalid frame chunk bytes: {len(data)}")
        fields = unpack(FRAME_CHUNK_PREFIX_FORMAT, data[:FRAME_CHUNK_PREFIX_SIZE])
        chunk_size, chunk_type = fields
        chunk_data = data[FRAME_CHUNK_PREFIX_SIZE:chunk_size]
        if len(chunk_data) + FRAME_CHUNK_PREFIX_SIZE != chunk_size:
            raise ValueError("Invalid frame chunk size")
        return cls(chunk_size, chunk_type, chunk_data)


class Frame:
    def __init__(self, header: FrameHeader, chunk: List[FrameChunk]):
        self.header = header
        self.chunk = chunk
