"""
PARTH ASSISTANT AI — Parent Tools
Provides tools for parent profile lookups and linked children data.
"""

from typing import Dict, Any, List
from mock_services.student_service import student_service


class ParentTools:
    def get_parent_children(self, parent_id: str) -> Dict[str, Any]:
        children = student_service.get_parent_children(parent_id)
        return {"success": True, "parent_id": parent_id, "children": children}


parent_tools = ParentTools()
