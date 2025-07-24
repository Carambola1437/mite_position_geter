import pymem
import struct
import time

class MinecraftCoordinateReader:
    def __init__(self):
        self.pm = None
        self.openal_base = 0
        self.aBaseBuffer = 0
        self._initialize()

    def _initialize(self):
        """初始化：自动查找进程和基址"""
        try:
            self.pm = pymem.Pymem("javaw.exe")
        except pymem.exception.ProcessNotFound:
            try:
                self.pm = pymem.Pymem("java.exe")
            except Exception as e:
                raise Exception(f"找不到Minecraft进程: {e}")

        # 获取OpenAL64.dll基址
        for module in self.pm.list_modules():
            if module.name.lower() == "openal64.dll":
                self.openal_base = module.lpBaseOfDll
                break

        if not self.openal_base:
            raise Exception("游戏可能未加载OpenAL64.dll")

    def _read_memory_int(self, address):
        """读取4字节整数（小端序）"""
        buffer = self.pm.read_bytes(address, 4)
        return struct.unpack("<i", buffer)[0]

    def _read_memory_float(self, address):
        """读取4字节浮点数（小端序）"""
        buffer = self.pm.read_bytes(address, 4)
        return struct.unpack("<f", buffer)[0]

    def get_pos(self):
        """
        获取当前坐标 (x, y, z)
        返回: tuple (x, y, z)
        """
        try:
            # 计算中间地址并读取aBaseBuffer
            aBaseAddress = self.openal_base + 377608
            self.aBaseBuffer = self._read_memory_int(aBaseAddress)
            
            # 读取坐标
            x = self._read_memory_float(self.aBaseBuffer + 192)
            y = self._read_memory_float(self.aBaseBuffer + 196) - 1.0  # Y坐标-1修正
            z = self._read_memory_float(self.aBaseBuffer + 200)
            
            return (x, y, z)
        except Exception as e:
            raise Exception(f"坐标读取失败: {e}")


