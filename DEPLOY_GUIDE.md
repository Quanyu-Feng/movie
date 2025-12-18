# myMovie Vercel 部署指南

## 📁 项目结构检查

✅ 您的项目结构正确：

```
myMovie/
├── api/
│   ├── __init__.py          ✅ Python 包标识
│   ├── _db.py              ✅ 数据库连接模块
│   ├── login.py            ✅ 登录 API
│   ├── register.py         ✅ 注册 API
│   ├── favorites.py        ✅ 收藏 API
│   └── history.py          ✅ 历史 API
├── assets/                  ✅ 静态资源
├── *.html                   ✅ 前端页面
├── requirements.txt         ✅ Python 依赖
├── vercel.json             ✅ Vercel 配置
└── .vercelignore           ✅ 忽略文件
```

## 🚀 部署步骤

### 步骤 1: 设置环境变量

在 Vercel Dashboard 中：

1. 进入项目 → Settings → Environment Variables
2. 添加以下变量：

| Key | Value | Environment |
|-----|-------|-------------|
| `DATABASE_URL` | `postgresql://postgres.jihfdpkcnuvkmarfkgoy:123456@aws-0-us-west-2.pooler.supabase.com:6543/postgres` | Production, Preview, Development |

### 步骤 2: 部署

**方式 A - 通过 Git 部署（推荐）：**
```bash
git add .
git commit -m "准备部署到 Vercel"
git push
```
Vercel 会自动检测并部署。

**方式 B - 使用 Vercel CLI：**
```bash
# 安装 Vercel CLI（如果还没安装）
npm i -g vercel

# 部署到生产环境
vercel --prod
```

## ⚠️ 常见问题

### 问题 1: "Environment Variable references Secret"
**原因**: 环境变量未设置  
**解决**: 在 Vercel Dashboard 中设置 `DATABASE_URL`

### 问题 2: "Module not found"
**原因**: 缺少依赖或 `__init__.py`  
**解决**: 
- 确保 `requirements.txt` 完整
- 确保 `api/__init__.py` 存在

### 问题 3: "Function exceeded timeout"
**原因**: 数据库连接超时  
**解决**: 
- 检查数据库 URL 是否正确
- 检查 Supabase 数据库是否在线

### 问题 4: CORS 错误
**原因**: 跨域请求被阻止  
**解决**: API 已配置 CORS，应该没问题

## 📝 部署检查清单

在部署前确认：

- [ ] `api/__init__.py` 文件存在
- [ ] `requirements.txt` 包含所有依赖
- [ ] `vercel.json` 配置正确
- [ ] 在 Vercel Dashboard 设置了 `DATABASE_URL` 环境变量
- [ ] 所有 API 文件（login.py, register.py, favorites.py, history.py）都已更新
- [ ] `.vercelignore` 文件存在

## 🔍 测试 API 端点

部署成功后，测试以下端点：

```bash
# 健康检查（如果有）
curl https://your-app.vercel.app/api/login

# 注册
curl -X POST https://your-app.vercel.app/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'

# 登录
curl -X POST https://your-app.vercel.app/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'
```

## 💡 提示

1. **首次部署可能需要 3-5 分钟**
2. **查看部署日志** 以了解任何错误
3. **使用 Preview 部署** 测试更改，然后再部署到生产环境
4. **数据库密码安全**: 建议更改默认密码 "123456"

## 📞 如果还是失败

请查看 Vercel 部署日志：
1. 打开 Vercel Dashboard
2. 选择您的项目
3. 点击 "Deployments"
4. 选择失败的部署
5. 查看 "Build Logs" 和 "Function Logs"

将错误信息提供给我，我可以进一步帮助您！

