from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Substitua pelos valores reais da sua integração
WHATSAPP_API_URL = "https://graph.facebook.com/v20.0/411390388720168/messages"
ACCESS_TOKEN = "EAAHbTqSwBDEBO2er1FgmJzY7rwYxp5tkpJyTZBMIjpADsS10HYTPhFADEhuE5sxYpYUH1qKLnUxcKwR98cIfgN8hjM6sopZCMII7B75rA6W3tnXECGiYZCWdicKr9ICAuBjZA98IHBMJzqGq5YI8LZA2Bk4btietZCYvPxSDrRUb3iw8F7HMjtt0tz9SHguV8ZB6wLCcnTe0w62B4it7Eq1Ui2EfullO7yZBzZCcNqNQZD"

VERIFY_TOKEN = "testeia12345"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    try:
        if request.method == 'GET':
            token = request.args.get("hub.verify_token")
            challenge = request.args.get("hub.challenge")
            if token == VERIFY_TOKEN:
                return str(challenge), 200
            return "Token inválido", 403

        elif request.method == 'POST':
            data = request.json
            #print(data)

            # Verifica se a requisição tem o campo 'messages'
            if data and 'messages' in data:
                for message in data['messages']:
                    print(message)
                    if message.get('type') == 'text':
                        sender = message['from']
                        print(sender)
                        # Neste exemplo, o nome do template é "hello_world"
                        send_template_message(sender)

                return jsonify({"status": "success"}), 200

            return jsonify({"status": "no messages found"}), 200

    except Exception as e:
        # Loga o erro e retorna uma resposta 500
        print(f"Erro: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

def send_template_message(to):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": "en_US"
            }
        }
    }

    response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        print("Template enviado com sucesso!")
    else:
        print(f"Falha ao enviar template: {response.status_code}, {response.text}")

if __name__ == '__main__':
    app.run(port=5000)