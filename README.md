# 歌姬 / geji-ts-bot

基于 [Rhythm](https://github.com/Kokoro-js/rhythm) 的个人 TeamSpeak 点歌部署与补丁工具，不是 Rhythm 官方完整源码发行版。

## 功能
- TS 点歌、网易云音乐搜索、队列与网页控制台。
- 96kbps Opus 限速和484字节帧上限，修复超大语音包无声；现场已确认可听。
- 中文指令：来这、点歌 歌名、暂停、继续、切歌、当前、歌单、音量 30、模式 随机、跳转 1:30、帮助。
- 清空队列保留当前歌曲；去除所有歌单会清空并停止；清空/删除仅限房主。
- @歌姬 点歌 歌名、@歌姬♪ 点歌 歌名；同频道用户首次点歌自动获得临时成员资格。该新增授权流程尚需另一位用户端到端验收。
- 昵称默认歌姬♪。自备有权使用的头像放 data/avatar.jpg，自动上传；本仓库不提供动漫图片。
- 网易云desktop-eapi扫码与本地Cookie导入；扫码确认仍未验证成功，不能承诺VIP歌曲可用。

## 环境及版本
Windows Docker Desktop + WSL2，或Linux amd64 Docker Compose；Python3用于生成补丁。
补丁针对0.5.12镜像的特定bundle，输入SHA256由patch.json严格校验。latest变化后可能拒绝应用，不要强制跳过校验。
上游实际镜像由ghcr.io/pluxeljs提供，需遵守上游使用条款。建议自行固定镜像digest，升级前重新审核补丁。

## 安装
1. 复制.env.example到.env，创建data、music、patches目录。
2. docker compose pull rhythm gateway
3. 从所下载rhythm镜像提取原版/app/app.mjs（不要使用已修改过的容器）：

```sh
docker create --name geji-extract ghcr.io/pluxeljs/rhythm:latest
docker cp geji-extract:/app/app.mjs upstream-app.mjs
docker rm geji-extract
python apply_patch.py upstream-app.mjs patches/app.mjs
docker compose up -d --wait
```

输入不匹配时停止安装，使用与manifest匹配的上游镜像，不要覆盖其他版本。
点歌页 http://127.0.0.1:3310/ ，后台 http://127.0.0.1:3311/plugins 。只监听本机；不要把管理端口公开。
后台TeamSpeakClientPlugin配置服务器地址、真实服务器UID与持久化机器人身份；启用三个TeamSpeak插件。不要将IP当作UID。
默认网易云来源netease。同频道发“来这”，再发“点歌 歌名”。

## 登录
后台网易云页面生成新二维码，用本人手机确认。重启后旧二维码失效。8821或风控错误可能需要官方网页登录后的本地Cookie导入。
如确需导入，将MUSIC_U凭据只写入本机data/netease-cookie.txt，重启后验证并保存到Vault，临时文件会被删除（无论验证是否成功）。不要提交或发给他人。

## 备份与回滚
修改前备份patches/app.mjs、compose.yaml及完整data目录。替换补丁后重建容器；回滚用备份文件并重建。已有真实队列不要为测试直接清空。
本仓库不含账号数据、Cookie、Vault、原始日志、聊天记录或服务器凭据。

## 已知限制
这是对上游编译产物的精确补丁，维护成本高；网站主体来自运行时上游镜像。扫码、自动授权与跨频道切换并非全面验证。修改权限规则后应使用独立普通成员账号验收。

## 来源与权利
Rhythm、相关依赖和原编译代码的权利属于各自作者。本仓库只分发部署配置及修改所需的差异数据，不授予上游代码、音乐或头像的使用权。感谢Claude提供v1/v2/v3修复方案，Codex完成本机部署和后续调整。
