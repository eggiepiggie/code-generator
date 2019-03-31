# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   StockLevel REST API Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.163719
# ===================================================================
from flask_restful import Resource, reqparse
from app.bo.StockLevel import StockLevelBO
from app.dao.StockLevel import stockLevelDAO


class StockLevelGetAll(Resource):

    def get(self):
        stockLevels = stockLevelDAO.getAllStockLevels()
        stockLevelsJson = []
        for stockLevel in stockLevels:
            stockLevelsJson.append(stockLevel.toJson())
        return stockLevelsJson

    def post(self):
        args = getParameters(reqparse.RequestParser())
        stockLevel = StockLevelBO()
        stockLevel.setItemId(args['ItemId'])
        stockLevel.setCount(args['Count'])
        stockLevel.setNextShipment(args['NextShipment'])
        stockLevel.save()
        return stockLevel.stockLevel.toJson()


class StockLevelById(Resource):

    def get(self, stockLevelId):
        stockLevel = stockLevelDAO.getStockLevelById(stockLevelId)
        return stockLevel.toJson()

    def put(self, stockLevelId):
        args = getParameters(reqparse.RequestParser())
        stockLevelDO = stockLevelDAO.getStockLevelById(stockLevelId)
        stockLevel = StockLevelBO(stockLevelDO)
        stockLevel.setItemId(args['ItemId'])
        stockLevel.setCount(args['Count'])
        stockLevel.setNextShipment(args['NextShipment'])
        stockLevel.update()
        return stockLevel.stockLevel.toJson()

    def delete(self, stockLevelId):
        return stockLevelDAO.deleteById(stockLevelId)


def getParameters(parser):
    '''Takes the requests body and returns it as json.'''
    parser = reqparse.RequestParser()
    parser.add_argument('ItemId')
    parser.add_argument('Count')
    parser.add_argument('NextShipment')
    return parser.parse_args()
