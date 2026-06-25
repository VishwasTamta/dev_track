from rest_framework.decorators import api_view
from rest_framework.response import Response
from issues.models import Reporter
import json
from pathlib import Path

@api_view(["GET", "POST"])
def reporters(request):
    try:
        BASE_DIR = Path(__file__).resolve().parent.parent
        json_path = BASE_DIR / "reporters.json"
        with open(json_path, "r") as file:
            reporters = json.load(file)

        if request.method == "GET":
            reporter_id = request.query_params.get("id")

            if reporter_id is None:
                return Response(reporters, status=200)

            reporter = next(
                (r for r in reporters if str(r["id"]) == reporter_id),
                None
            )

            if reporter is None:
                return Response(
                    {"error": "Reporter not found"},
                    status=404
                )
            
            return Response(reporter, status=200)
        elif request.method == "POST":
            reporter = Reporter(
                email=request.data.get("email"),
                name=request.data.get("name"),
                team=request.data.get('team')
            )

            reporter.validate()

            with open(json_path, "w") as file:
                reporters.append(reporter.to_dict())
                json.dump(reporters, file, indent=4)

            return Response(reporter.to_dict(), status=201)
    
    except ValueError as e:
        return Response({"error": str(e)}, status=400)