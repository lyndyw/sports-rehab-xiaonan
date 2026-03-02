# 运动康复小南 - 安装脚本 (PowerShell)
# Windows 一键安装

Write-Host "💪 运动康复小南 - 安装程序" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
Write-Host ""

# 获取目标目录
$SkillsDir = Join-Path $env:APPDATA "LobsterAI\SKILLs"

Write-Host "📁 目标目录：$SkillsDir" -ForegroundColor Gray
Write-Host ""

# 创建目录
New-Item -ItemType Directory -Force -Path $SkillsDir | Out-Null

# 备份现有配置
$ConfigFile = Join-Path $SkillsDir "skills.config.json"
if (Test-Path $ConfigFile) {
    $BackupFile = "$ConfigFile.backup.$(Get-Date -Format 'yyyyMMddHHmmss')"
    Copy-Item $ConfigFile $BackupFile
    Write-Host "✓ 已备份现有配置：$BackupFile" -ForegroundColor Green
}

# 复制 Skills
Write-Host ""
Write-Host "📦 正在复制 运动康复小南 Skill..." -ForegroundColor Yellow

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

if (Test-Path "$ScriptDir\运动康复小南") {
    Copy-Item -Recurse -Force "$ScriptDir\运动康复小南" $SkillsDir
    Write-Host "  → 运动康复小南" -ForegroundColor Gray
} else {
    Write-Host "❌ 未找到 Skill 目录" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ 安装完成！" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  请重启 LobsterAI / OpenClaw 以加载新 Skills" -ForegroundColor Yellow
Write-Host ""
Write-Host "📚 查看使用说明：https://github.com/lyndyw/sports-rehab-xiaonan" -ForegroundColor Gray
Write-Host ""
