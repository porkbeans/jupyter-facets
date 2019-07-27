__version__ = '0.2.0'
__all__ = ["dive", "overview"]

import base64
import random
import string
import typing

import numpy
import pandas
from IPython.core.display import HTML

from facets_overview.generic_feature_statistics_generator import GenericFeatureStatisticsGenerator

FACETS_DIVE_TEMPLATE = """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/webcomponentsjs/1.3.3/webcomponents-lite.js"></script>
    <link rel="import" href="https://raw.githubusercontent.com/PAIR-code/facets/1.0.0/facets-dist/facets-jupyter.html">
    <facets-dive id="{elem_id}" height="600"></facets-dive>
    <script>
      var data = {json_str};
      document.querySelector("#{elem_id}").data = data;
    </script>
"""

FACETS_OVERVIEW_TEMPLATE = """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/webcomponentsjs/1.3.3/webcomponents-lite.js"></script>
    <link rel="import" href="https://raw.githubusercontent.com/PAIR-code/facets/1.0.0/facets-dist/facets-jupyter.html">
    <facets-overview id="{elem_id}"></facets-overview>
    <script>
      document.querySelector("#{elem_id}").protoInput = "{proto_str}";
    </script>
"""


def _generate_element_id() -> str:
    return "facets_" + "".join(random.choices(string.digits + string.ascii_letters, k=20))


def dive(data: pandas.DataFrame) -> HTML:
    # Element ID MUST be unique
    elem_id = _generate_element_id()
    json_str = data.to_json(orient='records')
    return HTML(FACETS_DIVE_TEMPLATE.format(elem_id=elem_id, json_str=json_str))


def overview(tables: typing.Union[pandas.DataFrame, typing.Mapping[str, pandas.DataFrame]]) -> HTML:
    # Element ID MUST be unique
    elem_id = _generate_element_id()

    if isinstance(tables, pandas.DataFrame):
        tables = {"default": tables}

    table_list = []
    for name, table in tables.items():
        # Convert PandasExtensionDType column to object column because facets currently doesn't support it.
        view = table.copy()
        for k, v in view.dtypes.iteritems():
            if not isinstance(v, numpy.dtype):
                view[k] = view[k].astype(object)

        table_list.append({'name': name, 'table': view})

    proto = GenericFeatureStatisticsGenerator().ProtoFromDataFrames(table_list)
    proto_str = base64.b64encode(proto.SerializeToString()).decode("utf-8")
    return HTML(FACETS_OVERVIEW_TEMPLATE.format(elem_id=elem_id, proto_str=proto_str))
