import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
from PIL import Image
import base64
import io, os, shutil
import main

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash.Dash(__name__)

app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H1(children="Report Generator", id="page-header"),
            class_name="text-center"
        )
    ) ,

    # File Upload Widget
    dbc.Row(
        dbc.Col(
            dcc.Upload(
                id='upload-data', children=html.Div(
                    [
                        'Drag and Drop or ', html.A('Click to upload images')
                    ]
                ), 
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=True
            )
        )
    ),
    
    # Display Uploaded Content
    dbc.Row([
        dbc.Col(
            html.Div(id='upload-info',children="Number of images to be uploaded: Nil",style={'width':'100%'}),
        ), 
        dbc.Col(
            html.Div(id = 'report-output',style= {'width':'100%'})
        )
    ]),

    # Buttons
    dbc.Row([
        dbc.Col(
            dbc.Button(children="Upload Images",id='upload-images-button'),
            width={'size':1,'offset':10}
        ),
        dbc.Col(
            dbc.Button(children="Generate Report", id="generate-report-button"),
            width={'size':1}
        )
    ]),

    html.Div(style={'margin-top': '10px'}),  # Add space between rows

    # Indicator
    dbc.Row(
        dbc.Col(
            dcc.Loading(
                id= "loading-1",
                type= 'default',
                children=html.Div(id="loading-output-1")
            )
        )
    ),

    html.Div(style={'margin-top': '10px'}),  # Add space between rows

    # Embedded PDF
    dbc.Row(
        dbc.Col(
            html.Iframe(
                id= 'pdf-viewer',
                src= '',
                width= '100%',
                height= '600%'
            )
        )
    )
])

@app.callback(
    Output(component_id= 'upload-info', component_property= 'children'),
    Output(component_id= 'report-output', component_property= 'children', allow_duplicate= True),
    Output(component_id='pdf-viewer', component_property= 'style', allow_duplicate= True),
    Input(component_id= 'upload-data', component_property= 'contents'),
    prevent_initial_call=True
)
def display_uploaded_images(contents):
    if not contents:
        raise PreventUpdate

    num_images = len(contents)
    upload_info = f'Number of images to be uploaded: {num_images}'
    images_uploaded = f'Status: Image(s) yet to be uploaded'
    return (upload_info , images_uploaded, {'display':'none'})

@app.callback(
    Output('report-output', 'children', allow_duplicate=True),
    Input('upload-images-button', 'n_clicks'),
    State('upload-data', 'contents'),
    prevent_initial_call=True
)
def upload_image(n_clicks, uploaded_images):
    if not n_clicks or not uploaded_images:
        raise PreventUpdate

    # Clear the "Uploaded Images" directory before saving new images
    UPLOADS_DIR = 'Uploaded Images'
    uploaded_images_dir = os.path.join(os.getcwd(), UPLOADS_DIR)
    if os.path.exists(uploaded_images_dir):
        shutil.rmtree(uploaded_images_dir)
    os.makedirs(uploaded_images_dir, exist_ok=True)

    # Create a div to display uploaded images
    image_divs = []
    for i, image_content in enumerate(uploaded_images):
        image_data = base64.b64decode(image_content.split(",")[1])
        img = Image.open(io.BytesIO(image_data))
        img_path = os.path.join(uploaded_images_dir, f"uploaded_image_{i}.png")
        img.save(img_path)
        # image_divs.append(html.Img(src=img_path))

    return "Status: Images uploaded successfully"

@app.callback(
    Output(component_id='report-output', component_property='children'),
    Output(component_id= 'loading-1', component_property= "children"),
    Output(component_id='pdf-viewer', component_property= 'src'),
    Output(component_id='pdf-viewer',component_property='style'),
    Input(component_id='generate-report-button',component_property='n_clicks')
)
def generate_report(nclicks):
    if not nclicks:
        raise PreventUpdate 
       
    rep_pdf = main.process_image_and_generate_report()
    loading_value = ''
    report_status = "Status: Report generated successfully"
    return (report_status, loading_value, rep_pdf,{'display':'block'})

if __name__ == '__main__':
    app.run_server(debug=False)
