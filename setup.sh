#!/bin/bash

# Trinity AI Agent System - Setup Script
# سكريبت إعداد نظام الثالوث

set -e  # Exit on error

echo "🔧 إعداد نظام الثالوث للوكلاء الذكية"
echo "======================================"

# إنشاء البيئة الافتراضية
echo "📦 إنشاء البيئة الافتراضية..."
python3 -m venv venv
source venv/bin/activate

# ترقية pip
echo "⬆️ ترقية pip..."
pip install --upgrade pip

# تثبيت المكتبات
echo "📥 تثبيت المكتبات..."
pip install -r requirements.txt

# تثبيت متطلبات Playwright
echo "🌐 تثبيت متطلبات Playwright..."
playwright install chromium

# نسخ ملف البيئة
echo "⚙️ إعداد ملف البيئة..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "تم إنشاء ملف .env - يرجى إضافة مفاتيح API"
fi

# إنشاء المجلدات المطلوبة
echo "📁 إنشاء المجلدات..."
mkdir -p workspace/{memory,cache,artifacts,logs}
mkdir -p src/{core,agents,tools,api,utils}
mkdir -p tests

echo ""
echo "✅ تم إعداد النظام بنجاح!"
echo ""
echo "للتشغيل:"
echo "  source venv/bin/activate"
echo "  python -m src.main"
echo ""
echo "للوصول إلى واجهة API:"
echo "  http://localhost:8000/docs"
echo ""
