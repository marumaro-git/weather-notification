#!/bin/bash

# .env.localファイルを作成
touch .env.local

echo "api_key=\"\"" >> .env.local
echo "lat=35.6811081" >> .env.local
echo "lon=139.764516" >> .env.local
echo "slack_web_hook_url=\"\"" >> .env.local