#!/usr/bin/env python3
"""
sync_docs.py - Documentation compiler and asset sync script for Repin 2.0.

This script scans docs/ and docs/tutorials/ for Markdown files,
extracts H1 headers as page titles, compiles them into a structured JS format
matching the flat object expected by web/docs.html, and copies assets from
docs/assets/ to the web directory structure.
"""

import os
import shutil
import json
import re

def get_markdown_title(content, fallback_title):
    # Regex to find the first H1 header
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        # Strip any formatting like emojis or markdown markup
        title_text = match.group(1).strip()
        # Clean title text: e.g. "🧠 Архитектура Repin 2.0" or "🎨 Repin 2.0: ..."
        return title_text
    return fallback_title

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.join(base_dir, "docs")
    web_dir = os.path.join(base_dir, "web")
    output_file = os.path.join(web_dir, "docs_data.js")
    
    print(f"Workspace Directory: {base_dir}")
    print(f"Docs Directory: {docs_dir}")
    print(f"Web Directory: {web_dir}")
    
    if not os.path.exists(docs_dir):
        print(f"Error: docs directory not found at {docs_dir}")
        return
        
    docs_data = {}
    
    # 1. Compile Markdown files
    for root, dirs, files in os.walk(docs_dir):
        # Skip the assets folder inside docs from being parsed as markdown pages
        if "assets" in os.path.split(root):
            continue
            
        for file in files:
            if not file.lower().endswith(".md"):
                continue
                
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, docs_dir).replace("\\", "/")
            key = os.path.splitext(rel_path)[0].lower()
            
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading {full_path}: {e}")
                continue
                
            # Determine clean title
            # Default fallbacks
            fallback_titles = {
                "index": "Документация",
                "architecture": "Архитектура системы",
                "usage": "Руководство по использованию",
                "api_reference": "Справочник API",
                "troubleshooting": "Решение проблем",
                "tutorials/getting_started": "Быстрый старт: Создаем первый арт",
                "tutorials/training": "Обучение новой модели",
                "tutorials/hyperparameters": "Руководство по гиперпараметрам",
                "tutorials/generation_guide": "Руководство по продвинутой генерации",
                "tutorials/mode_collapse": "Mode Collapse",
                "changelog": "История изменений",
                "contributing": "Руководство контрибьютора",
                "faq": "FAQ",
                "best_practices": "Лучшие практики",
                "integration": "Интеграция"
            }
            fallback = fallback_titles.get(key, file)
            title = get_markdown_title(content, fallback)
            
            # Determine group and group order
            if rel_path.lower() == "index.md":
                group = "Введение"
                order = 0
            elif rel_path.startswith("tutorials/"):
                group = "Туториалы"
                order = 2
            elif file in ["architecture.md", "usage.md", "api_reference.md", "troubleshooting.md"]:
                group = "Документация"
                order = 1
            else:
                group = "Разработка"
                order = 3
                
            docs_data[key] = {
                "key": key,
                "title": title,
                "path": rel_path,
                "group": group,
                "groupOrder": order,
                "content": content
            }
            print(f"Compiled: {rel_path} -> key: {key}, group: {group}")
            
    # Output to docs_data.js
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    js_content = f"window.docsData = {json.dumps(docs_data, ensure_ascii=False, indent=2)};\n"
    
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(js_content)
        print(f"Generated docs data JS at {output_file}")
    except Exception as e:
        print(f"Error writing output JS file: {e}")
        return
        
    # 2. Copy asset files
    src_assets = os.path.join(docs_dir, "assets")
    dst_assets_1 = os.path.join(web_dir, "assets")
    dst_assets_2 = os.path.join(web_dir, "docs", "assets")
    
    if os.path.exists(src_assets):
        print(f"Syncing assets from {src_assets}...")
        for root, dirs, files in os.walk(src_assets):
            for file in files:
                src_file_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_file_path, src_assets)
                
                # Target 1: web/assets/
                target_path_1 = os.path.join(dst_assets_1, rel_path)
                try:
                    os.makedirs(os.path.dirname(target_path_1), exist_ok=True)
                    shutil.copy2(src_file_path, target_path_1)
                    print(f"  Copied {rel_path} to {target_path_1}")
                except Exception as e:
                    print(f"  Error copying to {target_path_1}: {e}")
                
                # Target 2: web/docs/assets/
                target_path_2 = os.path.join(dst_assets_2, rel_path)
                try:
                    os.makedirs(os.path.dirname(target_path_2), exist_ok=True)
                    shutil.copy2(src_file_path, target_path_2)
                    print(f"  Copied {rel_path} to {target_path_2}")
                except Exception as e:
                    print(f"  Error copying to {target_path_2}: {e}")
    else:
        print(f"No assets directory found at {src_assets}")
        
    print("Documentation sync completed successfully.")

if __name__ == "__main__":
    main()
