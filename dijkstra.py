import tkinter as tk
from tkinter import messagebox, ttk
import math

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = {}
        self.optimal_path = []
    
    def add_node(self, x, y):
        self.nodes.append((x, y))
        self.calculate_distances()
    
    def calculate_distances(self):
        n = len(self.nodes)
        self.edges = {}
        for i in range(n):
            for j in range(n):
                if i != j:
                    dx = self.nodes[i][0] - self.nodes[j][0]
                    dy = self.nodes[i][1] - self.nodes[j][1]
                    distance = math.sqrt(dx**2 + dy**2)
                    self.edges[(i, j)] = distance
    
    def solve_tsp(self):
        n = len(self.nodes)
        if n < 3:
            return None
        
        # Algoritmo do vizinho mais próximo
        path = [0]
        unvisited = set(range(1, n))
        
        while unvisited:
            current = path[-1]
            nearest = min(unvisited, key=lambda x: self.edges[(current, x)])
            path.append(nearest)
            unvisited.remove(nearest)
        
        path.append(0)  # Retornar ao ponto inicial
        self.optimal_path = path
        return path

class TSPVisualizer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Caixeiro Viajante")
        self.window.geometry("1200x600")
        
        self.graph = Graph()
        
        # Configuração do layout principal
        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas para desenho
        self.canvas = tk.Canvas(self.main_frame, bg="#f0f0f0")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame para tabela e controles
        self.side_frame = tk.Frame(self.main_frame, width=300)
        self.side_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tabela de rotas
        self.route_table = ttk.Treeview(self.side_frame, columns=('Step', 'City'), show='headings')
        self.route_table.heading('Step', text='Ordem')
        self.route_table.heading('City', text='Cidade')
        self.route_table.column('Step', width=50, anchor='center')
        self.route_table.column('City', width=100, anchor='center')
        self.route_table.pack(pady=10, padx=5, fill=tk.BOTH, expand=True)
        
        # Controles
        self.controls_frame = tk.Frame(self.window, bg="#e0e0e0")
        self.controls_frame.pack(fill=tk.X)
        
        self.clear_btn = tk.Button(
            self.controls_frame,
            text="Limpar Tudo",
            command=self.clear_graph,
            bg="#FF0000",
            fg="white",
            font=("Arial", 12)
        )
        self.clear_btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.solve_btn = tk.Button(
            self.controls_frame,
            text="Resolver TSP",
            command=self.solve_tsp,
            bg="#00FF00",
            fg="black",
            font=("Arial", 12)
        )
        self.solve_btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.status_label = tk.Label(
            self.controls_frame,
            text="Adicione cidades clicando na tela",
            bg="#3498db",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=10
        )
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
        # Eventos
        self.canvas.bind("<Button-1>", self.add_node)
        self.window.bind("<Delete>", self.clear_graph)
    
    def add_node(self, event):
        x, y = event.x, event.y
        self.graph.add_node(x, y)
        self.update_display()
    
    def solve_tsp(self):
        if len(self.graph.nodes) < 3:
            messagebox.showerror("Erro", "Adicione pelo menos 3 cidades!")
            return
        
        self.graph.solve_tsp()
        self.update_route_table()
        self.update_display()
        self.status_label.config(text="Rota ótima encontrada!", bg="#00FF00")
    
    def clear_graph(self, event=None):
        self.graph = Graph()
        self.route_table.delete(*self.route_table.get_children())
        self.update_display()
        self.status_label.config(text="Adicione cidades clicando na tela", bg="#3498db")
    
    def update_route_table(self):
        self.route_table.delete(*self.route_table.get_children())
        for step, city in enumerate(self.graph.optimal_path):
            self.route_table.insert('', 'end', values=(step+1, city+1))
    
    def update_display(self):
        self.canvas.delete("all")
        self.draw_nodes()
        if len(self.graph.optimal_path) > 0:
            self.draw_path()
    
    def draw_nodes(self):
        for i, (x, y) in enumerate(self.graph.nodes):
            self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="#1f8c31", outline="black")
            self.canvas.create_text(x, y, text=str(i+1), font=("Arial", 20, "bold"), fill="black")
    
    def draw_path(self):
        path = self.graph.optimal_path
        for i in range(len(path)-1):
            start = self.graph.nodes[path[i]]
            end = self.graph.nodes[path[i+1]]
            self.canvas.create_line(start[0], start[1], end[0], end[1], 
                                  fill="#b02828", width=3, arrow=tk.LAST) 
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = TSPVisualizer()
    app.run()