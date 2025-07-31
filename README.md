# Emissions Calculator for LLMs

A real-time environmental impact calculator for Large Language Models (LLMs) with mechanical counter-style displays.

## 🌍 What it does

This interactive web application calculates the environmental impact of using different LLM models by estimating:
- **Energy consumption** (Wh)
- **Water usage** (mL) 
- **Carbon emissions** (CO₂e in grams)

## 🚰 Features

- **Mechanical Counter Display**: Realistic rolling digit wheels like physical flow meters
- **Interactive Model Comparison**: Compare environmental impact across different models
- **Real-time Calculations**: Instant updates as you type
- **Visual Charts**: Bar charts showing impact comparisons
- **Smart Tips**: Personalized advice based on your usage
- **Responsive Design**: Works on desktop and mobile

## 🎯 Supported Models

- **o3** (Anthropic)
- **GPT-4o** (OpenAI)
- **Claude-3.7** (Anthropic)
- **DeepSeek-R1** (DeepSeek)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/emissions-counter-v3.git
   cd emissions-counter-v3
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app_dash.py
   ```

4. **Open in browser**:
   Navigate to `http://localhost:8050`

## 📊 How to Use

1. **Enter your prompt** in the text area
2. **Adjust response length** using the slider
3. **Select your model** from the radio buttons
4. **Compare models** by checking multiple options in the comparison section
5. **View real-time metrics** in the mechanical counters
6. **Check the visualization** for impact comparisons
7. **Read the tips** for environmental advice

## 🔧 Technical Details

- **Framework**: Dash (Python)
- **Styling**: Custom CSS with monospace fonts
- **Animations**: CSS transitions for mechanical counter effects
- **Calculations**: Based on 2025 industry-average PUE/WUE/CIF values
- **Responsive**: Mobile-friendly design

## 📈 Environmental Impact

The calculator uses industry-standard metrics:
- **PUE** (Power Usage Effectiveness)
- **WUE** (Water Usage Effectiveness) 
- **CIF** (Carbon Intensity Factor)

All estimates are based on 2025 industry averages for cloud computing infrastructure.

## 🎨 Design Features

- **Mechanical Counters**: Individual digit wheels that roll like physical meters
- **Monospace Typography**: Clean, technical appearance
- **Interactive Elements**: Real-time updates and smooth animations
- **Footer Behavior**: Appears only when scrolling to bottom
- **Color-coded Charts**: Easy-to-read environmental impact comparisons

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.

---

*Built with ❤️ and 🌱 for a more sustainable AI future* 