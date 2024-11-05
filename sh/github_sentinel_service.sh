#!/bin/bash

# 配置文件路径
PID_FILE="/var/run/github_sentinel.pid"
LOG_FILE="/var/log/github_sentinel.log"
PROGRAM_PATH="/path/to/your/GitHubSentinel"  # 修改为实际路径
PROGRAM_CMD="python3 $PROGRAM_PATH/main.py"

start() {
    # 检查是否已经有进程在运行
    if [ -f "$PID_FILE" ]; then
        echo "服务已经在运行。"
        exit 1
    fi

    # 启动程序并将 PID 写入文件
    echo "启动服务..."
    nohup $PROGRAM_CMD > $LOG_FILE 2>&1 &
    echo $! > $PID_FILE
    echo "服务已启动，PID: $(cat $PID_FILE)"
}

stop() {
    # 检查 PID 文件是否存在
    if [ ! -f "$PID_FILE" ]; then
        echo "服务未运行。"
        exit 1
    fi

    # 获取 PID 并停止进程
    PID=$(cat $PID_FILE)
    echo "停止服务 (PID: $PID)..."
    kill $PID

    # 删除 PID 文件
    rm -f $PID_FILE
    echo "服务已停止。"
}

restart() {
    # 停止服务
    stop
    # 启动服务
    start
}

status() {
    # 检查服务状态
    if [ -f "$PID_FILE" ]; then
        PID=$(cat $PID_FILE)
        echo "服务正在运行，PID: $PID"
    else
        echo "服务未运行。"
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
