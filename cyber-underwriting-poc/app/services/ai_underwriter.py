from __future__ import annotations

import os
from typing import Any

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from app.prompts.underwriting_prompt import UNDERWRITING_PROMPT


class AIUnderwriter:
    def __init__(self, model_name: str | None = None, api_key: str | None = None) -> None:
        self.model_name = model_name or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.llm = None
        if self.api_key:
            self.llm = ChatOpenAI(model=self.model_name, api_key=self.api_key, temperature=0.2)

    def generate_summary(self, assessment: dict[str, Any], risk_result: dict[str, Any]) -> str:
        if self.llm is None:
            return (
                "# Executive Summary\n"
                "The assessment indicates elevated cyber risk and recommends immediate controls.\n\n"
                "## Top Risks\n"
                "- Missing MFA\n"
                "- Lack of backup strategy\n"
                "- Weak incident response readiness\n"
            )

        prompt = PromptTemplate.from_template(UNDERWRITING_PROMPT)
        chain = prompt | self.llm
        response = chain.invoke({
            "company_name": assessment.get("company_name", "Unknown"),
            "industry": assessment.get("industry", "Unknown"),
            "risk_score": risk_result["risk_score"],
            "risk_category": risk_result["risk_category"],
            "premium": risk_result["premium"],
            "recommendations": "\n".join(risk_result.get("recommendations", [])),
            "coverage_recommendations": "\n".join(risk_result.get("coverage_recommendations", [])),
        })
        return response.content
