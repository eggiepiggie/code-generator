from app.bo.Department import DepartmentBO
from app.bo.Item import ItemBO
from app.bo.StockLevel import StockLevelBO

def createItemBO(name, description, weight, isStocked, colour, department):
	item = ItemBO()
	item.setName(name)
	item.setDescription(description)
	item.setWeight(weight)
	item.setIsStocked(isStocked)
	item.setColour(colour)
	item.setDepartment(department.department)
	item.save()
	return item

def createDepartmentBO(name, description):
	department = DepartmentBO()
	department.setName(name)
	department.setDescription(description)
	department.save()
	return department

def createStockLevelBO(count, nextShipment, item):
	stockLevel = StockLevelBO()
	stockLevel.setCount(count)
	stockLevel.setNextShipment(nextShipment)
	stockLevel.setItem(item.item)
	stockLevel.save()
	return stockLevel