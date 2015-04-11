
class test(object):
    def __init__(self, a = 0):
        self._a = a
        self._money = 0

    @property
    def b(self):
        print 'b is property defined by a'
        return self._a

    @b.setter
    def b(self, a):
       self._a = a 

    def get_money(self):
        return self._money

    def save_money(self, munny):
        self._money = munny

    money = property(get_money, save_money)

x = test()
print x.b
x.b = 5
print x.b
x.money = 7
print x.money
