"""
Default data initializations for the block
"""

# -*- coding: utf-8 -*-

TITLE = "Tagged text"

PROMPT = "For each of the highlighted words, select the category to which they belong."

SCORE = 1

CATEGORIES = [
    {
        "id": "en",
        "name": "English",
        "description": "Words in english"
    },
    {
        "id": "la",
        "name": "Latin",
        "color": "#3ea5ce",
        "description": "Words in latin"
    },
    {
        "id": "es",
        "name": "Spanish",
        "description": "Words in spanish"
    }
]

FRAGMENTS = [
    {
        "type": "text",
        "text": "Lorem ipsum dolor "
    },
    {
        "type": "keyword",
        "position": 0,
        "category": "la",
        "text": "sit",
        "score": 3
    },
    {
        "type": "text",
        "text": " amet, consectetur adipiscing elit. "
    },
    {
        "type": "keyword",
        "position": 1,
        "category": "en",
        "text": "In"
    },
    {
        "type": "text",
        "text": " hendrerit a lacus sed tempor. Nam ut neque in nisi "
    },
    {
        "type": "keyword",
        "position": 2,
        "category": "la",
        "text": "ultrices"
    },
    {
        "type": "text",
        "text": " porta sed et urna."
    }
]
