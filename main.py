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
    parser.add_argument('--port', '-p', type=int, default=8521)

    args = parser.parse_args()  # 从命令行读取参数
    print("Running with width {}, height {}, interval {}, frames {}".format(args.width, args.height, args.interval,
                                                                            args.steps))

    params = {
        "width": args.width,
        "height": args.height,
    }

    canvas_element = CanvasGrid(agent_portrayal, args.width, args.height, args.width * 10, args.height * 10)
    temperature_chart = ChartModule([
        {"Label": "Temperature", "Color": "Red"}
    ], data_collector_name='datacollector')
    dandelion_chart = ChartModule([
        {"Label": "All Dandelions", "Color": "Green"},
    ], data_collector_name='datacollector')
    mature_dandelion_chart = ChartModule([
        {"Label": "Mature Dandelions", "Color": "Black"},
    ], data_collector_name='datacollector')
    distance_chart = ChartModule([
        {"Label": "Distance", "Color": "Blue"},
    ], data_collector_name='datacollector')

    server = ModularServer(
        Paradise,
        [canvas_element, temperature_chart, dandelion_chart, mature_dandelion_chart, distance_chart],
        "Dandelion Spread Simulation",
        params,
    )

    server.launch(open_browser=True, port=args.port)


if __name__ == '__main__':
    main()
