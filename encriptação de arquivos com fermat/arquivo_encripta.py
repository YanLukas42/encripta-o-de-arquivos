import os
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import filedialog, messagebox



def generate_key():
    """Gera uma chave de criptografia e salva no disco."""
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    messagebox.showinfo("Chave Gerada", "Chave de criptografia salva como 'key.key'.")
    return key

def load_key():
    """Carrega a chave de criptografia do arquivo 'key.key'."""
    try:
        with open("key.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo 'key.key' não encontrado. Gere uma chave primeiro.")
        return None


def encrypt_file(filepath, key):
    """Criptografa um arquivo usando a chave fornecida."""
    try:
        with open(filepath, "rb") as file:
            data = file.read()
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data)

        with open(filepath + ".enc", "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)

        messagebox.showinfo("Sucesso", f"Arquivo criptografado: {filepath}.enc")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao criptografar: {e}")

def decrypt_file(filepath, key):
    """Descriptografa um arquivo criptografado usando a chave fornecida."""
    try:
        with open(filepath, "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)

        original_filepath = filepath.replace(".enc", "")
        with open(original_filepath, "wb") as decrypted_file:
            decrypted_file.write(decrypted_data)

        messagebox.showinfo("Sucesso", f"Arquivo descriptografado: {original_filepath}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao descriptografar: {e}")



def select_file(operation):
    """Permite ao usuário selecionar um arquivo para criptografia/descriptografia."""
    filepath = filedialog.askopenfilename()
    if filepath:
        key = load_key()
        if key:
            if operation == "encrypt":
                encrypt_file(filepath, key)
            elif operation == "decrypt":
                decrypt_file(filepath, key)

def create_gui():
    """Cria a interface gráfica para o programa."""
    root = tk.Tk()
    root.title("Ferramenta de Criptografia de Arquivos")

    tk.Label(root, text="Ferramenta de Criptografia", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="Gerar Chave", command=generate_key, bg="green", fg="white", width=20).pack(pady=5)
    tk.Button(root, text="Criptografar Arquivo", command=lambda: select_file("encrypt"), bg="blue", fg="white", width=20).pack(pady=5)
    tk.Button(root, text="Descriptografar Arquivo", command=lambda: select_file("decrypt"), bg="red", fg="white", width=20).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
