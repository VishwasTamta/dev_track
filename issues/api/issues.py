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

            query_issue_id = request.query_params.get("id")
            if query_issue_id is None:
                query_issue_status = request.query_params.get("status")
                if query_issue_status is None:
                    return Response(issues, status=200)
                
                filtered_issues = [
                    issue
                    for issue in issues
                    if issue["status"] == query_issue_status
                ]

                if not filtered_issues:
                    return Response(
                        {"error": "No Issues found"},
                        status=404
                    )

                return Response(filtered_issues, status=200)
                    
            
            issue = next(
                (i for i in issues if str(i["id"]) == query_issue_id),
                None
            )

            if not issue:
                return Response(
                    {"error": "Issue not found"},
                    status=404
                ) 

            return Response(issue, status=200)


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
