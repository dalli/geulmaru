"""Unit tests for Feed Parser service."""
import pytest
from datetime import datetime

# Import the service to be tested
from src.services import feed_parser


class TestFeedParser:
    """Test cases for Feed Parser service."""
    
    def test_parse_rss_success(self):
        """Test successful RSS parsing."""
        rss_content = '''<?xml version="1.0"?>
        <rss version="2.0">
            <channel>
                <item>
                    <title>Test Article</title>
                    <link>https://example.com/article/1</link>
                    <pubDate>Mon, 21 Jan 2025 11:00:00 +0000</pubDate>
                    <author>author@example.com (John Doe)</author>
                </item>
            </channel>
        </rss>'''
        
        articles = feed_parser.parse_rss(rss_content)
        assert len(articles) == 1
        assert articles[0]['title'] == 'Test Article'
        assert articles[0]['url'] == 'https://example.com/article/1'
        assert articles[0]['published_at'] is not None
    
    def test_parse_rss_empty_feed(self):
        """Test parsing of empty RSS feed."""
        rss_content = '''<?xml version="1.0"?>
        <rss version="2.0">
            <channel>
            </channel>
        </rss>'''
        
        articles = feed_parser.parse_rss(rss_content)
        assert len(articles) == 0
    
    def test_parse_rss_invalid_xml(self):
        """Test handling of invalid XML."""
        rss_content = '<invalid xml>'
        
        articles = feed_parser.parse_rss(rss_content)
        assert len(articles) == 0
    
    def test_parse_rss_missing_url(self):
        """Test handling of items without URL."""
        rss_content = '''<?xml version="1.0"?>
        <rss version="2.0">
            <channel>
                <item>
                    <title>Test Article</title>
                    <pubDate>Mon, 21 Jan 2025 11:00:00 +0000</pubDate>
                </item>
            </channel>
        </rss>'''
        
        articles = feed_parser.parse_rss(rss_content)
        assert len(articles) == 0
    
    def test_parse_rss_multiple_articles(self):
        """Test parsing of multiple articles."""
        rss_content = '''<?xml version="1.0"?>
        <rss version="2.0">
            <channel>
                <item>
                    <title>Article 1</title>
                    <link>https://example.com/article/1</link>
                    <pubDate>Mon, 21 Jan 2025 11:00:00 +0000</pubDate>
                </item>
                <item>
                    <title>Article 2</title>
                    <link>https://example.com/article/2</link>
                    <pubDate>Mon, 21 Jan 2025 10:00:00 +0000</pubDate>
                </item>
            </channel>
        </rss>'''
        
        articles = feed_parser.parse_rss(rss_content)
        assert len(articles) == 2

