@echo off
echo ===============================
echo 블로그 FAQ GitHub 자동 배포 시작
echo ===============================
cd /d %~dp0

git add .
git commit -m "🔄 자동 업데이트"
git push origin main

echo ===============================
echo ✅ 배포 완료! 웹사이트를 확인하세요
echo 🔗 https://doshutna.github.io/faq/
echo ===============================
pause
