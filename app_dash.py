import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import plotly.express as px
from emissions_counter.core import calculate_impact
from counter_component import create_counter_display, counter_css
import re

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Emissions Calculator for LLMs", style={
        'textAlign': 'center', 
        'marginBottom': '20px',
        'fontFamily': 'monospace',
        'color': '#2c3e50',
        'textShadow': '2px 2px 4px rgba(0,0,0,0.3)'
    }),

    # Compact input section
    html.Div([
        html.Div([
            html.Label("Input:", style={
                'fontFamily': 'monospace',
                'fontSize': '12px',
                'color': '#34495e',
                'marginBottom': '5px',
                'position': 'absolute',
                'top': '0',
                'left': '0'
            }),
            dcc.Textarea(
                id='prompt-input',
                placeholder='Type/paste your prompt here...',
                style={
                    'width': '100%',
                    'height': '80px',
                    'fontFamily': 'monospace',
                    'fontSize': '11px',
                    'border': '2px solid #34495e',
                    'borderRadius': '4px',
                    'backgroundColor': '#ecf0f1',
                    'resize': 'none',
                    'marginTop': '20px'
                }
            ),
            # Real-time character counter (deactivated)
            # html.Div(id='char-counter', style={
            #     'fontFamily': 'monospace',
            #     'fontSize': '10px',
            #     'color': '#7f8c8d',
            #     'textAlign': 'right',
            #     'marginTop': '5px'
            # })
        ], style={'marginBottom': '15px', 'position': 'relative'}),
        
        html.Div([
            html.Label("Expected Response Length:", style={
                'fontFamily': 'monospace',
                'fontSize': '12px',
                'color': '#34495e',
                'marginBottom': '5px'
            }),
            dcc.Slider(
                id='response-length-slider',
                min=10,
                max=2000,
                step=10,
                value=1000,
                marks={10: '10', 1000: '1000', 2000: '2000'},
                tooltip={"placement": "bottom", "always_visible": True},
                className='pixel-slider'
            )
        ], style={'marginBottom': '15px'}),
        
        html.Div([
            html.Label("Model:", style={
                'fontFamily': 'monospace',
                'fontSize': '12px',
                'color': '#34495e',
                'marginBottom': '5px'
            }),
            dcc.RadioItems(
                id='model-selector',
                options=[
                    {'label': 'o3', 'value': 'o3'},
                    {'label': 'GPT-4o', 'value': 'GPT-4o'},
                    {'label': 'Claude-3.7', 'value': 'Claude-3.7 Sonnet'},
                    {'label': 'DeepSeek-R1', 'value': 'DeepSeek-R1'}
                ],
                value='o3',
                style={'marginBottom': '5px', 'display': 'flex', 'gap': '20px'},
                className='pixel-radio',
                inline=True
            )
        ], style={'marginBottom': '10px'})
    ], style={
        'maxWidth': '400px',
        'margin': '0 auto 30px auto',
        'padding': '15px',
        'backgroundColor': '#f8f9fa',
        'border': '3px solid #34495e',
        'borderRadius': '8px'
    }),

    # Mechanical Counter-style metrics
    html.Div([
        html.Div([
            # Tokens Counter
            html.Div(id='tokens-counter', style={'display': 'inline-block'}),
            
            # Words Counter
            html.Div(id='words-counter', style={'display': 'inline-block'}),
            
            # Energy Counter
            html.Div(id='energy-counter', style={'display': 'inline-block'}),
            
            # Water Counter
            html.Div(id='water-counter', style={'display': 'inline-block'}),
            
            # CO2 Counter
            html.Div(id='co2-counter', style={'display': 'inline-block'})
        ], style={
            'display': 'flex',
            'flexDirection': 'row',
            'justifyContent': 'center',
            'alignItems': 'center',
            'maxWidth': '1000px',
            'margin': '0 auto',
            'gap': '10px',
            'flexWrap': 'wrap'
        })
    ], style={'marginBottom': '30px'}),

    # Interactive visualization section
    html.Div([
        html.H3("Environmental Impact Comparison", style={
            'textAlign': 'center',
            'fontFamily': 'monospace',
            'color': '#2c3e50',
            'marginBottom': '20px'
        }),
        
        # Interactive model comparison
        html.Div([
            dcc.Checklist(
                id='model-comparison',
                options=[
                    {'label': 'o3', 'value': 'o3'},
                    {'label': 'GPT-4o', 'value': 'GPT-4o'},
                    {'label': 'Claude-3.7', 'value': 'Claude-3.7 Sonnet'},
                    {'label': 'DeepSeek-R1', 'value': 'DeepSeek-R1'}
                ],
                value=['o3'],
                style={'marginBottom': '20px', 'display': 'flex', 'justifyContent': 'center', 'gap': '20px'},
                className='pixel-checkbox',
                inline=True
            )
        ], style={'marginBottom': '20px', 'textAlign': 'center'}),
        
        # Interactive chart
        dcc.Graph(
            id='impact-chart',
            style={'height': '400px'},
            config={'displayModeBar': False}
        ),
        
        # Interactive tips
        html.Div(id='tips-section', style={
            'marginTop': '20px',
            'padding': '15px',
            'fontFamily': 'monospace',
            'fontSize': '12px'
        })
    ], style={
        'maxWidth': '800px',
        'margin': '0 auto 30px auto',
        'padding': '20px',
        'backgroundColor': '#ffffff',
        'border': '3px solid #34495e',
        'borderRadius': '8px'
    }),



    html.Div([
        html.P("Estimates use 2025 industry-average PUE / WUE / CIF values", style={
            'textAlign': 'center',
            'fontSize': '10px',
            'color': '#7f8c8d',
            'marginTop': '20px',
            'fontFamily': 'monospace',
            'whiteSpace': 'nowrap'
        })
    ], id='footer', style={
        'position': 'fixed',
        'bottom': '0px',
        'left': '0',
        'right': '0',
        'backgroundColor': '#f0f8ff',
        'padding': '10px',
        'transition': 'transform 0.3s ease-in-out',
        'zIndex': '1000'
    })
], style={
    'fontFamily': 'monospace',
    'backgroundColor': '#f0f8ff',
    'minHeight': '100vh',
    'padding': '20px',
    'paddingBottom': '80px'  # Add space for footer
})

# Helper functions for interactive features
def create_impact_chart(comparison_models, prompt_tokens, response_length):
    """Create interactive chart comparing different models"""
    if not comparison_models:
        comparison_models = ['o3']
    
    models = []
    co2_values = []
    energy_values = []
    water_values = []
    
    for model in comparison_models:
        # Clean up model names for display
        if model == 'Claude-3.7 Sonnet':
            display_name = 'Claude-3.7'
        else:
            display_name = model
        models.append(display_name)
        
        # Calculate impact for this model
        e_prompt, w_prompt, c_prompt = calculate_impact(
            model_name=model,
            provider="azure-us",
            tokens_out=prompt_tokens,
            tps=400,
            latency_s=0.0
        )
        
        e_resp, w_resp, c_resp = calculate_impact(
            model_name=model,
            provider="azure-us",
            tokens_out=response_length,
            tps=400,
            latency_s=0.075
        )
        
        co2_values.append((c_prompt + c_resp) * 1000)  # Convert to grams
        energy_values.append((e_prompt + e_resp) * 1000)  # Convert to Wh
        water_values.append((w_prompt + w_resp) * 1000)  # Convert to mL
    
    # Create bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='CO₂e (g)',
        x=models,
        y=co2_values,
        marker_color='#e74c3c',
        text=[f'{v:.1f}g' for v in co2_values],
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        name='Energy (Wh)',
        x=models,
        y=energy_values,
        marker_color='#f39c12',
        text=[f'{v:.1f}Wh' for v in energy_values],
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        name='Water (mL)',
        x=models,
        y=water_values,
        marker_color='#3498db',
        text=[f'{v:.1f}mL' for v in water_values],
        textposition='auto'
    ))
    
    fig.update_layout(
        # title='Environmental Impact Comparison',
        xaxis_title='Model',
        yaxis_title='Impact',
        barmode='group',
        font=dict(family='monospace'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def generate_tips(co2, energy, water):
    """Generate interactive tips based on environmental impact"""
    tips = []
    
    if co2 > 0.001:  # More than 1g CO2
        tips.append("🌱 Consider using a smaller model for simple tasks")
    
    if energy > 0.1:  # More than 100mWh
        tips.append("⚡ High energy usage - try to be more concise")
    
    if water > 0.1:  # More than 100mL
        tips.append("💧 Significant water usage - batch your requests")
    
    if len(tips) == 0:
        tips.append("✅ Great! Your request has minimal environmental impact")
    
    return html.Div([
        html.H4("💡 Tips:", style={'marginBottom': '10px'}),
        html.Ul([html.Li(tip) for tip in tips])
    ])

# Custom CSS for pixel-art style - removed external CSS to fix warnings

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background-color: #f0f8ff !important;
                margin: 0;
                padding: 0;
                font-family: monospace;
            }
            html {
                background-color: #f0f8ff !important;
            }
            .pixel-slider .rc-slider-track {
                background-color: #34495e;
                height: 6px;
                border-radius: 3px;
            }
            .pixel-slider .rc-slider-handle {
                border: 2px solid #34495e;
                background-color: #ecf0f1;
                width: 16px;
                height: 16px;
                margin-top: -5px;
                border-radius: 2px;
            }
            .pixel-slider .rc-slider-rail {
                background-color: #bdc3c7;
                height: 6px;
                border-radius: 3px;
            }
            .pixel-radio input[type="radio"] {
                accent-color: #34495e;
            }
            .pixel-radio label {
                font-family: monospace;
                font-size: 12px;
                color: #34495e;
            }
            .pixel-checkbox input[type="checkbox"] {
                accent-color: #34495e;
            }
            .pixel-checkbox label {
                font-family: monospace;
                font-size: 12px;
                color: #34495e;
            }
            .footer-hidden {
                transform: translateY(100%);
            }
            
            /* Mechanical Counter Styles */
            @keyframes digitRoll {
                0% { transform: translateY(0px); }
                100% { transform: translateY(-270px); }
            }
            
            .digit-wheel {
                transition: transform 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            }
            
            .digit-wheel.rolling {
                animation: digitRoll 0.5s ease-out;
            }
        </style>
        <script>
            let scrollThreshold = 100; // Distance from bottom to show footer
            
            window.addEventListener('scroll', function() {
                let currentScroll = window.pageYOffset || document.documentElement.scrollTop;
                let windowHeight = window.innerHeight;
                let documentHeight = document.documentElement.scrollHeight;
                let footer = document.getElementById('footer');
                
                if (footer) {
                    // Check if we're near the bottom of the page
                    let distanceFromBottom = documentHeight - (currentScroll + windowHeight);
                    
                    if (distanceFromBottom <= scrollThreshold) {
                        // Near bottom - show footer
                        footer.classList.remove('footer-hidden');
                    } else {
                        // Not near bottom - hide footer
                        footer.classList.add('footer-hidden');
                    }
                }
            });
            
            // Also check on page load
            window.addEventListener('load', function() {
                let currentScroll = window.pageYOffset || document.documentElement.scrollTop;
                let windowHeight = window.innerHeight;
                let documentHeight = document.documentElement.scrollHeight;
                let footer = document.getElementById('footer');
                
                if (footer) {
                    let distanceFromBottom = documentHeight - (currentScroll + windowHeight);
                    
                    if (distanceFromBottom <= scrollThreshold) {
                        footer.classList.remove('footer-hidden');
                    } else {
                        footer.classList.add('footer-hidden');
                    }
                }
            });
        </script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

@callback(
    [Output('tokens-counter', 'children'),
     Output('words-counter', 'children'),
     Output('energy-counter', 'children'),
     Output('water-counter', 'children'),
     Output('co2-counter', 'children'),
     Output('impact-chart', 'figure'),
     Output('tips-section', 'children')],
    [Input('prompt-input', 'value'),
     Input('response-length-slider', 'value'),
     Input('model-selector', 'value'),
     Input('model-comparison', 'value')]
)
def update_metrics(prompt_text, response_length, model_name, comparison_models):
    if prompt_text:
        words = re.findall(r'\w+', prompt_text)
        prompt_tokens = int(len(words) / 0.75)
    else:
        prompt_tokens = 0

    total_tokens = prompt_tokens + response_length
    total_words = int(total_tokens * 0.75)

    if total_tokens > 0:
        e_prompt, w_prompt, c_prompt = calculate_impact(
            model_name=model_name,
            provider="azure-us",
            tokens_out=prompt_tokens,
            tps=400,
            latency_s=0.0
        )

        e_resp, w_resp, c_resp = calculate_impact(
            model_name=model_name,
            provider="azure-us",
            tokens_out=response_length,
            tps=400,
            latency_s=0.075
        )

        total_energy = e_prompt + e_resp
        total_water = w_prompt + w_resp
        total_co2 = c_prompt + c_resp
    else:
        total_energy = 0
        total_water = 0
        total_co2 = 0

    # Create mechanical counter components
    tokens_counter = create_counter_display(total_tokens, "TOKENS")
    words_counter = create_counter_display(total_words, "WORDS")
    energy_counter = create_counter_display(int(total_energy*1000), "ENERGY", "Wh")
    water_counter = create_counter_display(int(total_water*1000), "WATER", "mL")
    co2_counter = create_counter_display(int(total_co2*1000), "CO₂e", "g")
    
    # Create interactive chart
    chart_figure = create_impact_chart(comparison_models, prompt_tokens, response_length)
    
    # Generate interactive tips
    tips_text = generate_tips(total_co2, total_energy, total_water)
    
    return tokens_counter, words_counter, energy_counter, water_counter, co2_counter, chart_figure, tips_text

if __name__ == '__main__':
    print("Starting Dash server with debug mode enabled...")
    print("Server will be available at: http://localhost:8050")
    print("Hot-reloading should be active - try making changes to the code!")
    print("If changes don't appear, try refreshing your browser!")
    app.run_server(
        debug=True, 
        port=8050,
        dev_tools_hot_reload=True,
        dev_tools_ui=True
    )
