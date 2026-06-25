from rest_framework.decorators import api_view
from rest_framework.response import Response
from issues.models import Issue, CriticalIssue, LowPriorityIssue


@api_view(["POST"])
def create_issue(request):

    data = {
        "title": request.data.get("title"),
        "description": request.data.get("description"),
        "priority": request.data.get("priority"),
        # TODO: fix logic for getting reporter id.
        "reporter_id": "temp id for now",
        "status": "open",
    }

    try:
        if data["priority"] == "critical":
            issue = CriticalIssue(**data)
        elif data["priority"] == "low":
            issue = LowPriorityIssue(**data)
        else:
            issue = Issue(**data)

        issue.validate()

        return Response(issue.to_dict(), status=201)
    
    except ValueError as e:
        return Response({"error": str(e)}, status=400)
