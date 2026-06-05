#!/bin/bash
# ============================================================
# sync-wiki.sh — 无需重新部署，直接热更新知识库
# 用法：
#   bash sync-wiki.sh          # 仅同步（wiki/site 已经 build 好）
#   bash sync-wiki.sh --build  # 先 mkdocs build 再同步
# ============================================================

set -e

REMOTE_HOST="icpc"
LOCAL_WIKI="./wiki/site"

# 可选：先构建
if [ "$1" = "--build" ]; then
  echo "🔨 构建知识库（mkdocs build）..."
  if ! command -v mkdocs &>/dev/null; then
    echo "❌ 未找到 mkdocs，请先安装：pip install mkdocs-material"
    exit 1
  fi
  cd wiki && mkdocs build --quiet && cd ..
  echo "✅ 构建完成"
fi

echo "🔍 查找远程前端容器..."
CONTAINER_ID=$(ssh "$REMOTE_HOST" "docker ps --filter 'name=frontend' --format '{{.ID}}' | head -1")

if [ -z "$CONTAINER_ID" ]; then
  echo "❌ 未找到前端容器，请确认 Coolify 服务正在运行"
  exit 1
fi

echo "📦 前端容器：$CONTAINER_ID"
echo "🚀 正在同步 wiki/site 到容器..."

# 先把本地 wiki/site 打包传到远程，再 docker cp 进容器
tar -czf /tmp/wiki-site.tar.gz -C wiki/site .
scp /tmp/wiki-site.tar.gz "$REMOTE_HOST:/tmp/wiki-site.tar.gz"
ssh "$REMOTE_HOST" "
  docker exec $CONTAINER_ID mkdir -p /usr/share/nginx/html/wiki
  docker cp /tmp/wiki-site.tar.gz $CONTAINER_ID:/tmp/
  docker exec $CONTAINER_ID tar -xzf /tmp/wiki-site.tar.gz -C /usr/share/nginx/html/wiki
  rm /tmp/wiki-site.tar.gz
"
rm /tmp/wiki-site.tar.gz

echo "✅ 知识库同步完成！访问 http://192.168.31.131:5174/wiki/ 查看效果"
