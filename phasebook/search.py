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

    def is_partial_match(query, field):
        return query.lower() in field.lower()

    def is_age_match(query, age):
        return age - 1 <= int(query) <= age + 1

    if "id" in args:
        user_id = args["id"]
        id_match = [user for user in USERS if user["id"] == user_id]
        matching_users.extend(id_match)

    for user in USERS:
        if "name" in args and is_partial_match(args["name"], user["name"]):
            matching_users.append(user)

        if "age" in args and is_age_match(args["age"], user["age"]):
            matching_users.append(user)

        if "occupation" in args and is_partial_match(
            args["occupation"], user["occupation"]
        ):
            matching_users.append(user)

        unique_users = {user["id"]: user for user in matching_users}.values()

        # sort result by id
        sorted_users = sorted(unique_users, key=lambda x: x["id"])

    if matching_users:
        return list(sorted_users)
    return USERS

    # First Implementation
    # issue: repetitive list comprehension

    # if "name" in args:
    #     user_name = args["name"].lower()
    #     name_match = [user for user in USERS if user_name in user["name"].lower()]
    #     matching_users.extend(name_match)

    # if "age" in args:
    #     user_age = int(args["age"])
    #     age_match = [
    #         user for user in USERS if (user_age - 1) <= user["age"] <= (user_age + 1)
    #     ]
    #     matching_users.extend(age_match)

    # if "occupation" in args:
    #     user_occupation = args["occupation"].lower()
    #     occupation_match = [
    #         user for user in USERS if user_occupation in user["occupation"].lower()
    #     ]
    #     matching_users.extend(occupation_match)

    # matching_users = list({user["id"]: user for user in matching_users}.values())

    # if matching_users:
    #     return matching_users
    # else:
    #     return USERS
