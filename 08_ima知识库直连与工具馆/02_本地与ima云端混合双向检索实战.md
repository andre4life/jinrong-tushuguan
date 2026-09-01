# 02 本地与ima云端混合双向检索实战

## 1. 联合检索工具 \`ima_finance_hub.py\` 核心功能

金融图书馆内置了专用的 Python 检索工具 \`ima_finance_hub.py\`，实现本地 Markdown 智库与腾讯云端 ima 知识库的秒级统一检索。

### 常用命令示范：
```powershell
# 1. 列出当前账号下所有可用的云端 ima 知识库
python D:\Antigravity输出\金融图书馆\ima_finance_hub.py list

# 2. 全库联合检索（本地金融图书馆 + 腾讯云端 ima 知识库）
python D:\Antigravity输出\金融图书馆\ima_finance_hub.py search 家族信托
python D:\Antigravity输出\金融图书馆\ima_finance_hub.py search 沪深300
python D:\Antigravity输出\金融图书馆\ima_finance_hub.py search 杨笑
python D:\Antigravity输出\金融图书馆\ima_finance_hub.py search 美林时钟
```
