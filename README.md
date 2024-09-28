# ThoughtLink_LLM - Conversational Chatbot with Chain of Thought Reasoning

**ThoughtLink_LLM** is a conversational chatbot built with **Gemini API**. It incorporates **chain-of-thought reasoning**, allowing it to think step-by-step and provide more contextually intelligent responses.

## Table of Contents
- [Features](#features)
- [How It Works](#how-it-works)
- [License](#license)

## Features
- **Conversational AI**: Engages users in natural, human-like dialogue.
- **Chain of Thought Reasoning**: The chatbot uses logical steps to enhance response accuracy and provide a deeper context.
- **Gemini API Integration**: Built using the Gemini-flash API.
- **Scalable and Customizable**: Easily extend to add new features or improve performance.

## How it Works
- By default model loads in normal conversation mode.
- When toggled to chain of thoughts, the model generates 'thinking' and 'preliminary' sections.
- thinking : this section lets LLM think step-by-step to highlight steps involved in deriving answer.
- preliminary : this section lets LLM build over ideas generated during 'thinking' process.
- Then after model is called again asking it to generate final output for user.

## License
- This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
- Gemini API for providing the conversational model.

