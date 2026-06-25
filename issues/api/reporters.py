from rest_framework.decorators import api_view
from rest_framework.response import Response

from issues.models import Reporter
from utils.json_utils import load_json, save_json


@api_view(["GET", "POST"])
def reporters(request):
    try:
        reporters = load_json("reporters.json")

        if request.method == "GET":
            return get_reporters(request, reporters)

        return create_reporter(request, reporters)

    except ValueError as e:
        return Response({"error": str(e)}, status=400)
    
def get_reporters(request, reporters):
    reporter_id = request.query_params.get("id")

    if reporter_id is None:
        return Response(reporters)

    reporter = next(
        (r for r in reporters if str(r["id"]) == reporter_id),
        None
    )

    if reporter is None:
        return Response(
            {"error": "Reporter not found"},
            status=404
        )

    return Response(reporter)

def create_reporter(request, reporters):
    reporter = Reporter(
        email=request.data.get("email"),
        name=request.data.get("name"),
        team=request.data.get("team")
    )

    reporter.validate()

    reporters.append(reporter.to_dict())
    save_json("reporters.json", reporters)

    return Response(reporter.to_dict(), status=201)