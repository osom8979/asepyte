# -*- coding: utf-8 -*-

from io import BytesIO
from typing import List

from asepyte.frame import FRAME_HEADER_SIZE, Frame, FrameChunk, FrameHeader
from asepyte.header import HEADER_SIZE, Header


class Aseprite:
    def __init__(self, header: Header, frames: List[Frame]):
        self.header = header
        self.frames = frames

    def encode(self) -> bytes:
        buffer = BytesIO()
        buffer.write(self.header.encode())
        return buffer.getvalue()

    @classmethod
    def decode(cls, data: bytes):
        buffer = BytesIO(data)
        header = Header.decode(buffer.read(HEADER_SIZE))
        frames = list()
        for frame_index in range(header.frames):
            frame_header = FrameHeader.decode(buffer.read(FRAME_HEADER_SIZE))
            total_chunk_size = frame_header.bytes_in_this_frame - FRAME_HEADER_SIZE
            remain_chunk_data = buffer.read(total_chunk_size)

            frame_chunks = list()
            for frame_chunk_index in range(frame_header.number_of_chunks):
                frame_chunk = FrameChunk.decode(remain_chunk_data)
                frame_chunk_size = frame_chunk.chunk_size
                remain_chunk_data = remain_chunk_data[frame_chunk_size:]
                frame_chunks.append(frame_chunk)

            assert 0 <= len(remain_chunk_data)
            if len(remain_chunk_data) != 0:
                raise ValueError("Not all chunk data has been consumed")
            frames.append(Frame(frame_header, frame_chunks))
        return cls(header, frames)
