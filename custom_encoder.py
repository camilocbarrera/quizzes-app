import json
from decimal import Decimal


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder(self, obj)


{
    "name": "alejandro fonnegra aguilera",
    "group": 3,
    "quiz_score_aws": 2,
    "quiz_score_lambda": 1,
    "quiz_score_dynamo": 2,
    "quiz_score_apiGateway": 2

}
