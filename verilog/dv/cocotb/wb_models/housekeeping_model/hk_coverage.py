import cocotb
from cocotb_coverage.coverage import CoverPoint, CoverCross
from collections import namedtuple


class SPI_Coverage():
    def __init__(self) -> None:
        self.command_mapping = {
            "00000000": "no operation",
            "10000000": "write stream",
            "01000000": "read stream",
            "11000000": "write read stream",
            "11000100": "Pass-through management",
            "11000110": "Pass-through user",
        }
        self.command_mapping.update({f"10{format(n, '03b')}000": f"write {n}-bytes" for n in range(1,8)})
        self.command_mapping.update({f"01{format(n, '03b')}000": f"read {n}-bytes" for n in range(1,8)})
        self.command_mapping.update({f"11{format(n, '03b')}000": f"write read {n}-bytes" for n in range(1,8)})
        # initialize coverage no covearge happened just sample nothing so the coverge is initialized
        temp = namedtuple('temp', ['command', 'address', 'data_in', 'data_out'])
        self.spi_cov(temp('abc', "0xFFFFF", ["0xFFFFF"], ["0xFFFFF"]))

    def command_to_text(self, command):
        cocotb.log.debug(f"[{__class__.__name__}][command_to_text] command = {command}")
        if command in self.command_mapping:
            return self.command_mapping[command]
        else:
            return "invalid command"

    def spi_cov(self, spi_operation):
        @CoverPoint(
            "top.caravel.housekeeping.spi.modes",
            xf=lambda spi_operation: spi_operation.command,
            bins=[x for x in self.command_mapping.values()],
            weight=1
        )
        @CoverPoint(
            "top.caravel.housekeeping.spi.address",
            xf=lambda spi_operation: int(spi_operation.address, 16),
            bins=[(0, 0x10), (0x11, 0x20), (0x21, 0x30), (0x31, 0x40), (0x41, 0x50), (0x51, 0x60), (0x61, 0x6D)],
            bins_labels=["0 to 16", "17 to 32", "33 to 48", "49 to 64", "65 to 80", "81 to 96", "97 to 109"],
            rel=lambda val, b: b[0] <= val <= b[1],
            weight=1
        )
        def sample_command(spi_operation):
            pass

        @CoverPoint(
            "top.caravel.housekeeping.spi.data_write",
            xf=lambda data: int(data, 16),
            bins=[(0, 0), (1, 0xF), (0x10, 0xFF), (0xFF, 0xFF)],
            bins_labels=["zero", "1 to 15", "16 to 255", "255"],
            rel=lambda val, b: b[0] <= val <= b[1],
        )
        def sample_write(data):
            pass

        @CoverPoint(
            "top.caravel.housekeeping.spi.data_read",
            xf=lambda data: int(data, 16),
            bins=[(0, 0), (1, 0xF), (0x10, 0xFF), (0xFF, 0xFF)],
            bins_labels=["zero", "1 to 15", "16 to 255", "255"],
            rel=lambda val, b: b[0] <= val <= b[1],
        )
        def sample_read(data):
            pass

        sample_command(spi_operation)
        for data in spi_operation.data_in:
            sample_write(data)
        for data in spi_operation.data_out:
            sample_read(data)

        @CoverCross(
            "top.caravel.housekeeping.spi.modes_and_address",
            items=[
                "top.caravel.housekeeping.spi.modes",
                "top.caravel.housekeeping.spi.address",
            ],
        )
        def sample():
            pass
        sample()


class WB_Coverage():
    def __init__(self) -> None:
        # initialize coverage no covearge happened just sample nothing so the coverge is initialized
        temp = namedtuple('temp', ['write', 'address', 'write_data', 'read_data'])

        self.wb_cov(temp(write=0x1000, address=0x0, write_data=0xFFFFFFFFFF, read_data=0xFFFFFFFFFF))

    def wb_cov(self, wb_operation):
        @CoverPoint(
            "top.caravel.housekeeping.wb.access_type",
            xf=lambda wb_operation: wb_operation.write,
            bins=[0, 1],
            bins_labels=["read", "write"],
            weight=1
        )
        @CoverPoint(
            "top.caravel.housekeeping.wb.address",
            xf=lambda wb_operation: wb_operation.address,
            bins=[(0x26100000, 0x26100028), (0x26000000, 0x260000b8), (0x26200000, 0x26200010)],
            bins_labels=["spi address", "gpio address", "system address"],
            rel=lambda val, b: b[0] <= val <= b[1],
            weight=1
        )
        @CoverPoint(
            "top.caravel.housekeeping.wb.write_data",
            xf=lambda wb_operation: wb_operation.write_data,
            bins=[(0x00000000, 0x1FFFFFFF), (0x20000000, 0x3FFFFFFF), (0x40000000, 0x5FFFFFFF), (0x60000000, 0x7FFFFFFF), (0x80000000, 0x9FFFFFFF), (0xA0000000, 0xBFFFFFFF), (0xC0000000, 0xDFFFFFFF), (0xE0000000, 0xFFFFFFFF)],
            bins_labels=["0 to 0x1FFFFFFF", "0x20000000 to 0x3FFFFFFF", "0x40000000 to 0x5FFFFFFF", "0x60000000 to 0x7FFFFFFF", "0x80000000 to 0x9FFFFFFF", "0xA0000000 to 0xBFFFFFFF", "0xC0000000 to 0xDFFFFFFF", "0xE0000000 to 0xFFFFFFFF"],
            rel=lambda val, b: b[0] <= val <= b[1],
        )
        @CoverPoint(
            "top.caravel.housekeeping.wb.read_data",
            xf=lambda wb_operation: wb_operation.read_data,
            bins=[(0x00000000, 0x1FFFFFFF), (0x20000000, 0x3FFFFFFF), (0x40000000, 0x5FFFFFFF), (0x60000000, 0x7FFFFFFF), (0x80000000, 0x9FFFFFFF), (0xA0000000, 0xBFFFFFFF), (0xC0000000, 0xDFFFFFFF), (0xE0000000, 0xFFFFFFFF)],
            bins_labels=["0 to 0x1FFFFFFF", "0x20000000 to 0x3FFFFFFF", "0x40000000 to 0x5FFFFFFF", "0x60000000 to 0x7FFFFFFF", "0x80000000 to 0x9FFFFFFF", "0xA0000000 to 0xBFFFFFFF", "0xC0000000 to 0xDFFFFFFF", "0xE0000000 to 0xFFFFFFFF"],
            rel=lambda val, b: b[0] <= val <= b[1],
        )
        def sample(wb_operation):
            pass
        sample(wb_operation)