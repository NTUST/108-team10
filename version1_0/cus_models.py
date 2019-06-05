class Capacity():
    capacity = ''
    price = 0
    calories = 0

    def __str__(self):
        return '%s %d' % (self.capacity, self.price)


class BeverageInfo():
    BeverageId = ''
    name = ''
    shop = ''
    category = ''
    info = ''
    imagePath = ''
    hasCold = True
    hasHot = False
    remark = ''
    #
    price = 0
    capacity = ''
    capacitys = [Capacity]
    calories = 0

    def __str__(self):
        # self.BeverageId
        return '%s - %s - ' % (str(self.shop), str(self.name)) + str(self.capacity)

    def getCapacity(self):
        return len(capacitys)
