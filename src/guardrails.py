import re
from typing import Tuple, List, Dict, Any

class GuardrailFilter:
    """
    Blue-Team input validation engine.
    Detects and blocks prompt injection payloads before LLM execution.
    """
    
    # Common jailbreak signatures and system prompt override attempts
    OVERRIDE_PATTERNS = [
        r"ignore\s+(all\s+|previous\s+|prior\s+)*instructions",
        r"disregard\s+(all\s+|previous\s+)*rules",
        r"system\s*:\s*override",
        r"you\s+are\s+now\s+in\s+developer\s+mode",
        r"dan\s+mode",
        r"do\s+anything\s+now",
        r"print\s+your\s+(system\s+)?prompt",
        r"reveal\s+your\s+(secret|instructions)",
        r"base64\s+decode",
    ]

    # High-risk security keywords that trigger suspicion when used together
    SUSPICIOUS_KEYWORDS = [
        "override", "system", "jailbreak", "bypass", "unrestricted",
        "sudo", "admin", "prompt", "hidden", "flag", "key"
    ]

    def __init__(self, sensitivity: str = "medium"):
        self.sensitivity = sensitivity
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.OVERRIDE_PATTERNS]

    def inspect_prompt(self, user_prompt: str) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Inspects player input.
        Returns: (is_blocked: bool, block_reason: str, audit_metadata: dict)
        """
        cleaned_prompt = user_prompt.strip().lower()

        # 1. Check for known jailbreak regex patterns
        for pattern in self.compiled_patterns:
            if pattern.search(cleaned_prompt):
                return True, "Jailbreak Pattern Detected", {
                    "matched_pattern": pattern.pattern,
                    "action": "BLOCKED"
                }

        # 2. Check keyword density (Multiple suspicious terms in one prompt)
        keyword_hits = [kw for kw in self.SUSPICIOUS_KEYWORDS if kw in cleaned_prompt]
        threshold = 2 if self.sensitivity == "high" else 3
        
        if len(keyword_hits) >= threshold:
            return True, "Suspicious Keyword Density Exceeded", {
                "hits": keyword_hits,
                "action": "BLOCKED"
            }

        # 3. Prompt passed inspect filters
        return False, "Prompt Allowed", {
            "action": "PASSED"
        }
