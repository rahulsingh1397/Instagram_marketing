from .search import SearchTools

search_internet_tool = SearchTools.search_internet
search_instagram_tool = SearchTools.search_instagram
open_page_tool = SearchTools.open_page

# Optionally, you can also use pre-built tools from crewai_tools
# from crewai_tools import SerperDevTool
# serper_dev_tool = SerperDevTool() # Requires SERPER_API_KEY environment variable

# Example of how you might export them if needed in a list for some configurations:
# all_tools = [search_internet_tool, search_instagram_tool, open_page_tool]