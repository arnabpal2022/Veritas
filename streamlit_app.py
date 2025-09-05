import streamlit as st
import os
import re
import glob
from datetime import datetime, timedelta
import markdown
from pathlib import Path

# Configure page settings
st.set_page_config(
    page_title="Veritas - AI News Daily",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Inter font and blog-style UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        color: white;
        border-radius: 0 0 20px 20px;
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        font-weight: 300;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    .news-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .news-card:hover {
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }
    
    .news-date {
        color: #64748b;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .news-title {
        font-size: 2rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 1rem;
        line-height: 1.3;
    }
    
    .news-content {
        font-size: 1rem;
        line-height: 1.7;
        color: #475569;
    }
    
    .news-content h3 {
        color: #1e293b;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        font-size: 1.4rem;
    }
    
    .news-content h4 {
        color: #334155;
        font-weight: 600;
        margin: 1.5rem 0 0.8rem 0;
        font-size: 1.2rem;
    }
    
    .news-content strong {
        color: #1e293b;
        font-weight: 600;
    }
    
    .news-content a {
        color: #667eea;
        text-decoration: none;
        font-weight: 500;
    }
    
    .news-content a:hover {
        color: #5a6acf;
        text-decoration: underline;
    }
    
    .sidebar .stSelectbox > div > div {
        background-color: #f8fafc;
    }
    
    .generate-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin: 1rem 0;
    }
    
    .generate-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .stats-container {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        flex: 1;
        border: 1px solid #e2e8f0;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin: 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #64748b;
        margin: 0.5rem 0 0 0;
        font-weight: 500;
    }
    
    .no-reports {
        text-align: center;
        padding: 3rem;
        color: #64748b;
    }
    
    .no-reports h3 {
        color: #475569;
        margin-bottom: 1rem;
    }
    
    .loading-container {
        text-align: center;
        padding: 2rem;
    }
    
    .stApp > header {
        background-color: transparent;
    }
    
    .stApp {
        background-color: #f8fafc;
    }
    
    .block-container {
        max-width: 1200px;
        padding: 2rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

def get_available_reports():
    """Get all available news reports"""
    reports = []
    report_files = glob.glob("ai_news_report_*.md")
    
    for file_path in report_files:
        # Extract date from filename
        match = re.search(r'ai_news_report_(\d{4}-\d{2}-\d{2})\.md', file_path)
        if match:
            date_str = match.group(1)
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                reports.append({
                    'file_path': file_path,
                    'date_str': date_str,
                    'date_obj': date_obj,
                    'formatted_date': date_obj.strftime('%B %d, %Y')
                })
            except ValueError:
                continue
    
    # Sort by date (newest first)
    reports.sort(key=lambda x: x['date_obj'], reverse=True)
    return reports

def parse_markdown_content(content):
    """Parse markdown content and extract structured information"""
    # Remove the markdown generation info
    content = re.sub(r'Generated on: \d{4}-\d{2}-\d{2}', '', content)
    
    # Convert markdown to HTML
    html_content = markdown.markdown(content)
    
    # Extract title
    title_match = re.search(r'\*\*(.*?Weekly Roundup.*?)\*\*', content)
    title = title_match.group(1) if title_match else "AI News Daily Report"
    
    return {
        'title': title.strip(),
        'content': content.strip(),
        'html_content': html_content
    }

def generate_new_report():
    """Generate a new report using the workflow"""
    try:
        from app.workflow import create_workflow
        
        # Create and run the workflow
        workflow = create_workflow()
        result = workflow.invoke({})
        
        if 'report' in result:
            # Save the report
            today = datetime.now().strftime('%Y-%m-%d')
            filename = f"ai_news_report_{today}.md"
            
            with open(filename, 'w') as f:
                f.write(result['report'])
            
            return True, filename
        else:
            return False, "Failed to generate report content"
    except Exception as e:
        return False, f"Error generating report: {str(e)}"

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📰 Veritas</h1>
        <p>Your Daily AI News Digest</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🛠️ Controls")
        
        # Generate new report button
        if st.button("🔄 Generate Today's Report", key="generate"):
            with st.spinner("Generating fresh news report..."):
                success, message = generate_new_report()
                if success:
                    st.success(f"✅ New report generated: {message}")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
        
        st.markdown("---")
        
        # Get available reports
        reports = get_available_reports()
        
        if reports:
            st.markdown("### 📅 Available Reports")
            
            # Date selector
            selected_date = st.selectbox(
                "Select a date:",
                options=[report['date_str'] for report in reports],
                format_func=lambda x: next(report['formatted_date'] for report in reports if report['date_str'] == x),
                key="date_selector"
            )
            
            st.markdown("---")
            
            # Stats
            st.markdown("### 📊 Statistics")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Reports", len(reports))
            with col2:
                if reports:
                    days_ago = (datetime.now().date() - reports[0]['date_obj'].date()).days
                    st.metric("Last Report", f"{days_ago} days ago" if days_ago > 0 else "Today")
        else:
            selected_date = None
            st.info("No reports available. Generate your first report!")
    
    # Main content area
    if reports and selected_date:
        # Find selected report
        selected_report = next(report for report in reports if report['date_str'] == selected_date)
        
        try:
            with open(selected_report['file_path'], 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse content
            parsed_content = parse_markdown_content(content)
            
            # Display the report
            st.markdown(f"""
            <div class="news-card">
                <div class="news-date">
                    📅 {selected_report['formatted_date']}
                </div>
                <div class="news-title">
                    {parsed_content['title']}
                </div>
                <div class="news-content">
            """, unsafe_allow_html=True)
            
            # Display markdown content
            st.markdown(f"<div class=\"news-content\">{parsed_content['content']}</div>", unsafe_allow_html=True)

            st.markdown("</div></div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error loading report: {str(e)}")
    
    elif not reports:
        # No reports available
        st.markdown("""
        <div class="news-card no-reports">
            <h3>🎯 Welcome to Veritas!</h3>
            <p>No news reports are available yet. Click the "Generate Today's Report" button in the sidebar to create your first AI news digest.</p>
            <br>
            <p><strong>What Veritas does:</strong></p>
            <ul style="text-align: left; display: inline-block;">
                <li>🔍 Searches for the latest AI news</li>
                <li>📝 Summarizes important articles</li>
                <li>📰 Creates a comprehensive daily digest</li>
                <li>🎨 Presents it in a beautiful blog format</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; color: #64748b; font-size: 0.9rem; padding: 1rem;">
            Developed by Arnab Pal 
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()