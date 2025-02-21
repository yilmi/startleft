from typing import Optional

from shapely.geometry import Point
from vsdx import Shape

from sl_util.sl_util.injection import register
from slp_visio.slp_visio.load.objects.diagram_objects import DiagramConnector
from slp_visio.slp_visio.load.representation.simple_component_representer import SimpleComponentRepresenter
from slp_visio.slp_visio.load.strategies.connector.create_connector_strategy import CreateConnectorStrategy, \
    CreateConnectorStrategyContainer


@register(CreateConnectorStrategyContainer.visio_strategies)
class CreateConnectorByLineCoordinates(CreateConnectorStrategy):
    """
    Strategy to create a connector from the shape begin and end coordinates

    We search a component shape that touch the beginning line coordinates of the given shape connector
    We search a component shape that touch the ending line coordinates of the given shape connector
    If we find both shapes at the end and at the beginning of the line, we create the connector
    """

    def __init__(self):
        self.tolerance = 0.09
        self.representer: SimpleComponentRepresenter() = SimpleComponentRepresenter()

    def create_connector(self, shape: Shape, components=None) -> Optional[DiagramConnector]:
        if not shape.begin_x or not shape.begin_y or not shape.end_x or not shape.end_y:
            return None
        begin_line = Point(shape.begin_x, shape.begin_y)
        end_line = Point(shape.end_x, shape.end_y)
        if not begin_line or not end_line:
            return None

        if not components:
            return None
        origin = self.__match_component(begin_line, components)
        target = self.__match_component(end_line, components)

        if not origin or not target:
            return None

        return DiagramConnector(shape.ID, origin, target, name=shape.text)

    def __match_component(self, point, components):
        for component in components:
            polygon = self.representer.build_representation(component)
            distance = polygon.exterior.distance(point)
            if round(distance, 2) <= self.tolerance:
                return component.ID
