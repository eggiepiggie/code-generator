# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   PriceHistory REST API Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.170810
# ===================================================================
from flask_restful import Resource, reqparse
from app.bo.PriceHistory import PriceHistoryBO
from app.dao.PriceHistory import priceHistoryDAO


class PriceHistoryGetAll(Resource):

    def get(self):
        priceHistorys = priceHistoryDAO.getAllPriceHistorys()
        priceHistorysJson = []
        for priceHistory in priceHistorys:
            priceHistorysJson.append(priceHistory.toJson())
        return priceHistorysJson

    def post(self):
        args = getParameters(reqparse.RequestParser())
        priceHistory = PriceHistoryBO()
        priceHistory.setDate(args['Date'])
        priceHistory.setPrice(args['Price'])
        priceHistory.setItemId(args['ItemId'])
        priceHistory.save()
        return priceHistory.priceHistory.toJson()


class PriceHistoryById(Resource):

    def get(self, priceHistoryId):
        priceHistory = priceHistoryDAO.getPriceHistoryById(priceHistoryId)
        return priceHistory.toJson()

    def put(self, priceHistoryId):
        args = getParameters(reqparse.RequestParser())
        priceHistoryDO = priceHistoryDAO.getPriceHistoryById(priceHistoryId)
        priceHistory = PriceHistoryBO(priceHistoryDO)
        priceHistory.setDate(args['Date'])
        priceHistory.setPrice(args['Price'])
        priceHistory.setItemId(args['ItemId'])
        priceHistory.update()
        return priceHistory.priceHistory.toJson()

    def delete(self, priceHistoryId):
        return priceHistoryDAO.deleteById(priceHistoryId)


def getParameters(parser):
    '''Takes the requests body and returns it as json.'''
    parser = reqparse.RequestParser()
    parser.add_argument('Date')
    parser.add_argument('Price')
    parser.add_argument('ItemId')
    return parser.parse_args()
