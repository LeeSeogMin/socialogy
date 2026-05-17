#!/usr/bin/env python3
"""
W12.ipynb를 Notion 페이지에 업로드하는 스크립트
"""
import json
import os
import subprocess
import sys

# Notion API 설정
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
if not NOTION_TOKEN:
    sys.exit("NOTION_TOKEN 환경변수를 설정해야 합니다.")

PAGE_ID = "3587e328316b801ca9a9d3a6a34fd319"

# 노트북 파일 읽기
with open('notebooks/W12.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Notion 블록으로 변환
blocks = []

for cell in notebook['cells']:
    cell_type = cell['cell_type']
    source = ''.join(cell['source'])
    
    if not source.strip():
        continue
    
    if cell_type == 'markdown':
        # 마크다운 셀 -> 여러 블록으로 분할
        lines = source.split('\n')
        current_para = []
        
        for line in lines:
            if line.startswith('# '):
                # 기존 paragraph 추가
                if current_para:
                    para_text = '\n'.join(current_para)
                    blocks.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": para_text}}]
                        }
                    })
                    current_para = []
                # Heading 1 추가
                blocks.append({
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                    }
                })
            elif line.startswith('## '):
                if current_para:
                    para_text = '\n'.join(current_para)
                    blocks.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": para_text}}]
                        }
                    })
                    current_para = []
                blocks.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": line[3:]}}]
                    }
                })
            elif line.startswith('### '):
                if current_para:
                    para_text = '\n'.join(current_para)
                    blocks.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": para_text}}]
                        }
                    })
                    current_para = []
                blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": line[4:]}}]
                    }
                })
            else:
                current_para.append(line)
        
        # 남은 paragraph 추가
        if current_para:
            para_text = '\n'.join(current_para)
            if para_text.strip():
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": para_text[:2000]}}]
                    }
                })
    
    elif cell_type == 'code':
        # 코드 셀 -> code 블록
        # Notion의 rich_text는 2000자 제한이 있음
        if len(source) > 2000:
            # 긴 코드는 여러 블록으로 분할
            chunks = [source[i:i+1900] for i in range(0, len(source), 1900)]
            for chunk in chunks:
                blocks.append({
                    "object": "block",
                    "type": "code",
                    "code": {
                        "rich_text": [{"type": "text", "text": {"content": chunk}}],
                        "language": "python"
                    }
                })
        else:
            blocks.append({
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": [{"type": "text", "text": {"content": source}}],
                    "language": "python"
                }
            })

# Notion API 요청 (블록 단위로 나누어 전송 - 한번에 100개 제한)
batch_size = 50
for i in range(0, len(blocks), batch_size):
    batch = blocks[i:i+batch_size]
    
    payload = {
        "children": batch
    }
    
    # curl 명령 생성
    cmd = [
        'curl', '-X', 'PATCH',
        f'https://api.notion.com/v1/blocks/{PAGE_ID}/children',
        '-H', 'Authorization: Bearer ' + NOTION_TOKEN,
        '-H', 'Notion-Version: 2022-06-28',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps(payload)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error in batch {i//batch_size + 1}: {result.stderr}", file=sys.stderr)
    else:
        response = json.loads(result.stdout)
        if 'object' in response and response['object'] == 'error':
            print(f"API Error in batch {i//batch_size + 1}: {response['message']}", file=sys.stderr)
        else:
            print(f"Batch {i//batch_size + 1} uploaded successfully ({len(batch)} blocks)")

print(f"\nTotal {len(blocks)} blocks uploaded to Notion page {PAGE_ID}")
