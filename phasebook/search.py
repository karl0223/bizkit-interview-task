from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """

    # Implement search here!

    matching_users = []
    users_with_weights = []
    field_weights = {"id": 4, "name": 3, "age": 2, "occupation": 1}

    def is_partial_match(query, field):
        return query.lower() in field.lower()

    def is_age_match(query, age):
        return age - 1 <= int(query) <= age + 1

    if "id" in args:
        user_id = args["id"]
        id_match = [user for user in USERS if user["id"] == user_id]
        matching_users.extend(id_match)
        users_with_weights.append((id_match, field_weights["id"]))

    for field in field_weights:
        if field != "id" and field in args:
            query = args[field]
            for user in USERS:
                weight = 0
                if field == "name" and is_partial_match(query, user["name"]):
                    weight = field_weights[field]
                elif field == "age" and is_age_match(query, user["age"]):
                    weight = field_weights[field]
                elif field == "occupation" and is_partial_match(
                    query, user["occupation"]
                ):
                    weight = field_weights[field]

                if weight > 0 and user["id"] not in [
                    user["id"] for user in matching_users
                ]:
                    matching_users.append(user)
                    users_with_weights.append((user, weight))

    # Sort users based on total weight (highest to lowest)
    sorted_users = [
        user
        for user, weight in sorted(users_with_weights, key=lambda x: x[1], reverse=True)
    ]

    if sorted_users:
        return sorted_users
    return USERS
