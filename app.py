import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
from dash.dependencies import Input,Output
import plotly.express as px

external_stylesheet = [
    {
        'rel':"stylesheet"
        'href':"https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css"
        'integrity':"sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2"
        'crossorigin':"anonymous"
    }
]