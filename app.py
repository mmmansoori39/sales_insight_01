from flask import Flask, render_template, request, redirect, url_for, session
import os
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from flask_socketio import SocketIO


app = Flask(__name__)
app.secret_key = 'mdmoinuddinmansoori'
socketio = SocketIO(app)


# Dummy database (replace with an actual database in a real project)
users = [{'username': 'user1', 'password': 'password1'}, {'username': 'user2', 'password': 'password2'}]

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
        return redirect(url_for('dashboard_page'))

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/signupsucc', methods=['POST'])
def signupsucc():
    return render_template('login.html')

@app.route('/upload_page')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        data = pd.read_excel(uploaded_file, header=0)
        cleaned_data = data.drop_duplicates()
        session['cleaned_data'] = cleaned_data.to_html(classes='data')
        return render_template('display.html', tables=[data.to_html(classes='data')], titles=['Data'])

    return render_template('index.html', error='Please upload a file.')

@app.route('/chart_options')
def chart_options():
    if 'cleaned_data' not in session:
        return redirect(url_for('index'))

    return render_template('display.html')

@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    if 'cleaned_data' not in session:
        return redirect(url_for('index'))

    chart_type = request.form.get('chart_type')
    x_axis = request.form.get('x_axis')
    y_axis = request.form.get('y_axis')

    cleaned_data = pd.read_html(session['cleaned_data'], index_col=0)[0]

    if chart_type == 'pie':
        plt.pie(cleaned_data[y_axis], labels=cleaned_data[x_axis], autopct='%1.1f%%')
        plt.title('Pie Chart')

    elif chart_type == 'bar':
        plt.bar(cleaned_data[x_axis], cleaned_data[y_axis])
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title('Bar Graph')

    elif chart_type == 'line':
        plt.plot(cleaned_data[x_axis], cleaned_data[y_axis], marker='o')
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title('Line Chart')

    elif chart_type == 'bubble':
        # For simplicity, bubble chart is represented as a scatter plot with marker size based on a third column
        size_column = request.form.get('size_column')
        plt.scatter(cleaned_data[x_axis], cleaned_data[y_axis], s=cleaned_data[size_column])
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title('Bubble Chart')

    elif chart_type == 'scatter':
        plt.scatter(cleaned_data[x_axis], cleaned_data[y_axis], marker='o' )
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title('Scatter Plot')

    elif chart_type == 'stacked_bar':
        # For simplicity, stacked bar chart is represented as a regular bar chart
        plt.bar(cleaned_data[x_axis], cleaned_data[y_axis], bottom=cleaned_data[y_axis])
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title('Stacked Bar Chart')

    else:
        return render_template('display.html', error='Invalid chart type selected')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    
    # Save the generated chart to user's chart history
    chart_entry = {
        'title': f'{chart_type.capitalize()} Chart',
        'type': chart_type,
        'x_axis': x_axis,
        'y_axis': y_axis,
        'plot_url': plot_url
    }

    if 'chart_history' not in session:
        session['history'] = []

    session['history'].append(chart_entry)

    return render_template('generated_chart.html', plot_url=plot_url)

@app.route('/history_page')
def chart_history():
    if 'history' not in session:
        session['history'] = []

    return render_template('history.html', chart_history=session['history'])


@app.route('/dashboard_page')
def dashboard_page():
    return render_template('dashboard.html')


@app.route('/feedback_page')
def feedback_page():
    return render_template('feedback.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    feedback = request.form['feedback']

    # Add code to handle feedback (e.g., store in a database)

    return "Thank you for your feedback!"

@app.route('/explore_page')
def explore_page():
    return render_template('explore.html')

@app.route('/accessible_page')
def accessible_page():
    return render_template('accessible.html')



@app.route('/voice_activation_page')
def voice_activation_page():
    return render_template('voice_activation.html')



@app.route('/text_to_speech_page')
def text_to_speech_page():
    return render_template('text_to_speech.html')

@app.route('/logout_page')
def logout_page():
    return render_template('logout.html')

@app.route('/setting_page')
def setting_page():
    return render_template('setting.html')


@app.route('/voice_command')
def voice_command():
    return render_template('voice.html')

if __name__ == '__main__':
    import eventlet
    eventlet.monkey_patch()

    # Start the Flask-SocketIO application
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

