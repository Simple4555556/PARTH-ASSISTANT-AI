"""
PARTH ASSISTANT AI — Fee Tools
Provides secure tool endpoints for student fees and school-wide fee analytics.
"""

from typing import Dict, Any, Optional
from mock_services.academic_service import academic_service


class FeeTools:
    def get_student_fees(self, student_id: str) -> Dict[str, Any]:
        fees = academic_service.get_student_fees(student_id)
        return {"success": True, "student_id": student_id, "data": fees}

    def get_school_fee_summary(self) -> Dict[str, Any]:
        data = academic_service.get_school_fee_summary()
        return {"success": True, "data": data}


fee_tools = FeeTools()
