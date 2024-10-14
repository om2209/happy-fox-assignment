from chalice import Chalice, Response

from apis.gmail import gmail_apis

app = Chalice(app_name='happy-fox-assignment')

app.experimental_feature_flags.update([
    'BLUEPRINTS'
])

app.register_blueprint(gmail_apis)


@app.route('/health', methods=['GET'], api_key_required=False)
def health():
    return Response(body={'messages': 'Up and Running'}, status_code=200,
                    headers={'Content-Type': 'application/json'})
