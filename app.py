import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Registro de equipo - Medtronic")
        self.geometry("500x800")
        self.resizable(True, True)
        self.minsize(500, 700)
        self.configure(fg_color="white")


        self.correos_ingenieros = {
            "Nicolle Riaño": "nicolle.n.riano@medtronic.com"
        }

        self.tipo_operacion = None
        self.frames_equipos = []
        self.cliente_entry = None
        self.ingeniero_combo = None
        self.entry_movimiento_general = None
        self.botones_frame = None

        self.mostrar_pantalla_inicio()

    def mostrar_pantalla_inicio(self):
 
        self.frame_inicio = ctk.CTkFrame(self, fg_color="white")
        self.frame_inicio.pack(expand=True)

    # Logo dentro del frame_inicio
        try:
            logo_img = Image.open("logo_medtronic.png").resize((200, 200))
            self.logo_inicio = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(self.frame_inicio, image=self.logo_inicio, bg="white")
            logo_label.pack(pady=(20, 10))  # Ajusta los márgenes si lo deseas
        except Exception as e:
            print(f"No se pudo cargar el logo de inicio: {e}")

        ctk.CTkLabel(self.frame_inicio, text="¿Qué deseas registrar?", font=ctk.CTkFont(size=20)).pack(pady=20)
        ctk.CTkButton(self.frame_inicio, text="Ingreso", width=200, command=lambda: self.iniciar_app("Ingreso"), fg_color="#003366", hover_color="#002244").pack(pady=10)
        ctk.CTkButton(self.frame_inicio, text="Salida", width=200, command=lambda: self.iniciar_app("Salida"), fg_color="#003366", hover_color="#002244").pack(pady=10)

    def iniciar_app(self, tipo):
        self.tipo_operacion = tipo
        self.frame_inicio.destroy()

        self.main_frame = ctk.CTkScrollableFrame(self, label_text="", width=480, height=700, fg_color="white")
        self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        encabezado_frame = tk.Frame(self.main_frame, bg="#003366", height=60)
        encabezado_frame.pack(fill="x", pady=(10, 10), padx=10)

        # Botón de retroceso
        boton_retroceso = ctk.CTkButton(
            encabezado_frame,
            text="←",
            width=30,
            height=25,
            fg_color="#003366",
            hover_color="#002244",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.reiniciar_interfaz
        )
        boton_retroceso.pack(side="left", padx=(10, 5), pady=5)

        try:
            logo = Image.open("logo_medtronic.png").resize((120, 50))
            self.logo_header = ImageTk.PhotoImage(logo)
            logo_label = tk.Label(encabezado_frame, image=self.logo_header, bg="#003366")
            logo_label.pack(side="left", padx=(10, 15), pady=5)
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")

        texto_encabezado = tk.Frame(encabezado_frame, bg="#003366")
        texto_encabezado.pack(side="left", fill="both", expand=True)

        tk.Label(texto_encabezado, text="Información confidencial — Uso exclusivo de Medtronic", font=("Arial", 10, "bold"), fg="white", bg="#003366").pack(anchor="center")
        tk.Label(texto_encabezado, text=f"{self.tipo_operacion} - Registro de equipos", font=("Arial", 12, "bold"), fg="white", bg="#003366").pack(anchor="center")

        cliente_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        cliente_frame.pack(pady=(5, 5), fill="x", padx=10)
        ctk.CTkLabel(cliente_frame, text="Cliente:", width=70).pack(side="left", padx=(0, 5))
        self.cliente_entry = ctk.CTkEntry(cliente_frame)
        self.cliente_entry.pack(side="left", fill="x", expand=True)

        ingeniero_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        ingeniero_frame.pack(pady=(0, 5), fill="x", padx=10)
        ctk.CTkLabel(ingeniero_frame, text="Ingeniero:", width=100).pack(side="left", padx=(0, 5))
        self.ingeniero_combo = ctk.CTkComboBox(ingeniero_frame, values=list(self.correos_ingenieros.keys()))
        self.ingeniero_combo.pack(side="left", fill="x", expand=True)

        movimiento_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        movimiento_frame.pack(pady=(5, 10), fill="x", padx=10)
        ctk.CTkLabel(movimiento_frame, text="Movimiento / Delivery:", width=160).pack(side="left", padx=(0, 5))
        self.entry_movimiento_general = ctk.CTkEntry(movimiento_frame, width=160)
        self.entry_movimiento_general.pack(side="left")

        self.botones_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_add_equipo = ctk.CTkButton(self.botones_frame, text="Agregar otro equipo", command=self.agregar_equipo, fg_color="#003366", hover_color="#002244")
        self.btn_add_equipo.pack(side="left", expand=True, padx=(0, 5))
        self.btn_enviar = ctk.CTkButton(self.botones_frame, text="Enviar", command=self.enviar_reporte, fg_color="#003366", hover_color="#002244")
        self.btn_enviar.pack(side="left", expand=True, padx=(5, 0))

        self.agregar_equipo()

    def agregar_equipo(self):
        num_equipo = len(self.frames_equipos) + 1
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame.pack(pady=10, fill="x", padx=10)

        self.frames_equipos.append({
            "frame": frame,
            "fotos": [],
            "check_vars": [],
            "llegada_vars": [],
            "otro_var": tk.StringVar()
        })

        fila_info_frame = ctk.CTkFrame(frame, fg_color="transparent")
        fila_info_frame.pack(pady=(5, 2), fill="x")

        ctk.CTkLabel(fila_info_frame, text=f"Equipo {num_equipo}:", width=80).grid(row=0, column=0, padx=(0, 5), sticky="w")
        combo_equipo = ctk.CTkComboBox(fila_info_frame, values=["WEM", "ForceTriad", "FX", "PB840", "PB980", "BIS VISTA", "CONSOLA DE CAMARA"], width=110)
        combo_equipo.grid(row=0, column=1, padx=(0, 5))

        ctk.CTkLabel(fila_info_frame, text="Serial:", width=45).grid(row=0, column=2, padx=(0, 5), sticky="w")
        entry_serial = ctk.CTkEntry(fila_info_frame, width=160)
        entry_serial.grid(row=0, column=3, padx=(0, 5))

        # Botón Eliminar (solo si es un equipo adicional)
        if num_equipo > 1:
            eliminar_btn = ctk.CTkButton(fila_info_frame, text="✖", width=30, height=25, fg_color="#8B0000", hover_color="#5A0000", font=ctk.CTkFont(size=12),
                                         command=lambda f=frame: self.eliminar_equipo(f))
            eliminar_btn.grid(row=0, column=4, padx=(5, 0), sticky="e")

        ctk.CTkLabel(frame, text="Observaciones físicas:", anchor="w").pack(pady=(5, 5), fill="x")
        observaciones = ["Carcasa rayada", "Golpes visibles", "Pantalla rayada", "Pieza rotos", "Cable dañado", "otro"]
        checkbox_frame = ctk.CTkFrame(frame, fg_color="transparent")
        checkbox_frame.pack(pady=(2, 5), fill="x")

        check_vars = []
        otro_var = tk.BooleanVar()
        otro_entry_var = self.frames_equipos[-1]["otro_var"]

        for i, obs in enumerate(observaciones):
            var = tk.BooleanVar()
            if obs == "otro":
                otro_row = ctk.CTkFrame(checkbox_frame, fg_color="transparent")
                otro_row.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="w")

                chk = ctk.CTkCheckBox(otro_row, text="otro", variable=otro_var)
                chk.pack(side="left")

                label_cual = ctk.CTkLabel(otro_row, text="¿Cuál?")
                label_cual.pack(side="left", padx=(10, 0))
                label_cual.pack_forget()

                entry = ctk.CTkEntry(otro_row, textvariable=otro_entry_var, width=120)
                entry.pack(side="left", padx=(5, 0))
                entry.pack_forget()

                def toggle_otro():
                    if otro_var.get():
                        label_cual.pack(side="left", padx=(10, 0))
                        entry.pack(side="left", padx=(5, 0))
                        entry.configure(state="normal")
                    else:
                        label_cual.pack_forget()
                        entry.pack_forget()
                        entry.configure(state="disabled")

                chk.configure(command=toggle_otro)
                check_vars.append((obs, otro_var))
            else:
                chk = ctk.CTkCheckBox(checkbox_frame, text=obs, variable=var)
                chk.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="w")
                check_vars.append((obs, var))
        self.frames_equipos[-1]["check_vars"] = check_vars

        llegada_label = "¿Cómo llegó el equipo?" if self.tipo_operacion == "Ingreso" else "¿Cómo sale el equipo?"
        ctk.CTkLabel(frame, text=llegada_label, anchor="w").pack(pady=(5, 5), fill="x")
        formas_llegada = ["Caja original", "Caja cartón", "Huacal", "Maletín", "Contenedor"]
        llegada_frame = ctk.CTkFrame(frame, fg_color="transparent")
        llegada_frame.pack(pady=(2, 5), fill="x")

        llegada_vars = []
        for i, forma in enumerate(formas_llegada):
            var = tk.BooleanVar()
            chk = ctk.CTkCheckBox(llegada_frame, text=forma, variable=var)
            chk.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="w")
            llegada_vars.append((forma, var))
        self.frames_equipos[-1]["llegada_vars"] = llegada_vars

        ctk.CTkLabel(frame, text="Accesorios:", anchor="w").pack(pady=(5, 2), fill="x")
        entry_extra = ctk.CTkEntry(frame)
        entry_extra.pack(fill="x")

        ctk.CTkLabel(frame, text="Fotos del equipo:", anchor="w").pack(pady=(5, 2), fill="x")
        fotos_frame = ctk.CTkFrame(frame, fg_color="transparent")
        fotos_frame.pack(fill="x")

        label_fotos = ctk.CTkLabel(fotos_frame, text="0 fotos seleccionadas", anchor="w")
        label_fotos.pack(side="left", padx=10)

        def subir_fotos():
            archivos = filedialog.askopenfilenames(title="Selecciona las fotos", filetypes=[("Imágenes", "*.png *.jpg *.jpeg")])
            self.frames_equipos[-1]["fotos"] = list(archivos)
            label_fotos.configure(text=f"{len(archivos)} fotos seleccionadas")

        ctk.CTkButton(fotos_frame, text="Seleccionar Fotos", command=subir_fotos, fg_color="#003366", hover_color="#002244").pack(side="left", padx=(0, 10))

        self.frames_equipos[-1].update({
            "combo_equipo": combo_equipo,
            "entry_serial": entry_serial,
            "entry_extra": entry_extra,
            "label_fotos": label_fotos
        })

        self.botones_frame.pack_forget()
        self.botones_frame.pack(pady=(10, 20), fill="x", padx=10)

    def eliminar_equipo(self, frame_a_eliminar):
        for idx, datos in enumerate(self.frames_equipos):
            if datos["frame"] == frame_a_eliminar:
                datos["frame"].destroy()
                self.frames_equipos.pop(idx)
                break

        for i, datos in enumerate(self.frames_equipos):
            frame = datos["frame"]
            for widget in frame.winfo_children():
                if isinstance(widget, ctk.CTkFrame):
                    for subwidget in widget.winfo_children():
                        if isinstance(subwidget, ctk.CTkLabel) and subwidget.cget("text").startswith("Equipo"):
                            subwidget.configure(text=f"Equipo {i + 1}:")

    def enviar_reporte(self):
        ingeniero = self.ingeniero_combo.get()
        correo_destino = self.correos_ingenieros.get(ingeniero)
        correo_fijo = "mejiah5@medtronic.com"  # ← PON AQUÍ EL CORREO FIJO

        if not correo_destino:
            messagebox.showerror("Error", "Correo del ingeniero no encontrado.")
            return

        for idx, datos in enumerate(self.frames_equipos):
            if len(datos["fotos"]) < 4:
                messagebox.showerror("Error de validación", f"El equipo {idx + 1} debe tener al menos 4 fotos seleccionadas.")
                return

        try:
            from_email = "rianonicolle1101@gmail.com"
            password = "pmfb qjwu rnyc bojy"
            smtp_server = "smtp.gmail.com"
            smtp_port = 587

            msg = MIMEMultipart('related')
            msg["From"] = from_email
            msg["To"] = f"{correo_destino}, {correo_fijo}"
            msg["Subject"] = f"{self.tipo_operacion} ST - Movimiento/Delivery: {self.entry_movimiento_general.get()}"

            cuerpo_html = f"""<html><body>
            <p><b>{'Ingreso a Servicio Técnico' if self.tipo_operacion == 'Ingreso' else 'Salida de Servicio Técnico'}</b></p>
            <p><b>Cliente:</b> {self.cliente_entry.get()}<br>
            <b>Ingeniero:</b> {ingeniero}<br>
            <b>Movimiento / Delivery:</b> {self.entry_movimiento_general.get()}</p>
            <p><b>Equipos registrados:</b></p>
            """

            imagenes = []
            cid_counter = 0

            for idx, datos in enumerate(self.frames_equipos):
                observaciones = [nombre for nombre, var in datos['check_vars'] if var.get()]
                if datos['otro_var'].get():
                    observaciones.append(datos['otro_var'].get())

                llegada = [forma for forma, var in datos['llegada_vars'] if var.get()]

                cuerpo_html += f"""
                <p><b>Equipo {idx + 1}:</b><br>
                <b>- Tipo:</b> {datos['combo_equipo'].get()}<br>
                <b>- Serial:</b> {datos['entry_serial'].get()}<br>
                <b>- Accesorios:</b> {datos['entry_extra'].get()}<br>
                <b>- Observaciones físicas:</b> {', '.join(observaciones) if observaciones else 'Ninguna'}<br>
                <b>- Forma de {'llegada' if self.tipo_operacion == 'Ingreso' else 'salida'}:</b> {', '.join(llegada) if llegada else 'No especificada'}<br>
                <b>- Número de fotos:</b> {len(datos['fotos'])}</p>
                """

                for foto in datos["fotos"]:
                    cid = f"image{cid_counter}"
                    cid_counter += 1
                    cuerpo_html += f'<img src="cid:{cid}" style="max-width:400px;"><br>'

                    with open(foto, 'rb') as f:
                        img = MIMEImage(f.read())
                        img.add_header('Content-ID', f'<{cid}>')
                        img.add_header('Content-Disposition', 'inline', filename=foto.split('/')[-1])
                        imagenes.append(img)

                cuerpo_html += "<br>"

            cuerpo_html += """
             <p style="font-style: italic; color: #555; font-size: 12px; margin-top: 30px; border-top: 1px solid #ccc; padding-top: 10px;">
             Este mensaje ha sido generado automáticamente por el Departamento de Servicio Técnico de <b>Medtronic</b>.
              </p></body></html>
             """


            msg.attach(MIMEText(cuerpo_html, "html"))

            for img in imagenes:
                msg.attach(img)

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
            server.quit()

            messagebox.showinfo("Éxito", "Correo enviado correctamente.")

            # Reiniciar toda la interfaz
            self.reiniciar_interfaz()


        except Exception as e:
            print("Error al enviar el correo:", str(e))
            messagebox.showerror("Error", f"No se pudo enviar el correo: {str(e)}")


    def reiniciar_interfaz(self):
        # Elimina cualquier frame visible
        for widget in self.winfo_children():
            if isinstance(widget, (ctk.CTkFrame, tk.Frame, tk.Label)):
                widget.destroy()

        # Restablece los datos
        self.frames_equipos.clear()
        self.tipo_operacion = None

        # Vuelve a mostrar la pantalla inicial
        self.mostrar_pantalla_inicio()

if __name__ == "__main__":
    app = App()
    app.mainloop()











