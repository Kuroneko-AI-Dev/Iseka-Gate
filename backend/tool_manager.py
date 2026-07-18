from tools.research import research


def run_tool(tool, user_id, message):

    if tool["tool"] == "research":

        return research(
            query=message,
            user_id=user_id
        )

    return None