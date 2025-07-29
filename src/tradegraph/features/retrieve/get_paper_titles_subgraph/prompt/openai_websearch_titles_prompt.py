openai_websearch_titles_prompt = """\
You are a research assistant.
Task: Find recent academic papers related to: {{ query }}
{% if conference_preference -%}
Focus on papers from these conferences/venues: {{ conference_preference }}
{%- endif %}
Return **exactly {{ max_results }}** paper titles in JSON format.

Required output — **only** this JSON, nothing else:
{
  "titles": [
    "Paper title 1",
    "Paper title 2",
    "Paper title 3"
  ]
}
"""
