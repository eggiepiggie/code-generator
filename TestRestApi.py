from flask import Flask, request
from flask_restful import Api
from app.rest_api.Department import *
from app.rest_api.Item import *
from app.rest_api.PriceHistory import *
from app.rest_api.StockLevel import *
from app.rest_api.PurchaseItemList import *
from app.rest_api.Purchase import *

app = Flask(__name__)
api = Api(app)

api.add_resource(DepartmentGetAll,		'/department')
api.add_resource(DepartmentById,		'/department/<int:departmentId>')
api.add_resource(DepartmentItems,		'/department/<int:departmentId>/items')

api.add_resource(ItemGetAll,			'/item')
api.add_resource(ItemById,				'/item/<int:itemId>')
api.add_resource(ItemPriceHistorys,		'/item/<int:itemId>/priceHistory')
api.add_resource(ItemStockLevels,		'/item/<int:itemId>/stockLevel')
api.add_resource(ItemPurchaseItemLists,	'/item/<int:itemId>/purchaseItemList')

api.add_resource(PriceHistoryGetAll,	'/priceHistory')
api.add_resource(PriceHistoryById,		'/priceHistory/<int:priceHistoryId>')

api.add_resource(StockLevelGetAll,		'/stockLevel')
api.add_resource(StockLevelById,		'/stockLevel/<int:stockLevelId>')

api.add_resource(PurchaseItemListGetAll,		'/purchaseItemList')
api.add_resource(PurchaseItemListById,			'/purchaseItemList/<int:purchaseItemListId>')

api.add_resource(PurchaseGetAll,		'/purchase')
api.add_resource(PurchaseById,			'/purchase/<int:purchaseId>')
api.add_resource(PurchasePurchaseItemLists,			'/purchase/<int:purchaseId>/purchaseItemList')

if __name__ == "__main__":
	app.run(port='5000')
