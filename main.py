import random
import uuid
from google.cloud import dialogflowcx_v3beta1 as dialogflow
from google.api_core.client_options import ClientOptions
from google.oauth2 import service_account


def detect_intent_text(project_id, location, agent_id, session_id, texts, language_code):
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

    # Generate furniture if user has not specified all parameters
    if 'confirm' in response.query_result.current_page.display_name.lower():

        furniture = generate_furniture({
            'color': response.query_result.parameters['furniture_color'],
            'type': response.query_result.parameters['furniture_type'],
            'material': response.query_result.parameters['furniture_material'],
            'placement': response.query_result.parameters['furniture_placement'],
        })

        print(
            f"Generated {furniture['type']} in {furniture['color']} color, made of {furniture['material']} for the {furniture['location']}")

    else:
        print("=" * 20)
        print(f"Query text: {response.query_result.text}")
        print(f"Response text: {response.query_result.response_messages[0].text.text[0]}")


def generate_furniture(attributes):
    possible_colors = ["white", "black", "red", "green", "blue"]
    possible_types = ["chair", "table", "sofa", "bed", "cupboard"]
    possible_materials = ["wood", "steel", "plastic", "metal"]
    possible_placements = ["near the entrance", "at the corner", "in the middle of the room", "opposite the door"]

    if attributes.get("color") == "null":
        attributes["color"] = random.choice(possible_colors)

    if attributes.get("type") == "null":
        attributes["type"] = random.choice(possible_types)

    if attributes.get("material") == "null":
        attributes["material"] = random.choice(possible_materials)

    if attributes.get("placement") == "null":
        attributes["location"] = random.choice(possible_placements)

    return attributes


if __name__ == "__main__":
    project_id = "botbuildingbasics"
    location = "us-central1"
    agent_id = "5e0a2be0-d845-4751-be87-4b17f05d1208"
    session_id = str(uuid.uuid4())
    language_code = "en"

    while True:
        text = input("You: ")
        detect_intent_text(project_id, location, agent_id, session_id, text, language_code)
