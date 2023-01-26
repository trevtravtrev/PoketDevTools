import openai_secret_manager
from trello import TrelloClient


def authenticate():
    # Get Trello API key and token
    secrets = openai_secret_manager.get_secrets("trello")
    api_key = secrets["api_key"]
    token = secrets["token"]
    # Authenticate with Trello API
    client = TrelloClient(api_key=api_key, token=token)
    return client


def create_board(client):
    company_name = input("Enter the name of the client/company: ")
    board = client.add_board(f"PoketDev - {company_name}")
    return board


def create_lists(board):
    backlog = board.add_list("Requests")
    in_development = board.add_list("In Development")
    delivered = board.add_list("Delivered")
    customer_questions = board.add_list("Customer Questions")
    developer_clarification = board.add_list("Developer Clarifications")
    return (
        backlog,
        in_development,
        delivered,
        customer_questions,
        developer_clarification,
    )


def add_cards_to_lists(
    backlog, in_development, delivered, customer_questions, developer_clarification
):
    backlog.add_card(
        "How to use the Backlog List",
        "This is a card that describes how to use the Backlog List. This list would include all of the features and "
        "tasks that need to be developed. Each card in this list would include a brief description of the task, "
        "any relevant attachments or links, and the team members who will be working on it. Cards near the top of the "
        "list are the highest prioritized, while cards at the bottom of the list are the lowest priority.",
    )
    in_development.add_card(
        "**PoketDeveloper use only**",
        "This is a card that describes how to use the In Development List. Once a feature or task has been picked up "
        "by a developer, the card would be moved to the In Development list. This list would include all of the "
        "features and tasks that are currently being developed.",
    )
    delivered.add_card(
        "**PoketDeveloper use only**",
        "This is a card that describes how to use the Delivered List. Once a feature or task is completed and "
        "delivered, the card would be moved to the Delivered list. This list would include all of the features and "
        "tasks that have been delivered and are ready to be deployed.",
    )
    customer_questions.add_card(
        "How to use the Customer Questions List",
        "This is a card that describes how to use the Customer Questions List. This list would include all the "
        "questions or doubts that arise from the customer during the development process, and it would serve as a "
        "channel for the customer to communicate their requests or requirements. Team members should check this list "
        "frequently for new questions or updates.",
    )
    developer_clarification.add_card(
        "**PoketDeveloper use only**",
        "This is a card that describes how to use the Developer Clarification List. This list would include all the "
        "questions or doubts that arise during the development process and it would serve as a channel for "
        "clarifications and communication between the team members and the customer. Team members should use this "
        "list to document any questions or requests for clarification that they have, and to keep track of any "
        "updates or changes.",
    )


def main():
    client = authenticate()
    board = create_board(client)
    (
        backlog,
        in_development,
        delivered,
        customer_questions,
        developer_clarification,
    ) = create_lists(board)
    add_cards_to_lists(
        backlog, in_development, delivered, customer_questions, developer_clarification
    )


if __name__ == "__main__":
    main()
