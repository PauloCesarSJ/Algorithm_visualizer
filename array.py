import tkinter as tk
from tkinter import ttk
import time

def draw_squares(data, canvas, positions):
    """Desenha todos os quadrados e números no canvas."""
    canvas.delete("all")  # Limpa o canvas
    square_size = 50  # Tamanho fixo para os quadrados
    
    for i, value in enumerate(data):
        x0, y0 = positions[i]
        x1 = x0 + square_size
        y1 = y0 + square_size
        # Desenhar o quadrado 
        canvas.create_rectangle(x0, y0, x1, y1, outline="black", tags=f"square_{i}")
        # Números 
        canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=str(value), fill="black", font=("Arial", 10), tags=f"text_{i}")
        canvas.create_text((x0 + x1)/2, (y0 + y1) / 1.7, text=str(i), fill="black", font=("Arial", 10), tags=f"text_{i}")
    canvas.update()

def animate_swap(canvas, idx1, idx2, positions):
    
    # Posição inicial de ambos os quadrados
    x1, y1 = positions[idx1]
    x2, y2 = positions[idx2]

    # Número de passos para a animação
    steps = 20
    dx = (x2 - x1) / steps  # Distância horizontal por passo
    dy = -30 / steps        # Distância vertical (subindo)

    for step in range(steps):
        # Mover ambos os quadrados em cada passo
        canvas.move(f"square_{idx1}", dx, dy)
        canvas.move(f"text_{idx1}", dx, dy)
        canvas.move(f"square_{idx2}", -dx, dy)
        canvas.move(f"text_{idx2}", -dx, dy)
        canvas.update()
        time.sleep(0.02)

    # Após a troca horizontal, descer para a nova posição
    for step in range(steps):
        canvas.move(f"square_{idx1}", 0, -dy)  # Desce
        canvas.move(f"text_{idx1}", 0, -dy)
        canvas.move(f"square_{idx2}", 0, -dy)  # Desce
        canvas.move(f"text_{idx2}", 0, -dy)
        canvas.update()
        time.sleep(0.02)
   

def bubble_sort(data, canvas):
    primeiroloop = False

    n = len(data)
    square_size = 50
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    offset_x = (canvas_width - n * square_size) // 2
    offset_y = (canvas_height - square_size) // 2

    # Inicializa as posições dos quadrados
    positions = [(offset_x + i * square_size, offset_y) for i in range(n)]
    draw_squares(data, canvas, positions)

    for i in range(n - 1):
        for j in range(n - i - 1):
            if data[j] > data[j + 1]:
                
                data[j], data[j + 1] = data[j + 1], data[j]
               
               
               
               
                #erro na animação
                if primeiroloop == True:
                  animate_swap(canvas, j , j+1 , positions)
                primeiroloop = True
                draw_squares(data, canvas, positions)

def main():
    root = tk.Tk()
    root.title("Visualizador de Algoritmos de Ordenação")
    root.geometry("800x600")
    
    canvas = tk.Canvas(root, bg="white", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    array = [2,56,5,45,9,54,2,]

    start_button = tk.Button(root, text="Ordenar", command=lambda: bubble_sort(array, canvas))
    start_button.pack(pady=10)


    entry = tk.Entry(root, width=20)
    entry.pack(pady=10)

    start_button = tk.Button(root, text="entrada", command=lambda: get_selection())
    start_button.pack(pady=10)

    def get_selection():
        novovalor = entry.get()
        int_num = int(novovalor)
        array.append(int_num)
        bubble_sort(array, canvas)

    def Get_removeIndice():
        novovalor = entry.get()
        int_num = int(novovalor)
        array.pop(int_num)
        bubble_sort(array,canvas)


    button = tk.Button(root, text="Remove", command=lambda: Get_removeIndice())
    button.pack(pady=10)


    root.mainloop()

if __name__ == "__main__":
    main()


 # type: ignore