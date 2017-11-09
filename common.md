#### 拿csrf token ./get_token get
no params


#### 注册 ./register POST
params
- username: 用户名
- password: 密码
- email: 邮箱


#### 登录 ./login POST
params
- username: 用户名
- password: 密码

#### 登出 ./logout POST
no params

#### 改密码 ./modify_password POST
**login required**
params
- new_password: 新密码


#### 开始游戏 ./start_game
**login required**
no params
