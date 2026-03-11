# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


def wikipedia_search(query: str):
    """Wikipedia Search Tool."""
    # return "Wikipedia search tool is not available"  # Mock Test
    try:
        wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        page = wikipedia.run(query)
        return page if page else "No Wikipedia page found for query."
    except Exception as e:
        return f"Error accessing Wikipedia: {str(e)}"


if __name__ == "__main__":
    result = wikipedia_search("superpixel segmentation macro")
    print(result)
