#!/bin/bash
set -e

echo "=== 部署 GameCode 到 GitHub Pages ==="

cd "$(dirname "$0")/.."

if ! git diff --quiet; then
  echo "有未提交的更改，正在提交..."
  git add -A
  read -p "请输入提交信息: " msg
  git commit -m "$msg"
fi

echo "正在推送到 GitHub..."
git push origin main

echo "等待 Pages 部署..."
sleep 10

url="https://tsdking.github.io/GameCode/"
http_code=$(curl -s -o /dev/null -w "%{http_code}" "$url" || echo "000")

if [ "$http_code" = "200" ]; then
  echo "部署成功！"
  echo "访问地址: $url"
else
  echo "部署可能还在进行中，请稍后访问: $url"
fi
