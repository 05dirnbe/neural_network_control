import flatbuffers
# Generated by `flatc`.
import Buffer.IntegerArray

builder = flatbuffers.Builder(0)

n= 100000

# Serialize the FlatBuffer data.
Buffer.IntegerArray.IntegerArrayStartValuesVector(builder, n)
# Note: Since we prepend the items, this loop iterates in reverse order.
for i in reversed(range(n)):
	builder.PrependUint32(i)
inv = builder.EndVector(n)

Buffer.IntegerArray.IntegerArrayStart(builder)
Buffer.IntegerArray.IntegerArrayAddValues(builder, inv)
l = Buffer.IntegerArray.IntegerArrayEnd(builder)

builder.Finish(l)

# We now have a FlatBuffer that we could store on disk or send over a network.

# ...Saving to file or sending over a network code goes here...

# Instead, we are going to access this buffer right away (as if we just
# received it).

buf = builder.Output()

# Note: We use `0` for the offset here, since we got the data using the
# `builder.Output()` method. This simulates the data you would store/receive
# in your FlatBuffer. If you wanted to read from the `builder.Bytes` directly,
# you would need to pass in the offset of `builder.Head()`, as the builder
# actually constructs the buffer backwards.
l = Buffer.IntegerArray.IntegerArray.GetRootAsIntegerArray(buf, 0)
# Get and test the `values` FlatBuffer `vector`.
for i in xrange(l.ValuesLength()):
	# print l.Values(i)
	assert l.Values(i) == i

print 'The FlatBuffer was successfully created and verified!'