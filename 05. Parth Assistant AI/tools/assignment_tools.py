"""
PARTH ASSISTANT AI — Assignment Tools
Provides homework and project assignment lookup tools.
"""

from typing import Dict, Any
from mock_services.academic_service import academic_service


class AssignmentTools:
    def get_class_assignments(self, class_id: str) -> Dict[str, Any]:
        asns = academic_service.get_class_assignments(class_id)
        return {"success": True, "class_id": class_id, "assignments": asns}


assignment_tools = AssignmentTools()
