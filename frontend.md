###这里里面的所有API都是login require的


#### 广告投放



#### 长期贷款 /game/long_loan POST content_type="application/json"
json keys
- value: (int) 贷款额（正整数）
- year: (int) 年限（[1..6]）

return
- {'code': 200, 'msg': '成功'}
- {'code': 400, 'msg': '贷款额度不足'}


#### 短期贷款 /game/short_loan POST content_type="application/json"
json keys
- value: (int) 贷款额（正整数）

return
- {'code': 200, 'msg': '成功'}
- {'code': 400, 'msg': '贷款额度不足'}


#### 下原料订单 /game/order_raw_material POST content_type="application/json"
json keys
- r1: (int) r1原材料数量
- r2: (int) r2原材料数量
- r3: (int) r3原材料数量
- r4: (int) r4原材料数量

return
- {'code': 200, 'msg': '成功'}


#### 购买租用厂房 /game/but_rent_workshop POST content_type="application/json"
json keys
- cmd: (string) 买还是租，你搞个单选框('buy' or 'rent')
- workshop_type: (string) 厂房类型，单选框('small', 'medium', 'big')

return
- {'code': 200, 'msg': '成功'}
- {'code': 400, 'msg': '现金不足'}


#### 新建生产线 /game/new_line POST content_type="application/json"
json keys
- workshop_id: (int)
- line_id: (int)
- line_type: (string) 生产线类型，单选框('hand', 'aoto', 'flex')
- product_type: (string) 产品类型，单选框('p1','p2','p3','p4')

return
- {'code': 200, 'msg': '成功'}
- {'code': 400, 'msg': '现金不足'}


#### 在建生产线 /game/construct_line POST content_type="application/json"
json keys
- workshop_id: (int)
- line_id: (int)

return
- {'code': 200, 'msg': '成功'}
- {'code': 400, 'msg': '现金不足'}


#### 生产线转产 /game/switch_product POST content_type="application/json"
json keys
- workshop_id: (int)
- line_id: (int)
- product_type: (string) 转成什么产品类型，单选框('p1','p2','p3','p4')

return
- {'code': 200, 'msg': '成功'}
- {'code': 400, 'msg': '现金不足'}


#### 变卖生产线 /game/sell_line POST content_type="application/json"
json keys
- workshop_id: (int)
- line_id: (int)

return
- {'code': 200, 'msg': '成功'}


#### 紧急采购 /game/emergency_buy POST content_type="application/json"
json keys
- r1: (int) r1原材料数量，用户输入
- r2: 同上
- r3
- r4
- p1: (int) p1产品数量，用户输入
- p2: 同上
- p3
- p4

return
- {'code': 200, 'msg': '成功'}
- {'code': 402, 'msg': '没钱了，吃屎'}


#### 开始下一批生产 /game/produce POST content_type="application/json"
json keys
- workshop_id
- line_id

return
- {'code': 200, 'msg': '成功'}
- {'code': 402, 'msg': '没钱了，吃屎'}


#### 交货 /game/delivery POST content_type="application/json"
json keys
- order_id: 

return
- {'code': 200, 'msg': '成功'}
- {'code': 401, 'msg': '产品不够，不能交货'}


#### 产品研发 /game/product_dev POST content_type="application/json"
json keys
- product_types: 要研发的产品，复选框['p1', 'p2', 'p3', 'p4']

return
- {'code': 200, 'msg': '成功'}
<!-- 已经研发好了不能点 -->


#### 新市场开拓 /game/market_dev POST content_type="application/json"
json keys
- markets: 要开拓的市场，复选框['本地','区域','国内','亚洲','国际']

return
- {'code': 200, 'msg': '成功'}


#### 出售库存 /game/sell_stock POST content_type="application/json"
json keys
- r1: r1原材料数量，用户输入
- r2
- r3
- r4
- p1
- p2
- p3
- p4

return
- {'code': 200, 'msg': '成功'}


#### 贴现 /game/discount_receiable POST content_type="application/json"
json keys
- recei1: 一账期应收款贴现额，用户输入
- recei2:
- recei3:
- recei4:

return
- {'code': 200, 'msg': '成功'}
- {'code': 401, 'msg': '应收款不存在'}


#### ISO资格认证 /game/iso_dev POST content_type="application/json"
json keys
- ISOs: 要认证的资格，复选框['iso9','iso14']
