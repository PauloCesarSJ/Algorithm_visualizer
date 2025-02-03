import tkinter as tk
from tkinter import messagebox

class TreeNode:
#calsse que define oque e o nó da arvore 
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None
    
    def insert(self, value):
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)
    
    def delete(self, value):
        self.root = self._delete_recursive(self.root, value)
    
    def _delete_recursive(self, node, value):
        if node is None:
            return None
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            min_larger_node = self._get_min(node.right)
            node.value = min_larger_node.value
            node.right = self._delete_recursive(node.right, min_larger_node.value)
        return node
    
    def _get_min(self, node):
        while node.left is not None:
            node = node.left
        return node
    
    def balance(self):
        nodes = self._in_order_traversal()
        self.root = self._build_balanced_tree(nodes)
    
    def _in_order_traversal(self):
        nodes = []
        self._traverse_in_order(self.root, nodes)
        return nodes
    
    def _traverse_in_order(self, node, result):
        if node is not None:
            self._traverse_in_order(node.left, result)
            result.append(node.value)
            self._traverse_in_order(node.right, result)
    
    def _build_balanced_tree(self, nodes):
        if not nodes:
            return None
        
        mid = len(nodes) // 2
        node = TreeNode(nodes[mid])
        node.left = self._build_balanced_tree(nodes[:mid])
        node.right = self._build_balanced_tree(nodes[mid+1:])
        return node
    
    def is_balanced(self):
        return self._check_balance(self.root) != -1
    
    def _check_balance(self, node):
        if node is None:
            return 0
        
        left_height = self._check_balance(node.left)
        if left_height == -1:
            return -1
        
        right_height = self._check_balance(node.right)
        if right_height == -1:
            return -1
        
        if abs(left_height - right_height) > 1:
            return -1
        
        return max(left_height, right_height) + 1

class TreeVisualizer:
#classe de vizualização de arvore 
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Árvore Binária Balanceada")
        self.window.geometry("900x600")
        self.canvas = tk.Canvas(self.window, bg="#f0f0f0")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.tree = BinaryTree()
        
        self.controls_frame = tk.Frame(self.window, bg="#e0e0e0")
        self.controls_frame.pack(fill=tk.X)
        
        # Botões com cores RGB
        self.add_btn = tk.Button(
            self.controls_frame,
            text="Adicionar Nó",
            command=self.add_node,
            bg="#FF0000",  # Vermelho
            fg="white",
            font=("Arial", 12)
        )
        self.add_btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.remove_btn = tk.Button(
            self.controls_frame,
            text="Remover Nó",
            command=self.remove_node,
            bg="#00FF00",  # Verde
            fg="black",
            font=("Arial", 12)
        )
        self.remove_btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.balance_btn = tk.Button(
            self.controls_frame,
            text="Balancear Árvore",
            command=self.balance_tree,
            bg="#0000FF",  # Azul
            fg="white",
            font=("Arial", 12)
        )
        self.balance_btn.pack(side=tk.LEFT, padx=10, pady=5)

        self.entry = tk.Entry(self.controls_frame, width=20)
        self.entry.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Alerta de balanceamento
        self.balance_alert = tk.Label(
            self.controls_frame,
            text="Desbalanceada",
            bg="#FF0000",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=10
        )
        self.balance_alert.pack(side=tk.RIGHT, padx=10)
        
        self.window.bind("<Return>", self.add_node)
        self.window.bind("<BackSpace>", self.remove_node)
    
    def add_node(self, event=None):
        value = self.entry.get()
        try:
            num_value = int(value)
            self.tree.insert(num_value)
            self.entry.delete(0, tk.END)
            self.update_balance_status()
            self.animate()
        except ValueError:
            messagebox.showerror("Erro", "Por favor insira um número inteiro válido.")
    
    def remove_node(self, event=None):
        value = self.entry.get()
        try:
            num_value = int(value)
            self.tree.delete(num_value)
            self.entry.delete(0, tk.END)
            self.update_balance_status()
            self.animate()
        except ValueError:
            messagebox.showerror("Erro", "Por favor insira um número inteiro válido.")
    
    def balance_tree(self):
        self.tree.balance()
        self.update_balance_status()
        self.animate()
    
    def update_balance_status(self):
        if self.tree.is_balanced():
            self.balance_alert.config(text="Balanceada", bg="#00FF00")
        else:
            self.balance_alert.config(text="Desbalanceada", bg="#FF0000")
    
    def animate(self):
        self.canvas.delete("all")
        if self.tree.root:
            self._draw_tree(self.tree.root, 450, 50, 200)
    
    def _draw_tree(self, node, x, y, dx):
        if node.left:
            self.canvas.create_line(x, y, x - dx, y + 80, fill="black", width=2)
            self._draw_tree(node.left, x - dx, y + 80, dx // 2)
        if node.right:
            self.canvas.create_line(x, y, x + dx, y + 80, fill="black", width=2)
            self._draw_tree(node.right, x + dx, y + 80, dx // 2)
        
        self.canvas.create_oval(x - 25, y - 25, x + 25, y + 25, fill="#3498db", outline="black", width=2)
        self.canvas.create_text(x, y, text=str(node.value), font=("Arial", 14, "bold"), fill="white")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = TreeVisualizer()
    app.run()