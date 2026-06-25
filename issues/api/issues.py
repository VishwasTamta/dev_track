from rest_framework.decorators import api_view
from rest_framework.response import Response
from issues.models import Issue, CriticalIssue, LowPriorityIssue
import json
from pathlib import Path

@api_view(["POST", "GET"])
def issues(request):
    
    BASE_DIR = Path(__file__).resolve().parent.parent
    json_path = BASE_DIR / "issues.json"
    try:

        with open(json_path, "r") as f:
            issues = json.load(f)
        
        if request.method == "GET":
            return Response(issues, status=200)

        if request.method == "POST":

            data = {
                "title": request.data.get("title"),
                "description": request.data.get("description"),
                "priority": request.data.get("priority"),
                # TODO: fix logic for getting reporter id.
                "reporter_id": "temp id for now",
                "status": "open",
            }

            if data["priority"] == "critical":
                issue = CriticalIssue(**data)
            elif data["priority"] == "low":
                issue = LowPriorityIssue(**data)
            else:
                issue = Issue(**data)
            issue.validate()

            issues.append(issue.to_dict())
            with open(json_path, "w") as f:
                json.dump(issues, f, indent=4)

            return Response(issue.to_dict(), status=201)
    
    except ValueError as e:
        return Response({"error": str(e)}, status=400)
