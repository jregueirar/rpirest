class Task(object):
    def __init__(self, **kwargs):
        for field in ('id', 'name', 'owner', 'status'):
            setattr(self, field, kwargs.get(field, None))


class XY(object):

    def __init__(self, **kwargs):
        for field in ('x', 'y'):
            setattr(self, field, kwargs.get(field, None))

# FIXME: Utilizar herencia de clases de XY
class Pixel(object):
    matrix_len = 8

    def __init__(self, **kwargs):
        for field in ('x', 'y', 'r', 'g', 'b'):
            setattr(self, field, kwargs.get(field, None))

    def get_id(self):
        return self.y * self.matrix_len + self.x

    @classmethod
    def get_coordinates(cls, pos_in_list):
        x = pos_in_list % cls.matrix_len
        y = pos_in_list / cls.matrix_len
        return {'x': int(x), 'y': int(y)}
