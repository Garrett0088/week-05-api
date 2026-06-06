# test_claude.py — quick sanity check before adding Claude to the app
# This script tests that your API key is valid and the SDK is installed correctly

import anthropic  # the SDK we just installed

# Creates a client — automatically reads ANTHROPIC_API_KEY from your .env
# (python-dotenv is NOT used here, so we need to load it manually)
from dotenv import load_dotenv
load_dotenv()  # reads .env and puts ANTHROPIC_API_KEY into the environment

client = anthropic.Anthropic()  # now the client can find the key

# Send a single test message to Claude
message = client.messages.create(
    model="claude-haiku-4-5-20251001",  # the model the lab specifies "claude-sonnet-4-6"
    max_tokens=256,                     # limit the response length for this test
    messages=[
        {"role": "user", "content": "What is the book '1984' about in one paragraph?"}
    ]
)

# Print just the text of the response
print(message.content[0].text)