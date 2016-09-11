#
# Autogenerated by Thrift Compiler (0.9.2)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException

from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None



class HyySearchRequest:
  """
  Attributes:
   - qid
   - data
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'qid', None, None, ), # 1
    (2, TType.STRING, 'data', None, None, ), # 2
  )

  def __init__(self, qid=None, data=None,):
    self.qid = qid
    self.data = data

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.qid = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.data = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('HyySearchRequest')
    if self.qid is not None:
      oprot.writeFieldBegin('qid', TType.STRING, 1)
      oprot.writeString(self.qid)
      oprot.writeFieldEnd()
    if self.data is not None:
      oprot.writeFieldBegin('data', TType.STRING, 2)
      oprot.writeString(self.data)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.qid)
    value = (value * 31) ^ hash(self.data)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class HyyDoc:
  """
  Attributes:
   - doc_id
   - title
   - author
   - datetime
   - source
   - text
   - source_icon
   - source_desc
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'doc_id', None, None, ), # 1
    (2, TType.STRING, 'title', None, None, ), # 2
    (3, TType.STRING, 'author', None, None, ), # 3
    (4, TType.STRING, 'datetime', None, None, ), # 4
    (5, TType.STRING, 'source', None, None, ), # 5
    (6, TType.STRING, 'text', None, None, ), # 6
    (7, TType.STRING, 'source_icon', None, None, ), # 7
    (8, TType.STRING, 'source_desc', None, None, ), # 8
  )

  def __init__(self, doc_id=None, title=None, author=None, datetime=None, source=None, text=None, source_icon=None, source_desc=None,):
    self.doc_id = doc_id
    self.title = title
    self.author = author
    self.datetime = datetime
    self.source = source
    self.text = text
    self.source_icon = source_icon
    self.source_desc = source_desc

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.doc_id = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.title = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRING:
          self.author = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.STRING:
          self.datetime = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.STRING:
          self.source = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 6:
        if ftype == TType.STRING:
          self.text = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 7:
        if ftype == TType.STRING:
          self.source_icon = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 8:
        if ftype == TType.STRING:
          self.source_desc = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('HyyDoc')
    if self.doc_id is not None:
      oprot.writeFieldBegin('doc_id', TType.STRING, 1)
      oprot.writeString(self.doc_id)
      oprot.writeFieldEnd()
    if self.title is not None:
      oprot.writeFieldBegin('title', TType.STRING, 2)
      oprot.writeString(self.title)
      oprot.writeFieldEnd()
    if self.author is not None:
      oprot.writeFieldBegin('author', TType.STRING, 3)
      oprot.writeString(self.author)
      oprot.writeFieldEnd()
    if self.datetime is not None:
      oprot.writeFieldBegin('datetime', TType.STRING, 4)
      oprot.writeString(self.datetime)
      oprot.writeFieldEnd()
    if self.source is not None:
      oprot.writeFieldBegin('source', TType.STRING, 5)
      oprot.writeString(self.source)
      oprot.writeFieldEnd()
    if self.text is not None:
      oprot.writeFieldBegin('text', TType.STRING, 6)
      oprot.writeString(self.text)
      oprot.writeFieldEnd()
    if self.source_icon is not None:
      oprot.writeFieldBegin('source_icon', TType.STRING, 7)
      oprot.writeString(self.source_icon)
      oprot.writeFieldEnd()
    if self.source_desc is not None:
      oprot.writeFieldBegin('source_desc', TType.STRING, 8)
      oprot.writeString(self.source_desc)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.doc_id)
    value = (value * 31) ^ hash(self.title)
    value = (value * 31) ^ hash(self.author)
    value = (value * 31) ^ hash(self.datetime)
    value = (value * 31) ^ hash(self.source)
    value = (value * 31) ^ hash(self.text)
    value = (value * 31) ^ hash(self.source_icon)
    value = (value * 31) ^ hash(self.source_desc)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class HyySearchResponse:
  """
  Attributes:
   - qid
   - doc_list
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'qid', None, None, ), # 1
    (2, TType.LIST, 'doc_list', (TType.STRUCT,(HyyDoc, HyyDoc.thrift_spec)), None, ), # 2
  )

  def __init__(self, qid=None, doc_list=None,):
    self.qid = qid
    self.doc_list = doc_list

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.qid = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.LIST:
          self.doc_list = []
          (_etype3, _size0) = iprot.readListBegin()
          for _i4 in xrange(_size0):
            _elem5 = HyyDoc()
            _elem5.read(iprot)
            self.doc_list.append(_elem5)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('HyySearchResponse')
    if self.qid is not None:
      oprot.writeFieldBegin('qid', TType.STRING, 1)
      oprot.writeString(self.qid)
      oprot.writeFieldEnd()
    if self.doc_list is not None:
      oprot.writeFieldBegin('doc_list', TType.LIST, 2)
      oprot.writeListBegin(TType.STRUCT, len(self.doc_list))
      for iter6 in self.doc_list:
        iter6.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.qid)
    value = (value * 31) ^ hash(self.doc_list)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)