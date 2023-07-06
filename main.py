from google.cloud import dialogflowcx_v3beta1 as dialogflow
from google.api_core.client_options import ClientOptions
from google.oauth2 import service_account
import uuid


def detect_intent_text(project_id, location, agent_id, session_id, text, language_code):
    session_path = f"projects/{project_id}/locations/{location}/agents/{agent_id}/sessions/{session_id}"

    client_options = ClientOptions(api_endpoint='us-central1-dialogflow.googleapis.com')
    credentials = service_account.Credentials.from_service_account_file(
        '/Users/jhinpan/botbuildingbasics-a91819490394.json')
    client = dialogflow.SessionsClient(client_options=client_options, credentials=credentials)

    text_input = dialogflow.TextInput(text=text)
    query_input = dialogflow.QueryInput(text=text_input, language_code=language_code)

    request = dialogflow.DetectIntentRequest(
        session=session_path,
        query_input=query_input,
    )

    response = client.detect_intent(request=request)

    print("=" * 20)
    print(f"Query text: {response.query_result.text}")
    print(f"Response text: {response.query_result.response_messages[0].text.text[0]}")


if __name__ == "__main__":
    project_id = "botbuildingbasics"
    location = "us-central1"
    agent_id = "5e0a2be0-d845-4751-be87-4b17f05d1208"
    session_id = str(uuid.uuid4())
    language_code = "en"

    while True:
        text = input("You: ")
        detect_intent_text(project_id, location, agent_id, session_id, text, language_code)
