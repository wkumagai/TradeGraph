"""Node for generating HTML version of the report."""

import os
from typing import Dict, Any
from datetime import datetime


def generate_html_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Generate an HTML version of the investment research report.
    
    This node creates a styled HTML report for web viewing.
    """
    final_report = state.get("final_report", "")
    investment_method = state.get("investment_method", {})
    performance_metrics = state.get("performance_metrics", {})
    
    # Convert markdown to HTML (simplified version)
    # In production, would use markdown2 or similar library
    html_content = final_report.replace('\n', '<br>\n')
    html_content = html_content.replace('# ', '<h1>')
    html_content = html_content.replace('\n\n', '</p><p>')
    html_content = html_content.replace('## ', '<h2>')
    html_content = html_content.replace('### ', '<h3>')
    html_content = html_content.replace('**', '<strong>')
    html_content = html_content.replace('*', '<em>')
    html_content = html_content.replace('---', '<hr>')
    
    # Create complete HTML document
    html_report = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Investment Research Report - {investment_method.get('method_name', 'Strategy')}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-bottom: 1px solid #ecf0f1;
            padding-bottom: 5px;
        }}
        h3 {{
            color: #7f8c8d;
            margin-top: 20px;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .metric-card {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #e9ecef;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        }}
        .metric-label {{
            font-size: 14px;
            color: #7f8c8d;
            margin-top: 5px;
        }}
        .positive {{
            color: #27ae60;
        }}
        .negative {{
            color: #e74c3c;
        }}
        .warning {{
            background-color: #fff3cd;
            border: 1px solid #ffebc4;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f8f9fa;
            font-weight: bold;
        }}
        .chart-placeholder {{
            background-color: #f8f9fa;
            border: 2px dashed #dee2e6;
            padding: 40px;
            text-align: center;
            border-radius: 8px;
            margin: 20px 0;
            color: #6c757d;
        }}
        .timestamp {{
            text-align: right;
            color: #7f8c8d;
            font-size: 14px;
            margin-top: 40px;
        }}
        @media print {{
            body {{
                background-color: white;
            }}
            .container {{
                box-shadow: none;
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Investment Strategy Research Report</h1>
        <h2>{investment_method.get('method_name', 'Unnamed Strategy')}</h2>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value {'' if not performance_metrics.get('total_return') else 'positive' if float(str(performance_metrics.get('total_return', '0')).rstrip('%')) > 0 else 'negative'}">
                    {performance_metrics.get('total_return', 'N/A')}
                </div>
                <div class="metric-label">Total Return</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">
                    {performance_metrics.get('sharpe_ratio', 'N/A')}
                </div>
                <div class="metric-label">Sharpe Ratio</div>
            </div>
            <div class="metric-card">
                <div class="metric-value negative">
                    {performance_metrics.get('max_drawdown', 'N/A')}
                </div>
                <div class="metric-label">Max Drawdown</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">
                    {performance_metrics.get('win_rate', 'N/A')}
                </div>
                <div class="metric-label">Win Rate</div>
            </div>
        </div>
        
        <div class="warning">
            <strong>⚠️ Important Disclaimer:</strong> This report is generated by an automated AI system for research purposes only. 
            It does not constitute investment advice. Past performance does not guarantee future results. 
            Always consult with qualified financial advisors before making investment decisions.
        </div>
        
        <div class="report-content">
            {html_content}
        </div>
        
        <div class="timestamp">
            Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
        </div>
    </div>
    
    <script>
        // Add smooth scrolling for internal links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});
    </script>
</body>
</html>"""
    
    # Save HTML report
    save_dir = state.get("save_dir", "./stock_research_output")
    html_file = os.path.join(save_dir, "report", "investment_research_report.html")
    
    with open(html_file, "w") as f:
        f.write(html_report)
    
    # Update state
    state["html_report"] = html_report
    
    print(f"HTML report generated: {html_file}")
    
    return state