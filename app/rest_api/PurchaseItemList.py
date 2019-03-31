# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   PurchaseItemList REST API Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.157139
# ===================================================================
from flask_restful import Resource, reqparse
from app.bo.PurchaseItemList import PurchaseItemListBO
from app.dao.PurchaseItemList import purchaseItemListDAO


class PurchaseItemListGetAll(Resource):

    def get(self):
        purchaseItemLists = purchaseItemListDAO.getAllPurchaseItemLists()
        purchaseItemListsJson = []
        for purchaseItemList in purchaseItemLists:
            purchaseItemListsJson.append(purchaseItemList.toJson())
        return purchaseItemListsJson

    def post(self):
        args = getParameters(reqparse.RequestParser())
        purchaseItemList = PurchaseItemListBO()
        purchaseItemList.setPurchaseId(args['PurchaseId'])
        purchaseItemList.setItemId(args['ItemId'])
        purchaseItemList.setCount(args['Count'])
        purchaseItemList.save()
        return purchaseItemList.purchaseItemList.toJson()


class PurchaseItemListById(Resource):

    def get(self, purchaseItemListId):
        purchaseItemList = purchaseItemListDAO.getPurchaseItemListById(purchaseItemListId)
        return purchaseItemList.toJson()

    def put(self, purchaseItemListId):
        args = getParameters(reqparse.RequestParser())
        purchaseItemListDO = purchaseItemListDAO.getPurchaseItemListById(purchaseItemListId)
        purchaseItemList = PurchaseItemListBO(purchaseItemListDO)
        purchaseItemList.setPurchaseId(args['PurchaseId'])
        purchaseItemList.setItemId(args['ItemId'])
        purchaseItemList.setCount(args['Count'])
        purchaseItemList.update()
        return purchaseItemList.purchaseItemList.toJson()

    def delete(self, purchaseItemListId):
        return purchaseItemListDAO.deleteById(purchaseItemListId)


def getParameters(parser):
    '''Takes the requests body and returns it as json.'''
    parser = reqparse.RequestParser()
    parser.add_argument('PurchaseId')
    parser.add_argument('ItemId')
    parser.add_argument('Count')
    return parser.parse_args()
