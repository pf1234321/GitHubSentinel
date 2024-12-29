from typing import List, Dict
from datetime import datetime
import markdown
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from langchain_openai import ChatOpenAI
import json
_ = load_dotenv(find_dotenv())

llm = ChatOpenAI()
def summarize_progress(content):
    print(content)
    response= llm.invoke(content)
    print(f'response=={response}')
    print(f'response.content=={response.content}')

    return response.content


class ReportGenerator:
    def __init__(self):
        self.llm =llm
        # 创建报告保存目录
        self.report_dir = Path("reports")
        self.report_dir.mkdir(exist_ok=True)

    def generate_summary_report(self, sources: List[dict]) -> dict:
        """生成摘要报告"""
        prompt = self._create_summary_prompt(sources)
        return self._generate_report(prompt, "summary", sources)

    def generate_detailed_report(self, sources: List[dict]) -> dict:
        """生成详细报告"""
        prompt = self._create_detailed_prompt(sources)
        return self._generate_report(prompt, "detailed", sources)

    def generate_alert_report(self, sources: List[dict]) -> dict:
        """生成警报报告"""
        prompt = self._create_alert_prompt(sources)
        return self._generate_report(prompt, "alert", sources)

    def _create_summary_prompt(self, sources: List[dict]) -> str:
        """创建摘要报告提示"""
        source_info = self._format_source_info(sources)
        return f"""请基于以下GitHub信息生成一份简洁的摘要报告（markdown格式）：

{source_info}

请包含以下部分：
# GitHub 监控摘要报告

## 概述
[简要描述主要发现]

## 关键发现
[列出3-5个最重要的发现]

## 趋势分析
[分析主要趋势和模式]

## 建议
[提供2-3个具体建议]

要求：
- 使用清晰的markdown格式
- 保持简洁（300字左右）
- 重点突出关键信息
- 使用客观的语言
"""

    def _create_detailed_prompt(self, sources: List[dict]) -> str:
        """创建详细报告提示"""
        source_info = self._format_source_info(sources)
        return f"""请基于以下GitHub信息生成一份详细的分析报告（markdown格式）：

{source_info}

请包含以下部分：
# GitHub 详细分析报告

## 执行摘要
[总体情况概述]

## 详细发现
[具体分析每个重要发现]

## 技术分析
[深入的技术层面分析]

## 数据洞察
[基于数据的具体分析]

## 建议
[详细的改进建议]

## 附录
[相关数据和参考]

要求：
- 使用专业的markdown格式
- 详细展开（1000字左右）
- 包含具体的数据支持
- 提供深入的技术分析
"""

    def _create_alert_prompt(self, sources: List[dict]) -> str:
        """创建警报报告提示"""
        source_info = self._format_source_info(sources)
        return f"""请基于以下GitHub信息生成一份紧急警报报告（markdown格式）：

{source_info}

请包含以下部分：
# GitHub 安全警报报告

## 紧急警报
[最重要的安全问题]

## 风险评估
[每个问题的风险等级]

## 必要行动
[需要立即采取的措施]

## 时间线
[问题发现和处理的时间线]

## 联系方式
[相关负责人联系方式]

要求：
- 使用醒目的markdown格式
- 突出紧急程度
- 清晰列出行动步骤
- 标注优先级
"""

    def _format_source_info(self, sources: List[dict]) -> str:
        """格式化源信息"""
        formatted = []
        for source in sources:
            info = {
                "url": source.get("url"),
                "type": source.get("type"),
                "keywords": source.get("keywords", []),
                "last_updated": source.get("last_updated"),
                "data": source.get("data", {})
            }
            formatted.append(f"```json\n{json.dumps(info, indent=2)}\n```")
        return "\n\n".join(formatted)

    def _generate_report(self, prompt: str, report_type: str, sources: List[dict]) -> dict:
        """生成报告"""
        try:
            # 使用LLM生成报告内容
            content = summarize_progress(prompt)
            print(f'content=={content}')
            # 添加元数据
            metadata = self._generate_metadata(report_type, sources)
            print(f'metadata=={metadata}')
            # 组合最终报告
            final_content = self._combine_report(content, metadata)
            print(f'final_content=={final_content}')
            # 保存报告
            saved_paths = self._save_report(final_content, report_type)
            print(f'saved_paths=={saved_paths}')
            return {
                "content": final_content,
                "paths": saved_paths,
                "metadata": metadata,
                "status": "success"
            }
            
        except Exception as e:
            error_report = self._generate_error_report(e, report_type, sources)
            return {
                "content": error_report,
                "status": "error",
                "error": str(e)
            }

    def _generate_metadata(self, report_type: str, sources: List[dict]) -> dict:
        """生成报告元数据"""
        return {
            "generated_at": datetime.now().isoformat(),
            "report_type": report_type,
            "source_count": len(sources),
            "keywords": list(set(sum([s.get("keywords", []) for s in sources], []))),
            "urls": [s.get("url") for s in sources]
        }

    def _combine_report(self, content: str, metadata: dict) -> str:
        """组合报告内容和元数据"""
        metadata_section = f"""---
生成时间: {metadata['generated_at']}
报告类型: {metadata['report_type']}
数据源数量: {metadata['source_count']}
关键词: {', '.join(metadata['keywords'])}
---

"""
        return metadata_section + content

    def _save_report(self, content: str, report_type: str) -> Dict[str, str]:
        """保存报告文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"report_{report_type.lower()}_{timestamp}"
        
        # 保存 Markdown 文件
        md_path = self.report_dir / f"{base_name}.md"
        md_path.write_text(content, encoding="utf-8")
        
        # 保存 HTML 文件
        html_path = self.report_dir / f"{base_name}.html"
        html_content = self._markdown_to_html(content, report_type)
        html_path.write_text(html_content, encoding="utf-8")
        
        return {
            "markdown": str(md_path),
            "html": str(html_path)
        }

    def _markdown_to_html(self, content: str, report_type: str) -> str:
        """将 Markdown 转换为 HTML"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{report_type} Report</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css/github-markdown.min.css">
            <style>
                .markdown-body {{
                    box-sizing: border-box;
                    min-width: 200px;
                    max-width: 980px;
                    margin: 0 auto;
                    padding: 45px;
                }}
            </style>
        </head>
        <body class="markdown-body">
            {markdown.markdown(content, extensions=['tables', 'fenced_code'])}
        </body>
        </html>
        """

    def _generate_error_report(self, error: Exception, report_type: str, sources: List[dict]) -> str:
        """生成错误报告"""
        return f"""# Error Report

## Error Details
- Time: {datetime.now().isoformat()}
- Report Type: {report_type}
- Error Type: {type(error).__name__}
- Error Message: {str(error)}

## Context
- Number of Sources: {len(sources)}
- Source URLs: {[s.get('url') for s in sources]}
"""