# README for Langchain Speech-to-Text Summary Bot

## Overview
This project aims to build a Telegram bot that transcribes and summarizes voice messages using Langchain and OpenAI's Whisper API. The bot is designed to make it easier to consume long voice messages by providing a concise summary. For a comprehensive tutorial on how to build this bot, you can watch [this YouTube video](https://www.youtube.com/watch?v=2SMaVPl7nV8).

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Conclusion](#conclusion)

## Prerequisites
- Python 3.x
- OpenAI API key
- Telegram Bot Token
- User ID for Telegram

## Installation
1. Clone this repository to your local machine.
    ```bash
    https://github.com/Leon-Sander/langchain_telegram_audio_summarizer
    ```
2. Navigate to the project directory.
    ```bash
    cd langchain_telegram_audio_summarizer
    ```
3. Install the required packages.
    ```bash
    pip install -r requirements.txt
    ```

## Configuration
Add your OpenAI API key, Telegram Bot Token, and User ID into the `.env` file.


## Usage
1. Run the Telegram bot.
    ```bash
    python telegram_bot.py
    ```
2. The `AudioSummarizer` class will load `.ogg` audio files from the `/tmp/` directory.
3. Send a voice message to the bot on Telegram.
4. The bot will reply with the transcribed and summarized text.

## Conclusion
This Telegram bot serves as a convenient tool for transcribing and summarizing voice messages. It leverages the power of Langchain and OpenAI's Whisper API to provide accurate and concise summaries.
