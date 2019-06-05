from .models import *
from .cus_models import *
from django.db.models.query import QuerySet

# instance class


class CharBeeQueryModel():
    isInitializtion = False
    BeverageTable = QuerySet(Beverage)   # <QuerySet of Beverage>
    BeverageCapacityTable = QuerySet(BeverageCapacity)
    CategoryTable = QuerySet(Category)
    TeamMemberTable = QuerySet(TeamMember)
    ShopTable = QuerySet(Shop)
    amountOfBeverageLastQuery = 0
    amountOfBeverageDetailLastQuery = 0

    def __init__(self, *args, **kwargs):
        self.BeverageTable = Beverage.objects.all()
        self.BeverageCapacityTable = BeverageCapacity.objects.all()
        self.TeamMemberTable = TeamMember.objects.all()
        self.ShopTable = Shop.objects.all()
        self.CategoryTable = Category.objects.all()
        return super().__init__(*args, **kwargs)

    def TeamMemberQuery(self, _id=None, name=None):
        QueryResult = self.TeamMemberTable
        if _id is not None:
            QueryResult = QueryResult.filter(StudentId__in=_id)
        if name is not None:
            QueryResult = QueryResult.filter(name__contains=name)
        print(QueryResult[0].photoPath)
        return QueryResult

    def ShopQuery(self, name=None):
        QueryResult = self.ShopTable
        if name is not None:
            QueryResult = QueryResult.filter(name__contains=name)
        return QueryResult

    def getLastBeverageQueryAmount(self, detail=False):
        return self.amountOfBeverageDetailLastQuery if \
            detail is True else self.amountOfBeverageLastQuery

    def BeverageQuery(self, startIndex=0, amount=1, **queryParameter):
        # Return type: List<BeverageInfo>
        # queryParameter have: _id, name, shop, cateogry, price,
        # capacity, hasCold(provid Cold-Taste), hasHot(provid Hot-Taste) and getDetail
        # If All QueryParameters are none, this function will return all Beverage Information.
        # If All QueryParameters are none, BUT getDetail is True, this function will return all Beverage Information inculde Capacity Information.
        # startIndex is the variable that controls the datas will be seleted from.
        # amount is the variable that controls the amount of BeverageInfo must seleted start at strarIndex.

        QueryResult = []
        QuerySetOfBeverage = self.BeverageTable
        # Block: Query by BeverageId
        # find the Beverage that id is equal to the id user keyin.
        if queryParameter.get('_id', None) is not None:
            ids = []
            _id = queryParameter['_id']
            if type(_id) is not list:
                ids.append(_id)
            else:
                ids = _id
            QuerySetOfBeverage = QuerySetOfBeverage.filter(
                BeverageId__in=ids)

        # Block: Query by BeverageName,
        # find the Beverage that name has same content with the name user keyin.
        if queryParameter.get('name', None) is not None:
            name = queryParameter['name']
            QuerySetOfBeverage = QuerySetOfBeverage.filter(
                name__contains=name)

        # Block: Query by Shop-Name that the Beverage behind
        # find the Beverage that is dependant to the Shop user chooies.
        if queryParameter.get('shop', None) is not None:
            shops = []
            shop = queryParameter['shop']
            if type(shop) is not list:
                shops.append(shop)
            else:
                shops = shop
            QuerySetOfBeverage = QuerySetOfBeverage.filter(
                Shop__name__in=shops)

        # Block: Query by the Beverage-Category
        # find the Beverage that is categoryed to the Cateogry user chooies.
        if queryParameter.get('category', None) is not None:
            categorys = []
            category = queryParameter['category']
            if type(category) is not list:
                categorys.append(category)
            else:
                categorys = category
            QuerySetOfBeverage = QuerySetOfBeverage.filter(
                Category__name__in=categorys)

        # Block: Query by the Beverage-Taste
        # find the Beverage that provid status is equal to the option user chooies.
        if queryParameter.get('hasHot', None) is not None:
            hasHot = queryParameter['hasHot']
            QuerySetOfBeverage = QuerySetOfBeverage.filter(
                hasHot=hasHot)

        if queryParameter.get('hasCold', None) is not None:
            hasCold = queryParameter['hasCold']
            QuerySetOfBeverage = QuerySetOfBeverage.filter(
                hasCold=hasCold)

        QueryResult = QuerySetOfBeverage
        getDetail = queryParameter.get('getDetail', None)

        if getDetail is True or \
           queryParameter.get('price', None) is not None or \
           queryParameter.get('capacity', None) is not None:

            if queryParameter.get('price', None) is not None:
                price = queryParameter['price']
                QueryResult = QueryResult.filter(capacitys__price__range=price)
            if queryParameter.get('capacity', None) is not None:
                capacity = queryParameter['capacity']
                QueryResult = QueryResult.filter(
                    capacitys__capacity=capacity)

        # print('\n----------------------------------------------------------')
        # #print(QueryResult)
        amountOfResult = len(QueryResult)
        self.amountOfBeverageDetailLastQuery = amountOfResult
        # print('\n----------------------------------------------------------')

        QueryResult = QueryResult.distinct('BeverageId')
        self.amountOfBeverageLastQuery = len(QueryResult)
        startIndex = 0 if startIndex < 0 or startIndex >= self.amountOfBeverageLastQuery \
            else startIndex
        QueryResult = QueryResult[startIndex: startIndex + amount]
        #print('-----------After Query-----------')
        # print(QueryResult)
        # print('---------------------------------')
        # #print('\n--------------------------------------------')
        return CharBeeQueryModel.packIntoBeverageInfo(QueryResult)

    @staticmethod
    def Convert(b_data: Beverage):
        # Convert Beverage object into BeverageInfo object
        # #print(b_data)
        ReturnedBeverage = BeverageInfo()
        __beverage = b_data

        def getCapacitys(__beverage: Beverage):
            listOfCapacity = []
            for c in __beverage.capacitys.all():
                __capacity = Capacity()
                __capacity.capacity = c.capacity
                __capacity.calories = c.calories
                __capacity.price = c.price
                listOfCapacity.append(__capacity)
            return listOfCapacity
        ReturnedBeverage.BeverageId = __beverage.BeverageId
        ReturnedBeverage.name = __beverage.name
        ReturnedBeverage.shop = __beverage.Shop.name
        ReturnedBeverage.category = __beverage.Category.name
        ReturnedBeverage.info = __beverage.info
        ReturnedBeverage.imagePath = __beverage.imagePath
        ReturnedBeverage.hasCold = __beverage.hasCold
        ReturnedBeverage.hasHot = __beverage.hasHot
        ReturnedBeverage.remark = __beverage.remark
        ReturnedBeverage.capacitys = getCapacitys(b_data)
        return ReturnedBeverage

    @staticmethod
    def packIntoBeverageInfo(qs: QuerySet):
        # Pack the QuerySet<Beverage> into the list<BeverageInfo>

        BeverageInfos = list()
        amountOfBeverage = len(qs)
        if amountOfBeverage > 0:
            # Setting a list that size is amountOfBeveage inputted and
            # it's store-type is limit in BeverageInfo object
            BeverageInfos = [BeverageInfo] * amountOfBeverage
            for i in range(amountOfBeverage):
                BeverageInfos[i] = CharBeeQueryModel.Convert(qs[i])
        #print('---------------After Packed-------------')
        # print(BeverageInfos)
        # print('----------------------------------------')
        return BeverageInfos
