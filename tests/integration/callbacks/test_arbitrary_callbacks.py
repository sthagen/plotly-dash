import time
from multiprocessing import Value

from dash import (
    Dash,
    Input,
    Output,
    html,
    set_props,
    register_page,
    clientside_callback,
)


def test_arb001_global_set_props(dash_duo):
    app = Dash()
    app.layout = html.Div(
        [
            html.Div(id="output"),
            html.Div(id="secondary-output"),
            html.Button("click", id="clicker"),
        ]
    )

    @app.callback(
        Output("output", "children"),
        Input("clicker", "n_clicks"),
        prevent_initial_call=True,
    )
    def on_click(n_clicks):
        set_props("secondary-output", {"children": "secondary"})
        return f"Clicked {n_clicks} times"

    dash_duo.start_server(app)

    dash_duo.wait_for_element("#clicker").click()
    dash_duo.wait_for_text_to_equal("#output", "Clicked 1 times")
    dash_duo.wait_for_text_to_equal("#secondary-output", "secondary")


def test_arb002_no_output_callbacks(dash_duo):
    app = Dash()

    counter = Value("i", 0)

    app.layout = html.Div(
        [
            html.Div(id="secondary-output"),
            html.Button("no-output", id="no-output"),
            html.Button("no-output2", id="no-output2"),
            html.Button("no-output3", id="no-output3"),
        ]
    )

    @app.callback(
        Input("no-output", "n_clicks"),
        prevent_initial_call=True,
    )
    def no_output1(_):
        set_props("secondary-output", {"children": "no-output"})

    @app.callback(
        Input("no-output2", "n_clicks"),
        prevent_initial_call=True,
    )
    def no_output2(_):
        set_props("secondary-output", {"children": "no-output2"})

    @app.callback(
        Input("no-output3", "n_clicks"),
        prevent_initial_call=True,
    )
    def no_output3(_):
        with counter.get_lock():
            counter.value += 1

    dash_duo.start_server(app)

    dash_duo.wait_for_element("#no-output").click()
    dash_duo.wait_for_text_to_equal("#secondary-output", "no-output")

    dash_duo.wait_for_element("#no-output2").click()
    dash_duo.wait_for_text_to_equal("#secondary-output", "no-output2")

    dash_duo.wait_for_element("#no-output3").click()

    time.sleep(1)
    with counter.get_lock():
        assert counter.value == 1


def test_arb003_arbitrary_pages(dash_duo, clear_pages_state):
    app = Dash(use_pages=True, pages_folder="")

    register_page(
        "page",
        "/",
        layout=html.Div(
            [
                html.Div(id="secondary-output"),
                html.Button("no-output", id="no-output"),
                html.Button("no-output2", id="no-output2"),
            ]
        ),
    )

    @app.callback(
        Input("no-output", "n_clicks"),
        prevent_initial_call=True,
    )
    def no_output(_):
        set_props("secondary-output", {"children": "no-output"})

    @app.callback(
        Input("no-output2", "n_clicks"),
        prevent_initial_call=True,
    )
    def no_output(_):
        set_props("secondary-output", {"children": "no-output2"})

    dash_duo.start_server(app)

    dash_duo.wait_for_element("#no-output").click()
    dash_duo.wait_for_text_to_equal("#secondary-output", "no-output")

    dash_duo.wait_for_element("#no-output2").click()
    dash_duo.wait_for_text_to_equal("#secondary-output", "no-output2")


def test_arb004_wildcard_set_props(dash_duo):
    app = Dash()
    app.layout = html.Div(
        [
            html.Button("click", id="click"),
            html.Div(html.Div(id={"id": "output", "index": 0}), id="output"),
        ]
    )

    @app.callback(
        Input("click", "n_clicks"),
        prevent_initial_call=True,
    )
    def on_click(n_clicks):
        set_props(
            {"id": "output", "index": 0}, {"children": f"Clicked {n_clicks} times"}
        )

    dash_duo.start_server(app)

    dash_duo.wait_for_element("#click").click()
    dash_duo.wait_for_text_to_equal("#output", "Clicked 1 times")


def test_arb005_no_output_error(dash_duo):
    app = Dash()

    app.layout = html.Div([html.Button("start", id="start")])

    @app.callback(Input("start", "n_clicks"), prevent_initial_call=True)
    def on_click(clicked):
        return f"clicked {clicked}"

    dash_duo.start_server(
        app,
        debug=True,
        use_reloader=False,
        use_debugger=True,
        dev_tools_hot_reload=False,
    )

    dash_duo.wait_for_element("#start").click()
    dash_duo.wait_for_text_to_equal(
        ".dash-fe-error__title",
        "Callback error with no output from input start.n_clicks",
    )


def test_arb006_multi_set_props(dash_duo):
    app = Dash()

    app.layout = [
        html.Button("start", id="start"),
        html.Div("initial", id="output"),
    ]

    @app.callback(
        Input("start", "n_clicks"),
    )
    def on_click(_):
        set_props("output", {"children": "changed"})
        set_props("output", {"style": {"background": "rgb(255,0,0)"}})

    dash_duo.start_server(app)
    dash_duo.wait_for_element("#start").click()
    dash_duo.wait_for_text_to_equal("#output", "changed")
    dash_duo.wait_for_style_to_equal(
        "#output", "background-color", "rgba(255, 0, 0, 1)"
    )


def test_arb007_clientside_no_output(dash_duo):
    app = Dash()

    app.layout = [
        html.Button("start", id="start1"),
        html.Button("start2", id="start2"),
        html.Div(id="output"),
    ]

    clientside_callback(
        """
        function(_) {
            dash_clientside.set_props('output', {children: 'start1'})
        }
        """,
        Input("start1", "n_clicks"),
        prevent_initial_call=True,
    )
    clientside_callback(
        """
        function(_) {
            dash_clientside.set_props('output', {children: 'start2'})
        }
        """,
        Input("start2", "n_clicks"),
        prevent_initial_call=True,
    )

    dash_duo.start_server(app)

    dash_duo.find_element("#start1").click()
    dash_duo.wait_for_text_to_equal("#output", "start1")
    dash_duo.find_element("#start2").click()
    dash_duo.wait_for_text_to_equal("#output", "start2")
