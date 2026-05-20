#!/bin/bash
mkdir -p ~/.streamlit/

echo "\
[theme]
primaryColor = '#48bb78'
backgroundColor = '#0e1117'
secondaryBackgroundColor = '#161b27'
textColor = '#e2e8f0'

[client]
toolbarMode = 'minimal'

[server]
headless = true
port = \$PORT
enableXsrfProtection = true
" > ~/.streamlit/config.toml
