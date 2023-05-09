import math
import numpy as np
import matplotlib.pyplot as plt

class WeldingSimulation:
    def __init__(self, trigger):
        self.trigger = trigger
        self.variable_values = self.define_variables()
        self.variable_labels, self.unit_labels = self.define_labels()
        self.h_dict, self.x_axis, self.y_axis = self.initialize_h_dict()
        self.X, self.Y = self.create_grid()
        self.h_values = self.assign_variable_values()
        self.Z = self.calculate_h()

    def define_variables(self):
        return {
            "x1": np.linspace(0, 800, 200),
            "x2": np.linspace(-6, 6, 200),
            "x3": np.linspace(0, 7, 200),
            "x4": np.linspace(0, 2000, 200)
        }

    def define_labels(self):
        variable_labels = {
            "x1": "welding speed",
            "x2": "head position",
            "x3": "material thickness",
            "x4": "laser power"
        }

        unit_labels = {
            "x1": "mm/sec",
            "x2": "mm",
            "x3": "mm",
            "x4": "W"
        }

        return variable_labels, unit_labels

    def h(self, x1, x2, x3, x4):
        # welding_speedの関数
        lambda_1 = 0.0045
        g_x1 =  np.exp(-lambda_1 * abs(x1))

        # head_positionの関数
        mu = 0
        sigma = 2
        f_x2 = (1 / math.sqrt(2 * math.pi * sigma**2)) * np.exp(-((x2 - mu)**2) / (2 * sigma**2))

        # material_thicknessの関数
        lambda_3 = 1.0
        C = 0.5
        s_x3 = C + (1 - C) * np.exp(-lambda_3 * x3)

        # laser_powerの関数
        alpha = 1.0
        l_x4 = 1 + alpha * (x4 / 100)

        return f_x2 * g_x1 * s_x3 * l_x4

    def initialize_h_dict(self):
        # h_dict を初期化
        h_dict = {}
        
        # トリガーのキーを反復処理
        for key in self.trigger.keys():
            # x_var が指定された場合、x_axis と h_dict を設定
            if self.trigger[key] == "x_var":
                x_axis = (key, self.variable_values[key])
                h_dict[key] = self.variable_values[key]
            # y_var が指定された場合、y_axis と h_dict を設定
            elif self.trigger[key] == "y_var":
                y_axis = (key, self.variable_values[key])
                h_dict[key] = self.variable_values[key]
            # それ以外の場合、h_dict にトリガーの値を設定
            else:
                h_dict[key] = self.trigger[key]
        
        # h_dict, x_axis, y_axis を返す
        return h_dict, x_axis, y_axis

    def create_grid(self):
        X, Y = np.meshgrid(self.x_axis[1], self.y_axis[1])
        return X, Y

    def assign_variable_values(self):
        # 変数を初期化
        x1 = x2 = x3 = x4 = None

        # x_axisに対応する変数にXの値を割り当てる
        if self.x_axis[0] == "x1":
            x1 = self.X
        elif self.x_axis[0] == "x2":
            x2 = self.X
        elif self.x_axis[0] == "x3":
            x3 = self.X
        else:
            x4 = self.X

        # y_axisに対応する変数にYの値を割り当てる
        if self.y_axis[0] == "x1":
            x1 = self.Y
        elif self.y_axis[0] == "x2":
            x2 = self.Y
        elif self.y_axis[0] == "x3":
            x3 = self.Y
        else:
            x4 = self.Y

        # 割り当てられていない変数にtriggerの値を割り当てる
        if x1 is None:
            x1 = self.trigger["x1"]
        elif x2 is None:
            x2 = self.trigger["x2"]
        elif x3 is None:
            x3 = self.trigger["x3"]
        else:
            x4 = self.trigger["x4"]

        # 再度、割り当てられていない変数にtriggerの値を割り当てる
        if x1 is None:
            x1 = self.trigger["x1"]
        elif x2 is None:
            x2 = self.trigger["x2"]
        elif x3 is None:
            x3 = self.trigger["x3"]
        else:
            x4 = self.trigger["x4"]

        # h関数に渡す変数のリストを作成
        h_values = [x1, x2, x3, x4]
        return h_values

    def calculate_h(self):
        return self.h(self.h_values[0], self.h_values[1], self.h_values[2], self.h_values[3])

    def get_figure(self):
        # グラフのフィギュアを作成
        figure = plt.figure()
        # X, Y, Z のデータを使ってカラーメッシュを描画
        plt.pcolormesh(self.X, self.Y, self.Z, cmap='jet', vmax=1.0)
        # カラーバーを追加し、ラベルを設定
        plt.colorbar(label='Amplitude')
        # グリッドを表示
        plt.grid()

        # x軸とy軸の変数名を取得
        keys_with_x_var = [key for key, value in self.trigger.items() if value == "x_var"][0]
        keys_with_y_var = [key for key, value in self.trigger.items() if value == "y_var"][0]
        # x軸とy軸以外の変数名を取得
        keys_with_not_xy_var = [key for key, value in self.trigger.items() if value not in ["x_var", "y_var"]]

        # x軸のラベルを設定
        plt.xlabel(f"{self.variable_labels[keys_with_x_var]} [{self.unit_labels[keys_with_x_var]}]")
        # y軸のラベルを設定
        plt.ylabel(f"{self.variable_labels[keys_with_y_var]} [{self.unit_labels[keys_with_y_var]}]")

        # グラフのタイトルを設定
        plt.title(f"{self.variable_labels[keys_with_not_xy_var[0]]}: {self.trigger[keys_with_not_xy_var[0]]} [{self.unit_labels[keys_with_not_xy_var[0]]}], {self.variable_labels[keys_with_not_xy_var[1]]}: {self.trigger[keys_with_not_xy_var[1]]} [{self.unit_labels[keys_with_not_xy_var[1]]}]")

        # グラフを表示
        # plt.show()

        return figure

if __name__ == "__main__":
    trigger1 = {
        "x1": 500,
        "x2": "y_var",
        "x3": 1.0,
        "x4": "x_var"
    }

    welding_simulation = WeldingSimulation(trigger1)
    welding_simulation.get_figure()
