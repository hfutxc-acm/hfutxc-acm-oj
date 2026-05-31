#!/bin/bash
echo -e "\e[36m🚀 启动 HFUTXC ACM OJ 研发环境...\e[0m"

# 1. 检查并清理端口冲突
check_and_kill_port() {
    local port=$1
    local name=$2
    # 查找占用该端口的进程PID
    local pid=$(lsof -t -i:$port 2>/dev/null)
    if [ ! -z "$pid" ]; then
        echo -e "\e[33m⚠️ 检测到端口 $port 被进程 $pid 占用 ($name)，正在清理...\e[0m"
        kill -9 $pid 2>/dev/null
        sleep 0.5
    fi
}

check_and_kill_port 8000 "Backend FastAPI"
check_and_kill_port 5173 "Frontend Vite"

# 2. 启动后端 FastAPI
echo -e "\e[32m[Backend] 正在后台启动 FastAPI 服务 (http://localhost:8000)...\e[0m"
cd /home/ikun/PycharmProjects/hfutxc-acm-oj/backend
.venv/bin/uvicorn main:app --port 8000 --reload > /dev/null 2>&1 &
BACKEND_PID=$!

# 3. 启动前端 Vite
echo -e "\e[32m[Frontend] 正在启动 Vite 服务 (http://localhost:5173)...\e[0m"
cd /home/ikun/PycharmProjects/hfutxc-acm-oj/frontend
npm run dev &
FRONTEND_PID=$!

# 4. 捕获 Ctrl+C 信号以优雅退出所有子进程
cleanup() {
    echo -e "\n\e[31m🛑 正在关闭 OJ 研发服务...\e[0m"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "\e[32m✓ 后端 (PID: $BACKEND_PID) 与前端 (PID: $FRONTEND_PID) 已成功终止。\e[0m"
    exit 0
}

trap cleanup SIGINT SIGTERM

# 5. 保持运行并等待
wait
