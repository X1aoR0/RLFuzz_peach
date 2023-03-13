import ctypes
CMP_TYPE_INS = 1

class cmp_header(ctypes.Union):
    _fields_ = [
        ('b', ctypes.c_char * 8),
        ('bits', ctypes.c_uint64)
    ]

    def __init__(self):
        self.bits = 0

    @property
    def hits(self):
        return self.bits & 0xffffff



    @property
    def id(self):
        return (self.bits >> 24) & 0xffffff


    @property
    def shape(self):
        return (self.bits >> 48) & 0x1f


    @property
    def type(self):
        return (self.bits >> 53) & 0x03


    @property
    def attribute(self):
        return (self.bits >> 55) & 0x0f


    @property
    def overflow(self):
        return (self.bits >> 59) & 0x01

    @property
    def reserved(self):
        return (self.bits >> 60) & 0x0f


class cmp_operands(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('v0', ctypes.c_uint64),
        ('v1', ctypes.c_uint64),
        ('v0_128', ctypes.c_uint64),
        ('v1_128', ctypes.c_uint64)
    ]

class cmp_map(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('headers', cmp_header * 65536),
        ('log', cmp_operands * 32*65535)
    ]


