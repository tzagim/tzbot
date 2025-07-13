import re
from typing import List, Optional

def predicate_text(filters: Optional[List[str]], text: str) -> bool:
    """Check if the text contains any of the filters."""
    
    filters = filters or []
    
    for i in filters:
        pattern = r"( |^|[^\w])" + re.escape(i) + r"( |$|[^\w])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            return True

    return False
