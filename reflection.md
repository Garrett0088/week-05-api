## Week 5 Reflection

**1. What is the difference between the system prompt and the user message?
Why does the separation matter?**

The system prompt is set by the developer and defines the assistant's
personality, rules, and constraints before the conversation starts.
The user message is what the person types during the conversation.
The separation matters because it lets the developer control behavior
without the user being able to override it — for example, restricting
Claude to only discuss books regardless of what the user asks.

**2. What happened when you changed the system prompt in Part 4?
What surprised you most?**

When I switched to the opinionated/dramatic persona, the tone completely
changed — Claude started throwing in strong opinions and got way more
enthusiastic, almost pushy about certain books. With the structured prompt
that forced a rigid JSON-like format, every response felt robotic and the
conversation flow was gone. The constraint prompt was probably the most
interesting one: when I asked something totally off-topic, Claude politely
redirected me back to books instead of just refusing.

What surprised me most was how much the system prompt shapes the *personality*
not just the rules. I expected it to just filter what Claude could talk about,
but it actually changed how it communicated — word choice, energy, everything.
It made me realize the system prompt is basically writing a character, not just
setting guardrails.

**3. Name one situation where using AI in an app could cause harm,
and how you would mitigate it.**

A book app for kids could surface age-inappropriate content if Claude
recommends books without knowing the reader's age. The mitigation would
be adding an age group field to the user profile, then injecting it into
the system prompt — something like "The user is 10 years old. Only recommend
books appropriate for middle-grade readers." I'd also add a content-filter
layer on the backend that rejects any response containing flagged keywords
before it ever reaches the frontend.

**4. If you had infinite Claude API credits, what AI feature would you
add to this book tracker? Describe it technically.**

I'd add a "reading personality" profile that builds up over time. Every time
a user marks a book as "read" and rates it, a background job would call a new
POST /ai/profile/update endpoint. That endpoint would pull all rated books
from the DB, send them to Claude with a prompt asking it to identify patterns
(e.g. "prefers fast-paced sci-fi with unreliable narrators, avoids romance
subplots"), and store the result as a `reading_profile` text column on the
users table. The /ai/recommend endpoint would then inject that profile into
its system prompt alongside the book list — so recommendations get smarter
the more you use the app, not just based on raw titles but on actual taste
patterns Claude has inferred.
