SELECT
    sod.SalesOrderID,
	sod.ProductID,
	p.Name,
	sod.UnitPrice,
	sod.UnitPriceDiscount,
	max(case
		when pod.UnitPrice IS NOT NULL then pod.UnitPrice
		when wor.ActualCost IS NOT NULL then wor.ActualCost
		else pch.StandardCost
	end) as [ProductCost],
	sod.ModifiedDate
FROM Sales.SalesOrderDetail sod
left join Production.Product p ON sod.ProductID = p.ProductID
left join Purchasing.PurchaseOrderDetail pod ON (sod.ProductID = pod.ProductID and pod.StockedQty > 0 and sod.ModifiedDate >= pod.DueDate)
left join Production.WorkOrderRouting wor ON (sod.ProductID = wor.ProductID and sod.ModifiedDate > wor.ActualEndDate)
left join Production.ProductCostHistory pch ON (sod.ProductID = pch.ProductID and ((sod.ModifiedDate >= pch.StartDate and (sod.ModifiedDate <= pch.EndDate or pch.EndDate IS NULL))))
GROUP BY sod.SalesOrderID, sod.ProductID, p.Name, sod.UnitPrice, sod.UnitPriceDiscount, sod.ModifiedDate
order by SalesOrderID