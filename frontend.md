#### 广告投放
参数:
  - dasd


#### 长期贷款 /Company/long_loan POST

params
- company_id: 公司id
- value: 贷款额（正整数）
- year: 年限（[1..6]）

return
- {'code': 200, 'msg': '成功'}
- {'code': 401, 'msg': '额度不足, 可用额度xxx'}


#### 短期贷款 /Company/short_loan POST
params
- company_id
- value: 贷款额（正整数）

return
- {'code': 200, 'msg': '成功'}
- {'code': 401, 'msg': '额度不足, 可用额度xxx'}


#### 下原料订单 /Company/order_raw_material POST
params
- company_id
- num_r1: R1原材料数量，用户输入
- num_r2
- num_r3
- num_r4

return
- {'code': 200, 'msg': '成功'}
<!-- - {'code': 400, 'msg': '成功'} -->


#### 购买租用厂房 /Company/but_rent_workshop POST
params
- company_id
- cmd: 买还是租，你搞个单选框('buy' or 'rent')
- workshop_type: 厂房类型，单选框('small', 'medium', 'big')

return
- {'code': 200, 'msg': '成功'}
- {'code': 402, 'msg': '没钱了，吃屎'}


#### 新建生产线 /Company/new_line
params
- company_id
- workshop_id
- line_id
- line_type: 生产线类型，单选框('hand', 'aoto', 'flex')
- product_type: 产品类型，单选框('p1','p2','p3','p4')

return
- {'code': 200, 'msg': '成功'}
- {'code': 402, 'msg': '没钱了，吃屎'}


#### 在建生产线 /Company/construct_line
params
- company_id
- workshop_id
- line_id

return
- {'code': 200, 'msg': '成功'}
- {'code': 402, 'msg': '没钱了，吃屎'}


#### 生产线转产 Company/switch_product
params
- company_id
- workshop_id
- line_id
- product_type: 转成什么产品类型，单选框('p1','p2','p3','p4')

return
- {'code': 200, 'msg': '成功'}
- {'code': 402, 'msg': '没钱了，吃屎'}


#### 变卖生产线 Company/sell_line
params
- company_id
- workshop_id
- line_id

return
- {'code': 200, 'msg': '成功'}


#### 紧急采购 Company/emergency_buy
params
- company_id
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
- {'code': 402, 'msg': '没钱了，吃屎'}


#### 开始下一批生产 Company/produce
params
- company_id
- workshop_id
- line_id

return
- {'code': 200, 'msg': '成功'}
- {'code': 402, 'msg': '没钱了，吃屎'}


#### 交货 Company/delivery
params
- company_id
- order_id

return
- {'code': 200, 'msg': '成功'}
- {'code': 401, 'msg': '产品不够，不能交货'}


#### 产品研发 Company/product_dev
params
- company_id
- product_types: 要研发的产品，复选框['p1', 'p2', 'p3', 'p4']

return
- {'code': 200, 'msg': '成功'}
<!-- 已经研发好了不能点 -->


#### 新市场开拓 Company/market_dev
params
- company_id
- markets: 要开拓的市场，复选框['本地','区域','国内','亚洲','国际']

return
- {'code': 200, 'msg': '成功'}
<!-- 已经开拓好了不能点 -->


#### 出售库存
params
- company_id
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


#### 贴现
params
- company_id
- recei1: 一账期应收款贴现额，用户输入
- recei2:
- recei3:
- recei4:

return
- {'code': 200, 'msg': '成功'}
- {'code': 401, 'msg': '应收款不存在'}


#### ISO资格认证
params
- company_id
- ISOs: 要认证的资格，复选框['iso9','iso14']
