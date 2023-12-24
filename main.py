import argparse

from mesa_viz_tornado.ModularVisualization import ModularServer
from mesa_viz_tornado.modules import CanvasGrid, ChartModule

from paradise import Paradise


def agent_portrayal(agent):
    return {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "Color": "blue" if agent.is_mature() else "green",
        "r": 0.5,
    }


def mature_agents(model):
    """成熟的蒲公英数量"""
    return model.plant_count()


def temperature(model):
    return model.env.current_temperature


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, default=100)
    parser.add_argument('--height', type=int, default=100)
    parser.add_argument('--interval', type=int, default=500)
    parser.add_argument('--steps', type=int, default=100)

    args = parser.parse_args()  # 从命令行读取参数
    print("Running with width {}, height {}, interval {}, frames {}".format(args.width, args.height, args.interval,
                                                                            args.steps))

    params = {
        "width": args.width,
        "height": args.height,
    }

    canvas_element = CanvasGrid(agent_portrayal, args.width, args.height, 1024, 1024)
    chart = ChartModule([
        {"Label": "Mature", "Color": "Black"},
        {"Label": "Temperature", "Color": "Red"},
        {"Label": "Lifespan", "Color": "Blue"}
    ], data_collector_name='datacollector')

    server = ModularServer(
        Paradise,
        [canvas_element, chart],
        "Dandelion Spread Simulation",
        params,
    )

    server.launch(open_browser=True)


if __name__ == '__main__':
    main()
