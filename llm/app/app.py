import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from llm_engine import llm_response
from dash.exceptions import PreventUpdate

# Custom CSS styles
CUSTOM_CSS = {
    "chatDisplay": {
        "width": "100%", 
        "height": "400px", 
        "overflowY": "scroll", 
        "backgroundColor": "#f8f9fa", 
        "padding": "10px", 
        "borderRadius": "8px", 
        "border": "1px solid #dee2e6", 
        "marginBottom": "20px"
    },
    "inputArea": {
        "width": "100%", 
        "borderRadius": "20px"
    },
    "sendButton": {
        "width": "100%", 
        "borderRadius": "20px", 
        "backgroundColor": "#007bff", 
        "borderColor": "#007bff"
    }
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("LLM Chatbot", className="text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Textarea(id='user-input', placeholder='Type your message here...', style=CUSTOM_CSS["inputArea"]), width=9),
        dbc.Col(dbc.Button('Send', id='send-button', n_clicks=0, style=CUSTOM_CSS["sendButton"]), width=3)
    ], className="mb-3"),
    dbc.Row([
        dbc.Col(html.Div(id='chat-history', style=CUSTOM_CSS["chatDisplay"]), width=12)
    ])
], fluid=True)

@app.callback(
    Output('chat-history', 'children'),
    Input('send-button', 'n_clicks'),
    State('user-input', 'value'),
    State('chat-history', 'children')
)
def update_chat(n_clicks, user_message, chat_history):
    if n_clicks > 0: #and user_message is not None:
        if not user_message:
            raise PreventUpdate
        # bot_response = f"Bot: This is a simulated response to '{user_message}'"

        chat_history = [] if chat_history is None else chat_history
        bot_response =  llm_response(user_message,chat_history) if n_clicks < 10 else "LLM reached quota limit"
        bot_response = f"Bot: {bot_response} "

        new_chat_history = chat_history + [
        html.Div([html.P(f"You: {user_message}"), html.P(f"{bot_response}")])
        ]
        return new_chat_history
    return chat_history


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8080, use_reloader=False)


