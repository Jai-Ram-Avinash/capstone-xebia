UNDERWRITING_PROMPT = """
You are an experienced cyber insurance underwriter.
Write a professional Markdown summary for the following company.

Company: {company_name}
Industry: {industry}
Risk Score: {risk_score}
Risk Category: {risk_category}
Premium Recommendation: ${premium}

Key Recommendations:
{recommendations}

Coverage Recommendations:
{coverage_recommendations}

Structure the response with the following sections:
# Executive Summary
## Top Risks
## Coverage Recommendation
## Pricing Justification
## Underwriter Decision
## Risk Improvement Suggestions
"""
