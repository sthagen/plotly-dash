from dash import Dash, Input, Output, dcc, html
from dash.exceptions import PreventUpdate


def test_dddo001_dynamic_options(dash_dcc):
    dropdown_options = [
        {"label": "New York City", "value": "NYC"},
        {"label": "Montreal", "value": "MTL"},
        {"label": "San Francisco", "value": "SF"},
    ]

    app = Dash(__name__)
    app.layout = dcc.Dropdown(id="my-dynamic-dropdown", options=[])

    @app.callback(
        Output("my-dynamic-dropdown", "options"),
        [Input("my-dynamic-dropdown", "search_value")],
    )
    def update_options(search_value):
        if not search_value:
            raise PreventUpdate
        return [o for o in dropdown_options if search_value in o["label"]]

    dash_dcc.start_server(app)

    # Get the inner input used for search value.
    dropdown = dash_dcc.find_element("#my-dynamic-dropdown")
    input_ = dropdown.find_element_by_css_selector("input")

    # Focus on the input to open the options menu
    input_.send_keys("x")

    # No options to be found with `x` in them, should show the empty message.
    dash_dcc.wait_for_text_to_equal(".Select-noresults", "No results found")

    input_.clear()
    input_.send_keys("o")

    options = dropdown.find_elements_by_css_selector(".VirtualizedSelectOption")

    # Should show all options.
    assert len(options) == 3

    # Searching for `on`
    input_.send_keys("n")

    options = dropdown.find_elements_by_css_selector(".VirtualizedSelectOption")

    assert len(options) == 1
    print(options)
    assert options[0].text == "Montreal"

    assert dash_dcc.get_logs() == []


def test_dddo002_array_value(dash_dcc):
    dropdown_options = [
        {"label": "New York City", "value": "New,York,City"},
        {"label": "Montreal", "value": "Montreal"},
        {"label": "San Francisco", "value": "San,Francisco"},
    ]

    app = Dash(__name__)
    arrayValue = ["San", "Francisco"]

    dropdown = dcc.Dropdown(
        options=dropdown_options,
        value=arrayValue,
    )
    app.layout = html.Div([dropdown])

    dash_dcc.start_server(app)

    dash_dcc.wait_for_text_to_equal("#react-select-2--value-item", "San Francisco")

    assert dash_dcc.get_logs() == []
