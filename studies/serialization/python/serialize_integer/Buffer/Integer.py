# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Buffer

import flatbuffers

class Integer(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsInteger(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Integer()
        x.Init(buf, n + offset)
        return x

    # Integer
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Integer
    def Value(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

def IntegerStart(builder): builder.StartObject(1)
def IntegerAddValue(builder, value): builder.PrependInt32Slot(0, value, 0)
def IntegerEnd(builder): return builder.EndObject()
