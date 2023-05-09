# gui.py
import tkinter as tk
from tkinter import ttk
from welding_simulation import WeldingSimulation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class WeldingSimulationGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Welding Simulation")
        self.geometry("800x600")

        # スピンボックスの設定
        self.create_spinboxes()

        # Calculationボタンの設定
        self.calc_button = ttk.Button(self, text="Calculation", command=self.calculate_and_plot)
        self.calc_button.grid(row=2, column=0, padx=10, pady=10, columnspan=4)

        # グラフ表示用キャンバスの設定
        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.grid(row=3, column=0, padx=10, pady=10, columnspan=4)

        # Exitボタンの設定
        self.exit_button = ttk.Button(self, text="EXIT", command=self.destroy)
        self.exit_button.grid(row=4, column=1, padx=10, pady=10, columnspan=2)

        # デフォルト値でグラフを表示
        self.calculate_and_plot()

    def create_spinboxes(self):
        # スピンボックスとラベルを作成
        self.spinboxes = []
        self.labels = [
            "welding speed (mm/sec)",
            "head position (mm)",
            "material thickness (mm)",
            "laser power (W)"
        ]

        self.var = [tk.StringVar(), tk.StringVar(), tk.DoubleVar(), tk.DoubleVar()]
        print("ok?")
        self.var[0].set("x_var")
        self.var[1].set("y_var")
        self.var[2].set(1.0)
        self.var[3].set(1000)

        configs = [
            {"from_": 0, "to": 800, "increment": 10},
            {"from_": -6, "to": 6, "increment": 0.1},
            {"from_": 0, "to": 7, "increment": 0.1},
            {"from_": 0, "to": 2000, "increment": 10}
        ]

        for i, config in enumerate(configs):
            label = ttk.Label(self, text=self.labels[i])
            spinbox = ttk.Spinbox(self, from_=config["from_"], to=config["to"], increment=config["increment"], textvariable=self.var[i])

            row, column = divmod(i, 2)
            label.grid(row=row, column=2 * column, padx=10, pady=10)
            spinbox.grid(row=row, column=2 * column + 1, padx=10, pady=10)
            self.spinboxes.append(spinbox)

    def calculate_and_plot(self):
        trigger = {
            "x1": str(self.var[0].get()),
            "x2": str(self.var[1].get()),
            "x3": str(self.var[2].get()),
            "x4": str(self.var[3].get())
        }

        # triggerの要素をひとつずつ取り出して、floatに変換可能なものは、変換する
        for key, value_str in trigger.items():
            try:
                value = float(value_str)
            except ValueError:
                value = value_str
            trigger[key] = value

        print(trigger)

        welding_simulation = WeldingSimulation(trigger)
        figure = welding_simulation.get_figure()

        # 以前のグラフを削除
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        # グラフをキャンバスに表示
        self.canvas = FigureCanvasTkAgg(figure, self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 新しいグラフを追加
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = WeldingSimulationGUI()
    app.mainloop()
