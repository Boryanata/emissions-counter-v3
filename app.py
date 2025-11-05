import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import plotly.express as px
from emissions_counter.core import calculate_impact
from counter_component import create_counter_display, counter_css
import re

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout with Modern Design
app.layout = html.Div([
    # Modern Header with Gradient
    html.Div([
        html.H1("Emissions Calculator for LLMs", style={
            'textAlign': 'center', 
            'margin': '0',
            'fontFamily': '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
            'color': '#111827',
            'fontSize': '2.5rem',
            'fontWeight': '700',
            'letterSpacing': '-0.02em'
        }),
       
    ], style={
        'background': 'linear-gradient(135deg, rgba(229, 231, 235, 0.8) 0%, rgba(209, 213, 219, 0.8) 100%)',
        'padding': '2rem 2rem',
        'margin': '-20px -20px 40px -20px',
        'borderRadius': '0 0 2rem 2rem',
        'border': '2px solid #d1d5db',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'center',
        'minHeight': '120px'
    }),

    # Modern Input Card with Shadow - Wider
    html.Div([
        html.Div([
            html.Label("Input:", style={
                'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", sans-serif',
                'fontSize': '14px',
                'fontWeight': '600',
                'color': '#374151',
                'marginBottom': '8px',
                'display': 'block'
            }),
            dcc.Textarea(
                id='prompt-input',
                placeholder='Type or paste your prompt here...',
                style={
                    'width': '100%',
                    'height': '100px',
                    'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", sans-serif',
                    'fontSize': '14px',
                    'border': '1px solid #e5e7eb',
                    'borderRadius': '8px',
                    'backgroundColor': '#ffffff',
                    'resize': 'none',
                    'padding': '12px',
                    'transition': 'all 0.2s ease',
                    'boxShadow': '0 1px 2px rgba(0,0,0,0.05)'
                }
            ),
        ], style={'marginBottom': '24px'}),
        
        html.Div([
            html.Label("Expected Response Length:", style={
                'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", sans-serif',
                'fontSize': '14px',
                'fontWeight': '600',
                'color': '#374151',
                'marginBottom': '10px',
                'display': 'block'
            }),
            dcc.Slider(
                id='response-length-slider',
                min=10,
                max=2000,
                step=10,
                value=1000,
                marks={10: '10', 1000: '1000', 2000: '2000'},
                tooltip={"placement": "bottom", "always_visible": True},
                className='modern-slider'
            )
        ], style={'marginBottom': '24px'}),
        
        html.Div([
            html.Label("Model:", style={
                'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", sans-serif',
                'fontSize': '14px',
                'fontWeight': '600',
                'color': '#374151',
                'marginBottom': '12px',
                'display': 'block'
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
                style={'display': 'flex', 'gap': '24px', 'flexWrap': 'wrap'},
                className='modern-radio',
                inline=True
            )
        ])
    ], style={
        'maxWidth': '830px',  # Narrower to match counters visual width
        'margin': '0 auto 40px auto',
        'padding': '32px',
        'backgroundColor': '#ffffff',
        'borderRadius': '16px',
        'border': '1px solid #34495e',
        'boxShadow': '0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06)',
        'transition': 'all 0.3s ease'
    }, id='input-container'),

    # Mechanical Counter-style metrics - same width as input
    html.Div([
        html.Div([
            html.Div(id='tokens-counter', style={'display': 'inline-block'}),
            html.Div(id='words-counter', style={'display': 'inline-block'}),
            html.Div(id='energy-counter', style={'display': 'inline-block'}),
            html.Div(id='water-counter', style={'display': 'inline-block'}),
            html.Div(id='co2-counter', style={'display': 'inline-block'})
        ], style={
            'display': 'flex',
            'flexDirection': 'row',
            'justifyContent': 'center',
            'alignItems': 'center',
            'maxWidth': '900px',  # Match input container width
            'margin': '0 auto',
            'gap': '16px',
            'flexWrap': 'wrap'
        })
    ], style={'marginBottom': '40px'}, id='counters-container'),

    # Content Section - How Hungry Is AI?
    html.Div([
        html.H2("Making AI’s Footprint Visible 🌿", style={
            'textAlign': 'center',
            'fontFamily': '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
            'fontSize': '2rem',
            'fontWeight': '700',
            'color': '#111827',
            'marginBottom': '24px',
            'letterSpacing': '-0.01em'
        }),
        
        html.P([
            "Every question we ask a large language model consumes energy, evaporates water, and releases carbon. These are invisible costs — scattered across the data centers that power our daily conversations with AI.",
            html.Br(), html.Br(),
            "The Emissions Counter translates this hidden footprint into numbers we can see. It is grounded in the framework proposed by Jegham et al. (2025), the first large-scale study to measure the environmental cost of AI inference — the act of generating text — rather than training alone."
        ], style={
            'fontFamily': '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
            'fontSize': '1.1rem',
            'lineHeight': '1.8',
            'color': '#374151',
            'maxWidth': '800px',
            'margin': '0 auto 48px auto',
            'textAlign': 'left'
        }),
        
        # How the Counter Works
        html.H3("How the Counter Works", style={
            'fontFamily': '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
            'fontSize': '1.5rem',
            'fontWeight': '600',
            'color': '#111827',
            'marginBottom': '16px',
            'marginTop': '32px',
            'paddingLeft': '16px',
            'borderLeft': '4px solid #10b981'
        }),
        
        html.P([
            "The research behind this tool combines:",
            html.Br(),
            html.Br(),
            html.Strong("Model-specific performance data"), " (speed, latency, token throughput),",
            html.Br(),
            html.Strong("Hardware power characteristics"), " (H100/H200/A100 GPU systems), and",
            html.Br(),
            html.Strong("Regional infrastructure multipliers"), " — PUE for electricity overhead, WUE for cooling water, and CIF for carbon intensity.",
            html.Br(), html.Br(),
            "Together, these factors reveal how much real-world electricity, water, and carbon are embodied in a single prompt. A short GPT-4o query, for instance, consumes about 0.4 Wh — roughly 40 percent more than a Google search. Reasoning-heavy models such as DeepSeek-R1 or o3 can draw more than 30 Wh per response, equivalent to running a large TV for half an hour."
        ], style={
            'fontFamily': '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
            'fontSize': '1rem',
            'lineHeight': '1.8',
            'color': '#374151',
            'maxWidth': '800px',
            'margin': '0 auto 48px auto',
            'textAlign': 'left'
        }),
        
        # What the Numbers Mean
        html.H3("What the Numbers Mean", style={
            'fontFamily': '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
            'fontSize': '1.5rem',
            'fontWeight': '600',
            'color': '#111827',
            'marginBottom': '16px',
            'marginTop': '32px',
            'paddingLeft': '16px',
            'borderLeft': '4px solid #10b981'
        }),
        
        html.Div([
            html.P([
                html.Strong("Energy (Wh)"), " → the electricity used by servers to generate a reply.",
            ], style={
                'fontFamily': '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
                'fontSize': '1rem',
                'lineHeight': '1.8',
                'color': '#374151',
                'marginBottom': '12px'
            }),
            html.P([
                html.Strong("Water (mL)"), " → the freshwater lost to evaporation as data centers cool their processors.",
            ], style={
                'fontFamily': '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
                'fontSize': '1rem',
                'lineHeight': '1.8',
                'color': '#374151',
                'marginBottom': '12px'
            }),
            html.P([
                html.Strong("CO₂e (g)"), " → the greenhouse gases emitted from the electricity that powers those systems.",
            ], style={
                'fontFamily': '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
                'fontSize': '1rem',
                'lineHeight': '1.8',
                'color': '#374151',
                'marginBottom': '12px'
            }),
            html.P([
                "When scaled to hundreds of millions of queries each day, these small units compound dramatically. The study estimates that daily GPT-4o activity alone consumes electricity comparable to tens of thousands of U.S. homes, evaporates enough freshwater to meet the annual drinking needs of over a million people, and produces carbon that would require a Chicago-sized forest to offset."
            ], style={
                'fontFamily': '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
                'fontSize': '1rem',
                'lineHeight': '1.8',
                'color': '#374151',
                'marginTop': '16px'
            })
        ], style={
            'maxWidth': '800px',
            'margin': '0 auto 48px auto',
            'textAlign': 'left'
        }),
        
        # Why It Matters
        html.H3("Why It Matters", style={
            'fontFamily': '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
            'fontSize': '1.5rem',
            'fontWeight': '600',
            'color': '#111827',
            'marginBottom': '16px',
            'marginTop': '32px',
            'paddingLeft': '16px',
            'borderLeft': '4px solid #10b981'
        }),
        
        html.P([
            "As language models become faster and cheaper, our collective usage grows even faster — a pattern known as the Jevons Paradox. Efficiency gains per query can't offset the environmental load if total demand keeps multiplying.",
            html.Br(), html.Br(),
            "Understanding these hidden costs helps make AI's physical footprint visible — not to discourage use, but to invite transparency, accountability, and more sustainable infrastructure choices."
        ], style={
            'fontFamily': '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
            'fontSize': '1rem',
            'lineHeight': '1.8',
            'color': '#374151',
            'maxWidth': '800px',
            'margin': '0 auto 48px auto',
            'textAlign': 'left'
        }),
        
        # About the Data
        html.H3("About the Data", style={
            'fontFamily': '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
            'fontSize': '1.5rem',
            'fontWeight': '600',
            'color': '#111827',
            'marginBottom': '16px',
            'marginTop': '32px',
            'paddingLeft': '16px',
            'borderLeft': '4px solid #10b981'
        }),
        
        html.P([
            "All metrics shown are estimates based on 2025 industry averages for:",
            html.Br(), html.Br(),
            html.Strong("Data-center efficiency"), " (PUE ≈ 1.1–1.3)",
            html.Br(),
            html.Strong("Cooling water intensity"), " (WUE ≈ 0.3–1.2 L per kWh)",
            html.Br(),
            html.Strong("Regional carbon factors"), " (CIF ≈ 0.35–0.6 kg CO₂e per kWh)",
            html.Br(), html.Br(),
            "The values shown represent operational (Scope 1 + 2) impacts during model inference and exclude manufacturing emissions. They vary by hardware type, energy source, and deployment region. The counter translates these parameters into real-time approximations of electricity, water, and carbon embodied in each generated response."
        ], style={
            'fontFamily': '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
            'fontSize': '1rem',
            'lineHeight': '1.8',
            'color': '#374151',
            'maxWidth': '800px',
            'margin': '0 auto 48px auto',
            'textAlign': 'left'
        })
        
    ], style={
        'maxWidth': '850px',
        'margin': '0 auto 60px auto',
        'padding': '40px 32px',
        'backgroundColor': '#ffffff',
        'borderRadius': '16px',
        'boxShadow': '0 1px 3px rgba(0,0,0,0.05)'
    }),

    # Modern Visualization Card
    html.Div([
        html.H3("Environmental Impact Comparison", style={
            'textAlign': 'center',
            'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", sans-serif',
            'fontSize': '1.5rem',
            'fontWeight': '600',
            'color': '#111827',
            'marginBottom': '24px'
        }),
        
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
                style={'marginBottom': '24px', 'display': 'flex', 'justifyContent': 'center', 'gap': '24px', 'flexWrap': 'wrap'},
                className='modern-checkbox',
                inline=True
            )
        ], style={'marginBottom': '24px', 'textAlign': 'center'}),
        
        dcc.Graph(
            id='impact-chart',
            style={'height': '450px'},
            config={'displayModeBar': False}
        ),
        
        html.Div(id='tips-section', style={
            'marginTop': '24px',
            'padding': '20px',
            'backgroundColor': '#f9fafb',
            'borderRadius': '12px',
            'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", sans-serif',
            'fontSize': '14px',
            'lineHeight': '1.6'
        })
    ], style={
        'maxWidth': '850px',  # Match counters and input width
        'margin': '0 auto 40px auto',
        'padding': '32px',
        'backgroundColor': '#ffffff',
        'borderRadius': '16px',
        'border': '1px solid #34495e',
        'boxShadow': '0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06)'
    }),

    # Modern Footer
    html.Div([
        html.P("Estimates use 2025 industry-average PUE / WUE / CIF values", style={
            'textAlign': 'center',
            'fontSize': '12px',
            'color': '#6b7280',
            'margin': '0',
            'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", sans-serif'
        })
    ], id='footer', style={
        'position': 'fixed',
        'bottom': '0px',
        'left': '0',
        'right': '0',
        'backgroundColor': '#ffffff',
        'padding': '16px',
        'transition': 'transform 0.3s ease-in-out',
        'zIndex': '1000',
        'boxShadow': '0 -2px 8px rgba(0,0,0,0.1)',
        'borderTop': '1px solid #e5e7eb'
    })
], style={
    'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", sans-serif',
    'background': 'linear-gradient(to bottom, #f8fafc 0%, #e2e8f0 100%)',
    'minHeight': '100vh',
    'padding': '20px',
    'paddingBottom': '100px'
})

# Helper functions (same as original)
def create_impact_chart(comparison_models, prompt_tokens, response_length):
    """Create interactive chart comparing different models"""
    if not comparison_models:
        comparison_models = ['o3']
    
    models = []
    co2_values = []
    energy_values = []
    water_values = []
    
    for model in comparison_models:
        if model == 'Claude-3.7 Sonnet':
            display_name = 'Claude-3.7'
        else:
            display_name = model
        models.append(display_name)
        
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
        
        co2_values.append((c_prompt + c_resp) * 1000)
        energy_values.append((e_prompt + e_resp) * 1000)
        water_values.append((w_prompt + w_resp) * 1000)
    
    fig = go.Figure()
    
    # Solid colors - green for CO2, orange for energy, blue for water
    fig.add_trace(go.Bar(
        name='CO₂e (g)',
        x=models,
        y=co2_values,
        marker_color='#10b981',  # Green for CO2
        text=[f'{v:.1f}g' for v in co2_values],
        textposition='auto',
        textfont=dict(size=12, color='white', family='-apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", sans-serif')
    ))
    
    fig.add_trace(go.Bar(
        name='Energy (Wh)',
        x=models,
        y=energy_values,
        marker_color='#f59e0b',  # Orange for energy
        text=[f'{v:.1f}Wh' for v in energy_values],
        textposition='auto',
        textfont=dict(size=12, color='white', family='-apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", sans-serif')
    ))
    
    fig.add_trace(go.Bar(
        name='Water (mL)',
        x=models,
        y=water_values,
        marker_color='#3b82f6',  # Blue for water
        text=[f'{v:.1f}mL' for v in water_values],
        textposition='auto',
        textfont=dict(size=12, color='white', family='-apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", sans-serif')
    ))
    
    fig.update_layout(
        xaxis_title='Model',
        yaxis_title='Impact',
        barmode='group',
        font=dict(
            family='-apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", sans-serif',
            size=12,
            color='#374151'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(
            gridcolor='#e5e7eb',
            gridwidth=1
        ),
        yaxis=dict(
            gridcolor='#e5e7eb',
            gridwidth=1
        ),
        hovermode='x unified'
    )
    
    return fig

def generate_tips(co2, energy, water, comparison_models=None):
    """Generate interactive tips based on environmental impact and selected models"""
    if not comparison_models:
        comparison_models = []
    
    tips = []
    
    # Model-specific tips
    if 'o3' in comparison_models:
        tips.append("🧠 o3 is a reasoning model - use it for complex tasks that require deep thinking")
    
    if 'DeepSeek-R1' in comparison_models:
        tips.append("🔬 DeepSeek-R1 excels at reasoning but consumes more energy - consider it for specialized use cases")
    
    if 'GPT-4o' in comparison_models:
        tips.append("⚡ GPT-4o offers a good balance of performance and efficiency for most tasks")
    
    if 'Claude-3.7 Sonnet' in comparison_models:
        tips.append("🎯 Claude-3.7 Sonnet is efficient for general-purpose tasks")
    
    # Impact-based tips
    if energy > 0.1:
        if len(comparison_models) > 1:
            tips.append("⚡ Comparing multiple models increases energy usage - select only what you need")
        else:
            tips.append("⚡ High energy usage - try to be more concise")
    
    if water > 0.1:
        tips.append("💧 Significant water usage - batch your requests when possible")
    
    if co2 > 0.001:
        if len(comparison_models) > 1:
            tips.append("🌱 Comparing multiple models multiplies emissions - choose one model for simple tasks")
        else:
            tips.append("🌱 Consider using a smaller model for simple tasks")
    
    if len(tips) == 0:
        tips.append("✅ Great! Your request has minimal environmental impact")
    
    return html.Div([
        html.H4("💡 Tips", style={
            'marginBottom': '12px',
            'fontSize': '16px',
            'fontWeight': '600',
            'color': '#111827',
            'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", sans-serif'
        }),
        html.Ul([html.Li(tip, style={'marginBottom': '8px', 'color': '#374151'}) for tip in tips], style={
            'listStyle': 'none',
            'padding': '0',
            'margin': '0'
        })
    ])

# Modern CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            * {
                box-sizing: border-box;
            }
            
            body {
                background: linear-gradient(to bottom, #f8fafc 0%, #e2e8f0 100%) !important;
                margin: 0;
                padding: 0;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", sans-serif;
            }
            
            html {
                background: linear-gradient(to bottom, #f8fafc 0%, #e2e8f0 100%) !important;
            }
            
            /* Modern Slider */
            .modern-slider .rc-slider-track {
                background: #10b981;
                height: 8px;
                border-radius: 4px;
            }
            
            .modern-slider .rc-slider-handle {
                border: 3px solid #10b981;
                background-color: #ffffff;
                width: 20px;
                height: 20px;
                margin-top: -6px;
                border-radius: 50%;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                transition: all 0.2s ease;
            }
            
            .modern-slider .rc-slider-handle:hover {
                transform: scale(1.1);
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
            
            .modern-slider .rc-slider-rail {
                background-color: #e5e7eb;
                height: 8px;
                border-radius: 4px;
            }
            
            /* Modern Radio Buttons */
            .modern-radio input[type="radio"] {
                accent-color: #667eea;
                width: 18px;
                height: 18px;
                margin-right: 8px;
            }
            
            .modern-radio label {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", sans-serif;
                font-size: 14px;
                color: #374151;
                font-weight: 500;
                cursor: pointer;
                transition: color 0.2s ease;
            }
            
            .modern-radio label:hover {
                color: #667eea;
            }
            
            /* Modern Checkboxes */
            .modern-checkbox input[type="checkbox"] {
                accent-color: #667eea;
                width: 18px;
                height: 18px;
                margin-right: 8px;
            }
            
            .modern-checkbox label {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", sans-serif;
                font-size: 14px;
                color: #374151;
                font-weight: 500;
                cursor: pointer;
                transition: color 0.2s ease;
            }
            
            .modern-checkbox label:hover {
                color: #667eea;
            }
            
            /* Textarea Focus */
            textarea:focus {
                outline: none;
                border-color: #667eea !important;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
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
            
            /* Smooth Scroll */
            html {
                scroll-behavior: smooth;
            }
        </style>
        <script>
            let scrollThreshold = 100;
            
            window.addEventListener('scroll', function() {
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

    tokens_counter = create_counter_display(total_tokens, "TOKENS")
    words_counter = create_counter_display(total_words, "WORDS")
    energy_counter = create_counter_display(int(total_energy*1000), "ENERGY", "Wh")
    water_counter = create_counter_display(int(total_water*1000), "WATER", "mL")
    co2_counter = create_counter_display(int(total_co2*1000), "CO₂e", "g")
    
    chart_figure = create_impact_chart(comparison_models, prompt_tokens, response_length)
    tips_text = generate_tips(total_co2, total_energy, total_water, comparison_models)
    
    return tokens_counter, words_counter, energy_counter, water_counter, co2_counter, chart_figure, tips_text

if __name__ == '__main__':
    import os
    # Hugging Face Spaces uses port 7860, but also checks PORT env var
    port = int(os.environ.get('PORT', os.environ.get('SPACE_PORT', 7860)))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"Starting Dash server on port {port}...")
    print(f"Debug mode: {debug}")
    
    app.run_server(
        debug=debug,
        host='0.0.0.0',
        port=port
    )

