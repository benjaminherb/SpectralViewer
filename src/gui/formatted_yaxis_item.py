import pyqtgraph as pg

class FormattedYAxisItem(pg.AxisItem):
    """
    a custom class to define formatting for the y axis
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        return [f'{v:.2f}' for v in values]
