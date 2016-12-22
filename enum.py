# http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
class Enum(set):
  def __getattr__(self, name):
    if name in self:
      return name
    raise AttributeError
