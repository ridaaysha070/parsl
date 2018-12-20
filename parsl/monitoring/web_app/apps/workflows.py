import pandas as pd
import dash_html_components as html
from parsl.monitoring.web_app.utils import num_to_timestamp, DB_DATE_FORMAT

from parsl.monitoring.web_app.app import get_db, close_db


def dataframe_to_html_table(id, dataframe):

    def href(i):
        return '/workflows/' + dataframe['run_id'].iloc[i]

    return html.Table(id=id, children=(
            [html.Tr([html.Th(" ".join([x.capitalize() for x in col.split('_')])) for col in dataframe.columns[1:]])] +

            # Body
            [html.Tr([
                html.Td(html.A(children=dataframe.iloc[i]['workflow_name'], href=href(i))),
                html.Td(html.A(children=dataframe.iloc[i]['workflow_version'], href=href(i))),
                html.Td(html.A(children=num_to_timestamp(float(dataframe.iloc[i]['time_began']))
                               .strftime(DB_DATE_FORMAT) if dataframe.iloc[i]['time_began'] != 'None' else 'None', href=href(i))),
                html.Td(html.A(children=num_to_timestamp(float(dataframe.iloc[i]['time_completed']))
                               .strftime(DB_DATE_FORMAT) if dataframe.iloc[i]['time_completed'] != 'None' else 'None', href=href(i))),
                html.Td(html.A(children=dataframe.iloc[i]['tasks_completed_count'], href=href(i))),
                html.Td(html.A(children=dataframe.iloc[i]['tasks_failed_count'], href=href(i))),
                html.Td(html.A(children=dataframe.iloc[i]['user'], href=href(i))),
                html.Td(html.A(children=dataframe.iloc[i]['host'], href=href(i))),
                html.Td(html.A(children=dataframe.iloc[i]['rundir'], href=href(i)))
            ]) for i in range(len(dataframe))])
                      )


sql_conn = get_db()

layout = html.Div(children=[
    html.H1("Workflows"),
    dataframe_to_html_table(id='workflows_table',
                            dataframe=pd.read_sql_query("SELECT run_id, "
                                                        "workflow_name, "
                                                        "workflow_version, "
                                                        "time_began, "
                                                        "time_completed, "
                                                        "tasks_completed_count, "
                                                        "tasks_failed_count, "
                                                        "user, "
                                                        "host, "
                                                        "rundir FROM workflows", sql_conn)
                                        .sort_values(
                                            by=['time_began'],
                                            ascending=[True])
                                        .drop_duplicates(
                                            subset=['workflow_name', 'workflow_version'],
                                            keep='last')
                                        .sort_values(
                                            by=['time_began'],
                                            ascending=[False])),
])


close_db()
