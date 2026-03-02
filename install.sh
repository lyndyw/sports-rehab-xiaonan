#!/bin/bash

# 运动康复小南 - 安装脚本
# macOS / Linux 一键安装

set -e

echo "💪 运动康复小南 - 安装程序"
echo "========================="
echo ""

# 检测操作系统
case "$(uname -s)" in
    Darwin)
        SKILLS_DIR="$HOME/Library/Application Support/LobsterAI/SKILLs"
        ;;
    Linux)
        SKILLS_DIR="$HOME/.config/LobsterAI/SKILLs"
        ;;
    MINGW*|MSYS*|CYGWIN*)
        SKILLS_DIR="$APPDATA/LobsterAI/SKILLs"
        ;;
    *)
        echo "❌ 不支持的操作系统"
        exit 1
        ;;
esac

echo "📁 目标目录：$SKILLS_DIR"
echo ""

# 创建目录
mkdir -p "$SKILLS_DIR"

# 备份现有配置
if [ -f "$SKILLS_DIR/skills.config.json" ]; then
    BACKUP_FILE="$SKILLS_DIR/skills.config.json.backup.$(date +%Y%m%d%H%M%S)"
    cp "$SKILLS_DIR/skills.config.json" "$BACKUP_FILE"
    echo "✓ 已备份现有配置：$BACKUP_FILE"
fi

# 复制 Skill
echo ""
echo "📦 正在复制 运动康复小南 Skill..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -d "$SCRIPT_DIR/运动康复小南" ]; then
    cp -R "$SCRIPT_DIR/运动康复小南" "$SKILLS_DIR/"
    echo "  → 运动康复小南"
else
    echo "❌ 未找到 Skill 目录"
    exit 1
fi

echo ""
echo "✅ 安装完成！"
echo ""
echo "⚠️  请重启 LobsterAI / OpenClaw 以加载新 Skills"
echo ""
echo "📚 查看使用说明：https://github.com/lyndyw/sports-rehab-xiaonan"
