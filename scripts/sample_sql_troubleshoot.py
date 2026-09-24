USE AAD 
GO

DECLARE @order VARCHAR(30) = '###' ----compare HJ and FT Status----
SELECT 'HJ & FT STATUS', o.status as HJStatus, o.order_date, o.route, o.store_order_number, o.carrier, o.latest_ship_date, o.ship_to_state, o.ship_to_country_code,oh.OrderID, oh.Status as FTStatus,oh.ContainerizationError, oh.BlueToteOrder,oh.QtyRequired, oh.QtyPicked, oh.QtyShipped
FROM AAD.dbo.t_order o WITH(NOLOCK)
LEFT JOIN FASTTRAK.vitamz.vitahost.tblOrderHeader oh WITH(NOLOCK)
ON o.order_number = oh.OrderNumber COLLATE Latin1_General_CI_AI
WHERE o.order_number = @order

SELECT comment_text  
FROM dbo.t_order_comment 
WHERE order_number = @order

SELECT 't_order_date' AS t_order_date, * 
FROM dbo.t_order_date 
WHERE order_number = @order
SELECT 'status_log',* 
FROM dbo.t_order_status_log WITH (NOLOCK) 
WHERE order_number = @order  

SELECT * 
FROM dbo.t_order_additional_data oda WITH (NOLOCK)
JOIN t_order o ON oda.identifier = o.store_order_number
WHERE o.order_number = @order ----

——FROM D365——
SELECT 'D365 SO Header',TransactionCode, TranDttm, WhseID, OrderNumber, StoreOrder, EntryDate, ShipVia, Residential 
FROM dbo.T_AL_DAX_ORDER_MASTER_SO 
WHERE OrderNumber= @order

SELECT distinct ord.order_number, ord.store_order_number, dax.LineNumber,dax.ItemNumber AS AXItemNumber, dax.ExpectedQty, dax.VCLineStatus,mast.alt_item_number, mast.item_number as UPC, mast.inv_cat, mast.inspection_code, mast.haz_material
FROM T_AL_DAX_ORDER_LINE dax with(nolock)
LEFT JOIN t_order ord with(nolock) on dax.OrderNumber=ord.order_number collate Latin1_General_BIN
LEFT JOIN t_item_master mast with(nolock) on dax.ItemNumber=mast.alt_item_number collate Latin1_General_BIN
WHERE dax.OrderNumber= @order

---- when qty_shipped is 0, there is usually a remove Requirements in ParcelLog----
SELECT 'ORDER_DETAIL', * 
FROM t_order_detail WITH (NOLOCK) 
WHERE order_number = @order

SELECT 'ORDERDETAILS WITH LOCS', si.item_number, im.alt_item_number as AX#, od.line_number as line#, im.description,od.bo_qty,od.bo_description, im.haz_material, im.unit_weight, im.nested_volume, si.actual_qty, si.type, si.status, l.type, l.location_id, l.aisle,  pzl.location_id AS 'PickZoneLoca', tl.Location AS 'FastTrak.tblLocation', tl.Area
FROM t_order_detail od
LEFT JOIN t_stored_item siON od.item_number = si.item_number
LEFT JOIN t_item_master im ON si.item_number= im.item_number
LEFT JOIN t_location l ON si.location_id = l.location_id
LEFT JOIN t_pick_zone_loca pzl WITH(NOLOCK) ON pzl.location_id = l.location_id
LEFT JOIN FASTTRAK.vitamz.vitahost.tblLocation tl WITH(NOLOCK) ON tl.Location COLLATE Latin1_General_BIN= l.location_id
WHERE od.order_number = @order

SELECT 'FWDPICK',* FROM t_fwd_pick with(nolock) where item_number in (SELECT item_number from t_order_detail with(nolock) 
WHERE order_number=@order)
SELECT 'MISSING CUBISCAN', mast.item_number, mast.alt_item_number as AX#,od.line_number as line#, mast.description
FROM t_item_master mast with(nolock)
LEFT JOIN  t_stored_item si with(nolock) on mast.item_number=si.item_number
LEFT JOIN t_cubiscan_shipping_dimensions cb with(nolock) on mast.item_number=cb.item_number
LEFT JOIN t_order_detail od
ON si.item_number = od.item_number
WHERE mast.inspection_code !='D' 
AND ((cb.length=0 or cb.length is null) or (cb.width=0 or cb.width is NULL) or (cb.height=0 or cb.height is NULL) or (cb.unit_volume=0 or cb.unit_volume is NULL) or (cb.nested_volume=0 or cb.nested_volume is NULL))AND od.order_number = @orderGROUP by mast.item_number, mast.alt_item_number,od.line_number, mast.descriptionorder by mast.item_number 

SELECT 'TBLPARCEL', p.ParcelID, p.ParcelType, p.Status, p.InductionStatus, p.ManifestStatus, p.QtyRequired, p.QtyPicked,p.CheckWeighed, p.QCComplete, p.QCFailed, p.Weight 
FROM  FASTTRAK.vitamz.vitahost.tblParcel p
JOIN FASTTRAK.vitamz.vitahost.tblOrderHeader oh WITH(NOLOCK)
ON p.OrderID = oh.OrderID
WHERE oh.OrderNumber =  @order 

SELECT 'PARCEL DETAIL', PD.ParcelID, P.Status, P.ParcelNumber, PD.ItemNumber, PD.QCComplete,PD.QtyRequired, PD.QtyPicked, SUM(PD.QtyRequired- PD.QtyPicked) as Missing, PD.PickCount
FROM FASTTRAK.vitamz.vitahost.tblOrderHeader OH
JOIN FASTTRAK.vitamz.vitahost.tblParcel P ON OH.OrderID = P.OrderID
JOIN FASTTRAK.vitamz.vitahost.tblParcelDetail PD ON P.ParcelID = PD.ParcelID
WHERE OH.OrderNumber = @orderGROUP BY OH.OrderID, PD.ParcelID, P.Status, P.ParcelNumber, PD.ItemNumber, PD.QCComplete,PD.QtyRequired, PD.QtyPicked, PD.QtyRequired, PD.QtyPicked, PD.PickCount 

SELECT 'PICK LOCATION', order_number, line_number, pick_id, type, status, item_number, planned_quantity,picked_quantity, loaded_quantity, pick_location, pick_area
FROM AAD.dbo.t_pick_detail WITH(NOLOCK) 
WHERE order_number = @order

SELECT 'DEFICIENT PICK', order_number, line_number, pick_id, type, status, item_number, planned_quantity, picked_quantity, loaded_quantity, pick_location, pick_area
FROM AAD.dbo.t_pick_detail WITH(NOLOCK)
WHERE order_number = @order    
AND planned_quantity > picked_quantity     

----------- SHORT PICKS
SELECT 'SHORTPICKS', * 
FROM tblShortPick 
WHERE order_number = @order 

---- confirm items with 0 qty from order detail are missing from Pick Detail----
SELECT 'PICK DETAIL', pd.order_number, pd.line_number, pd.pick_id, pd.type, pd.status, pd.item_number, pd.planned_quantity, pd.picked_quantity, pd.loaded_quantity,pd.pick_location, pd.pick_area, loc.zone
FROM AAD.dbo.t_pick_detail pd WITH(NOLOCK)
JOIN t_location loc WITH (NOLOCK) ON pd.pick_location = loc.location_id
WHERE order_number = @order 

SELECT 'PARCEL PICKS', PZ.ParcelID, PZ.Area, PZ.Zone, PPI.QtyRequired, PPI.QtyPicked, SUM(PPI.QtyRequired- PPI.QtyPicked) as Missing,PPI.Visited, PPI.ItemNumber
FROM FASTTRAK.vitamz.vitahost.tblOrderHeader OH
LEFT JOIN  FASTTRAK.vitamz.vitahost.tblParcel PON OH.OrderID = P.OrderIDLeft Join FASTTRAK.vitamz.vitahost.tblParcelPickZone PZ ON P.ParcelID = PZ.ParcelID
LEFT JOIN FASTTRAK.vitamz.vitahost.tblParcelPickLocation PL ON PZ.ParcelID = PL.ParcelID
LEFT JOIN FASTTRAK.vitamz.vitahost.tblParcelPickItem PPI ON PZ.ParcelID = PPI.ParcelID
WHERE OH.OrderNumber = @order
GROUP BY PZ.ParcelID, PZ.Area, PZ.Zone, PPI.QtyRequired, PPI.QtyPicked,PPI.Visited, PPI.ItemNumber-

--- If Remove Requirements filter does not return any values, remove that filter and re- query----
SELECT 'PARCELLOG', oh.OrderNumber, pl.ParcelID, pl.OrderID, pl.LogType, pl.LogTime, pl.UserName, pl.ItemNumber, pl.Qty, pl.ErrorMessage, pl.User1
FROM FASTTRAK.vitamz.vitahost.tblParcelLog pl
JOIN FASTTRAK.vitamz.vitahost.tblOrderHeader oh ON oh.OrderID = pl.OrderID
WHERE oh.OrderNumber = @order
ORDER BY pl.LogTime--LogType = 'Induct Calvel'
--AND pl.User1 = 'Remove Requirement'  

----Select the ItemNumber from tblParcelLog with Remove Requirements, and filter in this query----
SELECT 'TRAN LOG', tran_type, description, start_tran_date, start_tran_time, employee_id, hu_id, control_number, location_id, item_number, tran_qty, location_id_2
FROM AAD.dbo.t_tran_log WITH(NOLOCK)
WHERE control_number = @order    
--AND item_number = '076280884500'
ORDER BY start_tran_date, start_tran_time 

SELECT 'tblUpLoad', * 
FROM FASTTRAK.vitaxfer.dbo.tblUpLoad 
WHERE order_number = @order

SELECT 'tblDownLoad', * 
FROM FASTTRAK.vitaxfer.dbo.tblDownLoad 
WHERE order_number = @order 

SELECT 'SHIP INFO', ecom_ship_complete, track_no, carrier 
FROM FASTTRAK.vitaxfer.dbo.tblVitaFreight
WHERE pkgid = @order 

SELECT 'SOUP', TranDttm, WarehouseID, CarrierCode, Status, TotalWeight, VCTTracking, LoadID  
FROM T_AL_DAX_IVC_MASTER
WHERE OrderNumber = @order 

SELECT 'SOUP DETAILS', mast.OrderNumber,mast.Status,m.item_number,det.ItemNumber, det.LineNumber,CONVERT(INT,det.QuantityShipped) AS QtyShipped
FROM dbo.T_AL_DAX_IVC_MASTER mast WITH(NOLOCK)
JOIN dbo.T_AL_DAX_IVC_DETAIL det WITH(NOLOCK) ON mast.hjs_node_id=det.hjs_parent_idLEFT join t_item_master m WITH(NOLOCK) ON det.ItemNumber=m.alt_item_number COLLATE Latin1_General_BIN
WHERE mast.OrderNumber=@order
ORDER BY mast.Status 

SELECT 'VITAFREIGHT', vf.carname, vf.track_no, vf.prod_desc, vf.act_wgt, vf.ecom_ship_complete, vf.ship_pallet_id,vf.dock_status, pm.PalletLP, tm.TruckLP, tm.CloseDate as TruckClosed 
FROM FASTTRAK.vitaxfer.dbo.tblVitaFreight vf
LEFT JOIN FASTTRAK.vitaxfer.shipdock.tblPalletMaster pm    on vf.ship_pallet_id = pm.PalletLP
LEFT JOIN FASTTRAK.vitaxfer.shipdock.tblTruckMaster tm    on pm.TruckID = tm.TruckLP
WHERE vf.pkgid = @order"
