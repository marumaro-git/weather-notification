#!/bin/bash

# .env.localファイルを作成
touch .env.local

echo "api_key=\"\"" >> .env.local
echo "lat=35.72967696209984" >> .env.local
echo "lon=139.71084645217894" >> .env.local
echo "slack_web_hook_url=\"\"" >> .env.local