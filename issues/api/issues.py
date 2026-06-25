from rest_framework.decorators import api_view
from rest_framework.response import Response

from issues.models import Issue, CriticalIssue, LowPriorityIssue
from utils.json_utils import load_json, save_json


@api_view(["GET", "POST"])
def issues(request):
    try:
        issues_data = load_json("issues.json")

        if request.method == "GET":
            return get_issues(request, issues_data)

        return create_new_issue(request, issues_data)

    except ValueError as e:
        return Response({"error": str(e)}, status=400)


def get_issues(request, issues_data):
    issue_id = request.query_params.get("id")
    status_filter = request.query_params.get("status")

    if issue_id:
        issue = next(
            (issue for issue in issues_data if str(issue["id"]) == issue_id),
            None,
        )

        if issue is None:
            return Response({"error": "Issue not found"}, status=404)

        return Response(issue)

    if status_filter:
        filtered = [
            issue
            for issue in issues_data
            if issue.get("status") == status_filter
        ]

        if not filtered:
            return Response({"error": "No issues found"}, status=404)

        return Response(filtered)

    return Response(issues_data)


def create_new_issue(request, issues_data):
    data = {
        "title": request.data.get("title"),
        "description": request.data.get("description"),
        "priority": request.data.get("priority"),
        "reporter_id": request.data.get("reporter_id"),
        "status": request.data.get("status"),
    }

    issue = create_issue(data)
    issue.validate()

    issue_dict = issue.to_dict()

    issues_data.append(issue_dict)
    save_json("issues.json", issues_data)

    return Response(issue_dict, status=201)


def create_issue(data):
    priority = data.get("priority")

    issue_class = {
        "critical": CriticalIssue,
        "low": LowPriorityIssue,
    }.get(priority, Issue)

    return issue_class(**data)