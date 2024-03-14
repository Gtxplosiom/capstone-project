class Yehey:
    check = 0
    def __init__(self):
        pass

class Yoohoo:
    def __init__(self):
        pass
    def update(self):
        Yehey.check = 1

yoohoo = Yoohoo()
yehey = Yehey()

yoohoo.update()

print(Yehey.check)
print(yehey.check)
