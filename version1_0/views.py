from django.shortcuts import render
from django.template import loader
from django.http import *
from .queryMethod import *
from CharBee.settings import *
from django.db import connection
import logging

import datetime as d
import json


class CharBeeURLRegister():

    isFlag = bool(True)
    QueryModel = CharBeeQueryModel()
    @staticmethod
    def init():
        if CharBeeURLRegister.isFlag is True:
            return
        CharBeeURLRegister.QueryModel = CharBeeQueryModel()
        CharBeeURLRegister.isFlag = True

    @staticmethod
    def GetParameterFromPOST(userRequest, key):
        value = userRequest.POST.get(key, None)
        return None if value == '' else value

    @staticmethod
    def GetPAarameterFromCookies(userRequest, key):
        value = CharBeeURLRegister.Cookies_get(userRequest, key)
        return None if value == '' else value

    @staticmethod
    def Cookies_set(serverResponse, key, value):
        # Python Type to Json
        value = json.dumps(value)
        serverResponse.set_cookie(key, value)

    @staticmethod
    def Cookies_get(userRequest, key):
        # Json to Python Type
        value = json.loads(json.dumps(
            None) if key not in userRequest.COOKIES else userRequest.COOKIES[key])
        return value

    @staticmethod
    def GetQueryParameter(userRequest, serverResponse, focusPage):
        # userRequest is a Django..HttpRequest, serverResponse is a Django..HttpResponse
        # _id, name, shop, category, capacity, price, t, hasCold, hasHot
        try:
            keysNames = ['_id', 'name', 'shop',
                         'category', 'capacity', 'price',
                         'orderby', 'orderd', 'taste', ]
            parametersDict = dict()

            if CharBeeURLRegister.Cookies_get(userRequest, 'init') != True:
                CharBeeURLRegister.Cookies_set(serverResponse, 'init', True)
                CharBeeURLRegister.Cookies_set(serverResponse, 'focusPage', 1)
                for key in keysNames:
                    CharBeeURLRegister.Cookies_set(serverResponse, key, None)

            ParameterGetter = None
            if userRequest.method == 'POST':
                ParameterGetter = CharBeeURLRegister.GetParameterFromPOST
            else:
                ParameterGetter = CharBeeURLRegister.GetPAarameterFromCookies

            for key in keysNames:
                parameterValue = ParameterGetter(userRequest, key)
                parametersDict[key] = CharBeeURLRegister.QueryParameterExplained(
                    key, parameterValue)
                CharBeeURLRegister.Cookies_set(
                    serverResponse, key, parameterValue)
            # -------------------------------------------------SetPageValue
            if focusPage is None:
                focusPage = CharBeeURLRegister.Cookies_get(
                    userRequest, 'focusPage')
            else:
                CharBeeURLRegister.Cookies_set(
                    serverResponse, 'focusPage', focusPage)
            # ---------------------------------------------------
                # unpacked value of dict[taste] and pack it into dict
            parametersDict['hasCold'], parametersDict['hasHot'] = parametersDict['taste']
            parametersDict['focusPage'] = focusPage
            # throw taste, we don't need it.
            parametersDict.pop('taste')
            # parametersDict will like
            # {
            # '_id':str, the beverageId user input,
            # 'name':str, the beverageName user input,
            # 'capacity':str, the capacity of beverage user selected,
            # 'shop':str the beverageShop user selected,
            # 'category':str, the category of beverage user selected,
            # 'price':tuple, the price-range user selected,
            # 'hasCold':bool, the beverage's taste-option user selected,
            # 'hasHot':bool, the beverage's taste-option user selected
            # }
            return parametersDict
        except TypeError as typeError:
            raise typeError
        except KeyError as typeError:
            raise typeError

    @staticmethod
    def QueryParameterExplained(key, value):
        # Python Type
        decodedValue = value

        if key is 'price':
            # input data is a number mean the low-bound of price-range
            if value == None or value == '':
                # all
                decodedValue = (0, 200)
            elif value == '0':
                # under $30
                decodedValue = (0, 30)
            elif value == '100':
                # above $100
                decodedValue = (100, 200)
            else:
                # a range
                decodedValue = (int(value), int(value) + 10)
        elif key is 'taste':
            hasCold, hasHot = (None, None)
            if value is not None and value != '':
                hasCold = True if value == 'HasCold' else None
                hasHot = True if value == 'HasHot' else None
                hasCold = False if value == 'OnlyHot' else True
                hasHot = False if value == 'OnlyCold' else True
            decodedValue = (hasCold, hasHot)
        return decodedValue

    @staticmethod
    def IndexHandle(userRequest):  # 首頁處理函式
        ShopInfos = CharBeeURLRegister.QueryModel.ShopQuery()
        # return HttpResponse(ShopInfos)
        return render(userRequest, 'index.html', {'Shops': ShopInfos})

    @staticmethod
    def ResultHandle(userRequest, focusPage=None):  # 查詢結果處理函式
        CharBeeURLRegister.init()
        try:
            #p = connection.connection
            #b = DATABASES['default']
            serverResponse = render(userRequest, 'Result.html')
            queryParameterDict = CharBeeURLRegister.GetQueryParameter(userRequest,
                                                                      serverResponse,
                                                                      focusPage)  # Get a Dict

            _id, name, shop, category, capacity, price, orderby, orderd, hasCold, hasHot, focusPage = \
                (queryParameterDict[key] for key in queryParameterDict)

            if focusPage is None:
                v = CharBeeURLRegister.Cookies_get(userRequest, 'focusPage')
                focusPage = 1 if v is None else v
            else:
                CharBeeURLRegister.Cookies_set(
                    serverResponse, 'focusPage', focusPage)
            startIndex = (focusPage-1)*12
            # print('%d %d' % (startIndex, endIndex))

            BeverageInfos = \
                CharBeeURLRegister.QueryModel.BeverageQuery(_id=_id, name=name, shop=shop, category=category,
                                                            capacity=capacity, price=price, hasCold=hasCold,
                                                            hasHot=hasHot, orderby=orderby, orderd=orderd,
                                                            startIndex=startIndex, amount=12)
            # print('123')
            BeverageAmount = CharBeeURLRegister.QueryModel.getLastBeverageQueryAmount()

            # Page Compute---------------------
            pageAmount = BeverageAmount // 12 + \
                (1 if BeverageAmount % 12 > 0 else 0)

            pageStart = focusPage - 4 if focusPage - 4 >= 1 else 1
            pageEnd = pageStart + 4 if pageStart + 4 <= pageAmount else pageAmount
            pageMap = [i for i in range(pageStart, pageEnd+1)]
            # ---------------------
            queryFlag = None
            if userRequest.method == 'POST':
                queryFlag = False if pageAmount is 0 \
                    else True

            message = '沒有符合的飲料！' if queryFlag is 0 \
                else '找到 %d 種符合搜尋要求的飲料！' % BeverageAmount

            ReturnData = {'message': message,
                          'queryFlag': queryFlag,
                          'Beverages': BeverageInfos,
                          'PageMap': pageMap,
                          'FocusPage': focusPage,
                          'QueryParameter': queryParameterDict}

            # return HttpResponse(BeverageInfos)
            # print([b.name for b in BeverageInfos])
            ResponseContent = loader.render_to_string(
                'Result.html', ReturnData, userRequest)
            serverResponse.content = ResponseContent
            # serverResponse['Fuck'] = 123
            # print('-------------------------------------------------------------------------------')
            print(BeverageInfos)
            return serverResponse
        except TypeError as typeError:
            data = {'Error': 'QQ'}
            h = render(userRequest, 'Result.html', context=data)
            return h

    @staticmethod
    def ShopMenuHandle(request, shop='50嵐', focusPage=None):  # 店家菜單顯示函式
        CharBeeURLRegister.init()
        serverResponse = HttpResponse()

        if focusPage is None:
            v = CharBeeURLRegister.Cookies_get(request, 'focusPage')
            focusPage = 1 if v is None else v
        else:
            CharBeeURLRegister.Cookies_set(
                serverResponse, 'focusPage', focusPage)
        startIndex = (focusPage-1) * 16

        BeverageInfos = CharBeeURLRegister.QueryModel.BeverageQuery(
            shop=shop, startIndex=startIndex, amount=16)
        BeverageAmount = CharBeeURLRegister.QueryModel.getLastBeverageQueryAmount()

        # Page Compute---------------------
        pageAmount = BeverageAmount // 16 + \
            (1 if BeverageAmount % 16 > 0 else 0)

        pageStart = focusPage - 4 if focusPage - 4 > 1 else 1
        pageEnd = pageStart + 4 if pageStart + 4 <= pageAmount else pageAmount
        print(pageStart)
        print(pageEnd)
        pageMap = [i for i in range(pageStart, pageEnd + 1)]
        print(pageMap)
        # ---------------------
        # return HttpResponse(BeverageInfos)
        ReturnData = {'Shop': shop,
                      'Menu': BeverageInfos,
                      'PageMap': pageMap,
                      'FocusPage': focusPage}
        ResponseContent = loader.render_to_string(
            'ShopMenu.html', ReturnData, request)
        serverResponse.content = ResponseContent
        # return HttpResponse(ReturnData)
        # print('-------------------------------------------------------------------------------')
        # print('Return ShopMenu')
        return serverResponse

    @staticmethod
    def AboutUsHandle(request):  # 關於我們處理函式
        CharBeeURLRegister.init()
        TMInfos = CharBeeURLRegister.QueryModel.TeamMemberQuery()
        # print('-------------------------------------------------------------------------------')
        # print('Return AboutUs')
        return render(request, 'AboutUs.html', {'TeamMembers': TMInfos})

    @staticmethod
    def BeverageInfoHandle(request, _id, capacity=None):  # 飲料詳細資訊處理涵式
        # beverageInfo is a version1_0.cus_models.BeverageInfo
        CharBeeURLRegister.init()
        beverageInfo = CharBeeURLRegister.QueryModel.BeverageQuery(
            _id=_id, capacity=capacity, getDetail=True)
        # type: BeverageInfo
        beverage = None \
            if len(beverageInfo) == 0 \
            else beverageInfo[0]
        if beverage is not None:
            capacity = beverage.capacitys[0].capacity \
                if capacity is None else capacity
            for c in beverage.capacitys:
                if c.capacity == capacity:
                    beverage.price = c.price
                    beverage.calories = c.calories
            print(beverage.capacitys[0].capacity)
            beverage.capacity = beverage.capacitys[0].capacity if capacity is None \
                else capacity
        message = 'No Matched Beverage!' \
            if beverage is None \
            else 'Success! Amount of Matched Beverage is % d' % len(beverageInfo)
        beverageId = 'A01' \
            if beverage is None \
            else beverage.BeverageId

        ReturnData = {'message': message,
                      'Beverage': beverage,
                      'Capacity': capacity,
                      'BeverageId': beverageId}
        # return HttpResponse(BeverageInfo)
        # print('-------------------------------------------------------------------------------')
        # print('Return BeverageInfo')
        print(beverage.calories)
        return render(request, 'BeverageInfo.html', ReturnData)
