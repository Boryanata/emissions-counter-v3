import dash
from dash import html, dcc

def create_digit_wheel(value, max_value=9):
    """Create a single digit wheel that scrolls like a mechanical counter"""
    return html.Div([
        html.Div([
            html.Div([
                html.Span(str(i), style={
                    'display': 'block',
                    'height': '30px',
                    'lineHeight': '30px',
                    'textAlign': 'center',
                    'fontFamily': 'monospace',
                    'fontSize': '24px',
                    'fontWeight': 'bold',
                    'color': '#2c3e50'
                }) for i in range(10)
            ], style={
                'transform': f'translateY(-{value * 30}px)',
                'transition': 'transform 0.5s ease-out'
            })
        ], style={
            'height': '30px',
            'overflow': 'hidden',
            'border': '2px solid #34495e',
            'borderRadius': '4px',
            'backgroundColor': '#ecf0f1'
        })
    ], style={
        'display': 'inline-block',
        'margin': '0 2px',
        'verticalAlign': 'top'
    })

def create_counter_display(value, label, unit=""):
    """Create a counter display with rolling digits"""
    # Convert value to string and pad with zeros
    value_str = str(value).zfill(4)  # 4 digits for a more compact display
    
    return html.Div([
        # Label
        html.Div(label, style={
            'fontFamily': 'monospace',
            'fontSize': '10px',
            'color': '#7f8c8d',
            'textAlign': 'center',
            'marginBottom': '5px',
            'fontWeight': 'bold'
        }),
        
        # Digit wheels container with inline unit
        html.Div([
            *[create_digit_wheel(int(digit)) for digit in value_str],
            # Unit label inline after the last digit
            html.Span(unit, style={
                'fontFamily': 'monospace',
                'fontSize': '12px',
                'color': '#7f8c8d',
                'fontWeight': 'bold',
                'marginLeft': '8px',
                'verticalAlign': 'top',
                'lineHeight': '30px'
            }) if unit else None
        ], style={
            'textAlign': 'center',
            'marginBottom': '5px'
        })
    ], style={
        'padding': '12px',
        'border': '3px solid #34495e',
        'borderRadius': '8px',
        'backgroundColor': '#ffffff',
        'margin': '8px',
        'minWidth': '140px',
        'boxShadow': '3px 3px 6px rgba(0,0,0,0.3)',
        'textAlign': 'center'
    })

# CSS for the counter animation
counter_css = """
<style>
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
""" 