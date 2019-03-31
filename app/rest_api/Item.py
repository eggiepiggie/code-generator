# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   Item REST API Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.132099
# ===================================================================
from flask_restful import Resource, reqparse
from app.bo.Item import ItemBO
from app.dao.Item import itemDAO


class ItemGetAll(Resource):

    def get(self):
        items = itemDAO.getAllItems()
        itemsJson = []
        for item in items:
            itemsJson.append(item.toJson())
        return itemsJson

    def post(self):
        args = getParameters(reqparse.RequestParser())
        item = ItemBO()
        item.setName(args['Name'])
        item.setDescription(args['Description'])
        item.setColour(args['Colour'])
        item.setWeight(args['Weight'])
        item.setIsStocked(args['IsStocked'])
        item.setDepartmentId(args['DepartmentId'])
        item.save()
        return item.item.toJson()


class ItemById(Resource):

    def get(self, itemId):
        item = itemDAO.getItemById(itemId)
        return item.toJson()

    def put(self, itemId):
        args = getParameters(reqparse.RequestParser())
        itemDO = itemDAO.getItemById(itemId)
        item = ItemBO(itemDO)
        item.setName(args['Name'])
        item.setDescription(args['Description'])
        item.setColour(args['Colour'])
        item.setWeight(args['Weight'])
        item.setIsStocked(args['IsStocked'])
        item.setDepartmentId(args['DepartmentId'])
        item.update()
        return item.item.toJson()

    def delete(self, itemId):
        return itemDAO.deleteById(itemId)


class ItemPriceHistorys(Resource):
    def get(self, itemId):
        itemDO = itemDAO.getItemById(itemId)
        item = ItemBO(itemDO)
        priceHistorys = item.getPriceHistorys()
        results = []
        for priceHistory in priceHistorys:
            results.append(priceHistory.toJson())
        return results


class ItemStockLevels(Resource):
    def get(self, itemId):
        itemDO = itemDAO.getItemById(itemId)
        item = ItemBO(itemDO)
        stockLevels = item.getStockLevels()
        results = []
        for stockLevel in stockLevels:
            results.append(stockLevel.toJson())
        return results


class ItemPurchaseItemLists(Resource):
    def get(self, itemId):
        itemDO = itemDAO.getItemById(itemId)
        item = ItemBO(itemDO)
        purchaseItemLists = item.getPurchaseItemLists()
        results = []
        for purchaseItemList in purchaseItemLists:
            results.append(purchaseItemList.toJson())
        return results


def getParameters(parser):
    '''Takes the requests body and returns it as json.'''
    parser = reqparse.RequestParser()
    parser.add_argument('Name')
    parser.add_argument('Description')
    parser.add_argument('Colour')
    parser.add_argument('Weight')
    parser.add_argument('IsStocked')
    parser.add_argument('DepartmentId')
    return parser.parse_args()
