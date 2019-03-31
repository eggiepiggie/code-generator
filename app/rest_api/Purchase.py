# ===================================================================
#  WARNING: This is an auto-generated file. Do not modify this file.
# ===================================================================
#
#   Purchase REST API Class
#
# ===================================================================
#  Generated on: 2019-03-29 23:14:57.145904
# ===================================================================
from flask_restful import Resource, reqparse
from app.bo.Purchase import PurchaseBO
from app.dao.Purchase import purchaseDAO


class PurchaseGetAll(Resource):

    def get(self):
        purchases = purchaseDAO.getAllPurchases()
        purchasesJson = []
        for purchase in purchases:
            purchasesJson.append(purchase.toJson())
        return purchasesJson

    def post(self):
        args = getParameters(reqparse.RequestParser())
        purchase = PurchaseBO()
        purchase.setCustomer(args['Customer'])
        purchase.setPurchaseDate(args['PurchaseDate'])
        purchase.save()
        return purchase.purchase.toJson()


class PurchaseById(Resource):

    def get(self, purchaseId):
        purchase = purchaseDAO.getPurchaseById(purchaseId)
        return purchase.toJson()

    def put(self, purchaseId):
        args = getParameters(reqparse.RequestParser())
        purchaseDO = purchaseDAO.getPurchaseById(purchaseId)
        purchase = PurchaseBO(purchaseDO)
        purchase.setCustomer(args['Customer'])
        purchase.setPurchaseDate(args['PurchaseDate'])
        purchase.update()
        return purchase.purchase.toJson()

    def delete(self, purchaseId):
        return purchaseDAO.deleteById(purchaseId)


class PurchasePurchaseItemLists(Resource):
    def get(self, purchaseId):
        purchaseDO = purchaseDAO.getPurchaseById(purchaseId)
        purchase = PurchaseBO(purchaseDO)
        purchaseItemLists = purchase.getPurchaseItemLists()
        results = []
        for purchaseItemList in purchaseItemLists:
            results.append(purchaseItemList.toJson())
        return results


def getParameters(parser):
    '''Takes the requests body and returns it as json.'''
    parser = reqparse.RequestParser()
    parser.add_argument('Customer')
    parser.add_argument('PurchaseDate')
    return parser.parse_args()
