#!/bin/bash

# Convert HTML to PDF using wkhtmltopdf
# Install wkhtmltopdf first: sudo apt-get install wkhtmltopdf

echo "Converting HTML proposals to PDF..."

# Check if wkhtmltopdf is installed
if ! command -v wkhtmltopdf &> /dev/null; then
    echo "wkhtmltopdf is not installed. Installing..."
    echo "Please run: sudo apt-get install wkhtmltopdf"
    echo "Or visit: https://wkhtmltopdf.org/downloads.html"
    exit 1
fi

# Convert detailed proposal
echo "Creating detailed PDF proposal..."
wkhtmltopdf --page-size A4 \
    --margin-top 15mm --margin-bottom 15mm \
    --margin-left 15mm --margin-right 15mm \
    --header-center "Private AI System Proposal" \
    --footer-center "[page]/[topage]" \
    tax_ai_system_proposal.html \
    tax_ai_system_proposal_detailed.pdf

# Convert simple proposal  
echo "Creating simple PDF proposal..."
wkhtmltopdf --page-size A4 \
    --margin-top 15mm --margin-bottom 15mm \
    --margin-left 15mm --margin-right 15mm \
    --footer-center "[page]/[topage]" \
    tax_ai_system_proposal_simple.html \
    tax_ai_system_proposal_simple.pdf

echo "PDF files created successfully:"
echo "1. tax_ai_system_proposal_detailed.pdf (Detailed version)"
echo "2. tax_ai_system_proposal_simple.pdf (Simple version)"

echo ""
echo "Alternative method using Chrome/Chromium:"
echo "Open the HTML files in Chrome and use Print > Save as PDF"