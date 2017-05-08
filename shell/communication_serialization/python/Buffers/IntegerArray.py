# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Buffers

import flatbuffers

class IntegerArray(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsIntegerArray(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = IntegerArray()
        x.Init(buf, n + offset)
        return x

    # IntegerArray
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # IntegerArray
    def List(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Int32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # IntegerArray
    def ListLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def IntegerArrayStart(builder): builder.StartObject(1)
def IntegerArrayAddList(builder, list): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(list), 0)
def IntegerArrayStartListVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def IntegerArrayEnd(builder): return builder.EndObject()