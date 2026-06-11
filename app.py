"""
Computacao Grafica
  Aba 1 — Rasterizacao de Retas     (DDA e Bresenham 1o octante)
  Aba 2 — Transformacoes Geometricas (coord. homogeneas, poligono regular)
           Algoritmo de desenho: Bresenham generalizado (todos os octantes)
"""

import tkinter as tk
from tkinter import ttk, messagebox

from rasterizacao import dda, bresenham, bresenham_geral
from transformacoes import (
    identidade, mat_mult,
    aplicar_transformacao, poligono_regular,
    translacao, escala, rotacao, reflexao, cisalhamento,
)

CANVAS_W, CANVAS_H = 700, 500
CX, CY = CANVAS_W // 2, CANVAS_H // 2   # origem cartesiana no centro

# ---------------------------------------------------------------------------
# Atalhos de estilo
# ---------------------------------------------------------------------------
_BTN  = dict(relief="flat", cursor="hand2", font=("Arial", 9, "bold"))
_ENTR = dict(bg="#3c3c3c", fg="white", insertbackground="white",
             relief="flat", bd=3, width=8)
_LBL  = dict(bg="#2b2b2b", fg="#ccc")
_FRM  = dict(bg="#2b2b2b", fg="#aaa", font=("Arial", 9))


def _lframe(parent, text):
    return tk.LabelFrame(parent, text=text, **_FRM)


def _entry(parent, default, width=8):
    e = tk.Entry(parent, **{**_ENTR, "width": width})
    e.insert(0, default)
    return e


# ---------------------------------------------------------------------------
class App:
# ---------------------------------------------------------------------------

    def __init__(self, root):
        self.root = root
        root.title("Computacao Grafica")
        root.resizable(False, False)
        root.configure(bg="#2b2b2b")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook",     background="#2b2b2b", borderwidth=0)
        style.configure("TNotebook.Tab", background="#3c3c3c", foreground="white",
                        padding=[14, 5])
        style.map("TNotebook.Tab",       background=[("selected", "#4a4a4a")])

        nb = ttk.Notebook(root)
        nb.pack(fill="both", expand=True, padx=10, pady=10)

        tab_r = tk.Frame(nb, bg="#2b2b2b")
        nb.add(tab_r, text="  Rasterizacao de Retas  ")
        self._build_raster_tab(tab_r)

        tab_t = tk.Frame(nb, bg="#2b2b2b")
        nb.add(tab_t, text="  Transformacoes Geometricas  ")
        self._build_transf_tab(tab_t)

    # =========================================================
    #  ABA 1 — RASTERIZACAO DE RETAS
    # =========================================================

    def _build_raster_tab(self, parent):
        esq = tk.Frame(parent, bg="#2b2b2b")
        esq.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        dir_ = tk.Frame(parent, bg="#2b2b2b")
        dir_.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        self.canvas = tk.Canvas(dir_, width=CANVAS_W, height=CANVAS_H,
                                bg="black", highlightthickness=1,
                                highlightbackground="#555")
        self.canvas.pack()

        tk.Label(esq, text="Algoritmo de Reta",
                 font=("Arial", 12, "bold"),
                 bg="#2b2b2b", fg="white").pack(pady=(6, 4))

        frame_alg = _lframe(esq, "Algoritmo")
        frame_alg.pack(padx=8, pady=4, fill="x")
        self.alg = tk.StringVar(value="DDA")
        for txt, val in [("DDA", "DDA"), ("Bresenham (1 oitante)", "BRESENHAM")]:
            tk.Radiobutton(frame_alg, text=txt, variable=self.alg, value=val,
                           bg="#2b2b2b", fg="white", selectcolor="#444",
                           activebackground="#2b2b2b",
                           activeforeground="white").pack(anchor="w", padx=6)

        frame_p = _lframe(esq, "Pontos")
        frame_p.pack(padx=8, pady=4, fill="x")
        self.ent = {}
        for i, (lbl, default) in enumerate([("x1","0"),("y1","0"),
                                             ("x2","0"),("y2","0")]):
            tk.Label(frame_p, text=lbl+":", width=3, **_LBL).grid(
                row=i//2, column=(i%2)*2, padx=6, pady=4, sticky="e")
            e = _entry(frame_p, default)
            e.grid(row=i//2, column=(i%2)*2+1, padx=6, pady=4)
            self.ent[lbl] = e

        frame_btn = tk.Frame(esq, bg="#2b2b2b")
        frame_btn.pack(pady=10)
        tk.Button(frame_btn, text="Desenhar", command=self.desenhar,
                  width=12, bg="#4CAF50", fg="white", **_BTN).pack(side="left", padx=4)
        tk.Button(frame_btn, text="Limpar",   command=self.limpar,
                  width=10, bg="#555",    fg="white", **_BTN).pack(side="left", padx=4)

        frame_log = tk.Frame(esq, bg="#2b2b2b")
        frame_log.pack(fill="x", padx=8)
        self.log_box = tk.Text(frame_log, width=38, height=22,
                               bg="#1a1a1a", fg="#d4d4d4",
                               font=("Consolas", 8),
                               insertbackground="white", relief="flat", bd=4)
        sc = tk.Scrollbar(frame_log, command=self.log_box.yview)
        self.log_box.configure(yscrollcommand=sc.set)
        self.log_box.pack(side="left", fill="both")
        sc.pack(side="right", fill="y")

        self._draw_axes(self.canvas)

    def set_pixel(self, x, y, cor="white"):
        px = int(round(x)) + CX
        py = CY - int(round(y))
        self.canvas.create_rectangle(px, py, px+1, py+1, outline=cor, fill=cor)

    def limpar(self):
        self.canvas.delete("all")
        self._draw_axes(self.canvas)
        self.log_box.delete("1.0", "end")

    def log(self, msg=""):
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")

    def desenhar(self):
        try:
            x1 = int(self.ent["x1"].get())
            y1 = int(self.ent["y1"].get())
            x2 = int(self.ent["x2"].get())
            y2 = int(self.ent["y2"].get())
        except ValueError:
            messagebox.showerror("Erro", "Use somente valores inteiros.")
            return
        self.limpar()
        if self.alg.get() == "DDA":
            dda(x1, y1, x2, y2, self.set_pixel, self.log)
        else:
            bresenham(x1, y1, x2, y2, self.set_pixel, self.log)

    # =========================================================
    #  ABA 2 — TRANSFORMACOES GEOMETRICAS
    # =========================================================

    def _build_transf_tab(self, parent):
        esq = tk.Frame(parent, bg="#2b2b2b")
        esq.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        dir_ = tk.Frame(parent, bg="#2b2b2b")
        dir_.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        self.canvas_t = tk.Canvas(dir_, width=CANVAS_W, height=CANVAS_H,
                                  bg="black", highlightthickness=1,
                                  highlightbackground="#555")
        self.canvas_t.pack()

        tk.Label(esq, text="Transformacoes Geometricas",
                 font=("Arial", 12, "bold"),
                 bg="#2b2b2b", fg="white").pack(pady=(6, 4))

        # ---- Poligono ----
        frame_poly = _lframe(esq, "Poligono Regular")
        frame_poly.pack(padx=8, pady=4, fill="x")

        self.ent_t = {}
        tk.Label(frame_poly, text="Lados:", **_LBL).grid(
            row=0, column=0, padx=6, pady=6, sticky="e")
        e_lados = _entry(frame_poly, "4")
        e_lados.grid(row=0, column=1, padx=6, pady=6)
        self.ent_t["lados"] = e_lados

        tk.Label(frame_poly, text="Tamanho:", **_LBL).grid(
            row=0, column=2, padx=6, pady=6, sticky="e")
        e_raio = _entry(frame_poly, "100")
        e_raio.grid(row=0, column=3, padx=6, pady=6)
        self.ent_t["raio"] = e_raio


        # ---- Tipo de transformacao ----
        frame_tipo = _lframe(esq, "Tipo de Transformacao")
        frame_tipo.pack(padx=8, pady=4, fill="x")

        self.transf_tipo = tk.StringVar(value="translacao")
        tipos = [
            ("Translacao (T)",  "translacao"),
            ("Escala (S)",      "escala"),
            ("Rotacao (R)",     "rotacao"),
            ("Reflexao",        "reflexao"),
            ("Cisalhamento",    "cisalhamento"),
        ]
        for i, (txt, val) in enumerate(tipos):
            tk.Radiobutton(
                frame_tipo, text=txt,
                variable=self.transf_tipo, value=val,
                command=self._on_tipo_changed,
                bg="#2b2b2b", fg="white", selectcolor="#444",
                activebackground="#2b2b2b", activeforeground="white",
            ).grid(row=i // 3, column=i % 3, padx=6, pady=3, sticky="w")

        # ---- Painel dinamico de parametros ----
        self._params_container = tk.Frame(esq, bg="#2b2b2b")
        self._params_container.pack(padx=8, pady=2, fill="x")

        self._frames_params = {}
        self._build_param_translacao()
        self._build_param_escala()
        self._build_param_rotacao()
        self._build_param_reflexao()
        self._build_param_cisalhamento()
        self._on_tipo_changed()  # exibe frame inicial

        # ---- Botoes ----
        frame_btn = tk.Frame(esq, bg="#2b2b2b")
        frame_btn.pack(pady=8)
        tk.Button(frame_btn, text="Original",
                  command=self._draw_original,
                  width=10, bg="#2196F3", fg="white", **_BTN).pack(side="left", padx=3)
        tk.Button(frame_btn, text="Aplicar",
                  command=self._apply_transform,
                  width=10, bg="#4CAF50", fg="white", **_BTN).pack(side="left", padx=3)
        tk.Button(frame_btn, text="Resetar",
                  command=self._reset_transf,
                  width=8,  bg="#555",    fg="white", **_BTN).pack(side="left", padx=3)

        # ---- Log ----
        frame_log = tk.Frame(esq, bg="#2b2b2b")
        frame_log.pack(fill="x", padx=8)
        self.log_t = tk.Text(frame_log, width=38, height=8,
                             bg="#1a1a1a", fg="#d4d4d4",
                             font=("Consolas", 8),
                             insertbackground="white", relief="flat", bd=4)
        sc = tk.Scrollbar(frame_log, command=self.log_t.yview)
        self.log_t.configure(yscrollcommand=sc.set)
        self.log_t.pack(side="left", fill="both")
        sc.pack(side="right", fill="y")

        self._draw_axes(self.canvas_t)

    # ---- Sub-frames de parametros (um por tipo de transformacao) ----

    def _build_param_translacao(self):
        f = _lframe(self._params_container, "Parametros — Translacao")
        tk.Label(f, text="tx:", **_LBL).grid(row=0, column=0, padx=6, pady=6, sticky="e")
        self._tx = _entry(f, "50")
        self._tx.grid(row=0, column=1, padx=6, pady=6)
        tk.Label(f, text="ty:", **_LBL).grid(row=0, column=2, padx=6, pady=6, sticky="e")
        self._ty = _entry(f, "30")
        self._ty.grid(row=0, column=3, padx=6, pady=6)
        self._frames_params["translacao"] = f

    def _build_param_escala(self):
        f = _lframe(self._params_container, "Parametros — Escala")
        tk.Label(f, text="sx:", **_LBL).grid(row=0, column=0, padx=6, pady=6, sticky="e")
        self._sx = _entry(f, "2.0")
        self._sx.grid(row=0, column=1, padx=6, pady=6)
        tk.Label(f, text="sy:", **_LBL).grid(row=0, column=2, padx=6, pady=6, sticky="e")
        self._sy = _entry(f, "2.0")
        self._sy.grid(row=0, column=3, padx=6, pady=6)
        self._frames_params["escala"] = f

    def _build_param_rotacao(self):
        f = _lframe(self._params_container, "Parametros — Rotacao")
        tk.Label(f, text="Angulo (graus):", **_LBL).grid(
            row=0, column=0, padx=6, pady=6, sticky="e")
        self._angulo = _entry(f, "45", width=8)
        self._angulo.grid(row=0, column=1, padx=6, pady=6)
        tk.Label(f, text="(+ anti-horario)", bg="#2b2b2b",
                 fg="#666", font=("Arial", 8)).grid(
            row=0, column=2, padx=4, sticky="w")
        self._frames_params["rotacao"] = f

    def _build_param_reflexao(self):
        f = _lframe(self._params_container, "Parametros — Reflexao")
        self._eixo_refl = tk.StringVar(value="x")
        eixos = [("Eixo X",   "x"),
                 ("Eixo Y",   "y"),
                 ("Origem",   "origem"),
                 ("y = x",    "y=x")]
        for i, (txt, val) in enumerate(eixos):
            tk.Radiobutton(f, text=txt,
                           variable=self._eixo_refl, value=val,
                           bg="#2b2b2b", fg="white", selectcolor="#444",
                           activebackground="#2b2b2b",
                           activeforeground="white"
                           ).grid(row=i//2, column=i%2, padx=10, pady=3, sticky="w")
        self._frames_params["reflexao"] = f

    def _build_param_cisalhamento(self):
        f = _lframe(self._params_container, "Parametros — Cisalhamento")
        tk.Label(f, text="shx:", **_LBL).grid(row=0, column=0, padx=6, pady=6, sticky="e")
        self._shx = _entry(f, "0.5")
        self._shx.grid(row=0, column=1, padx=6, pady=6)
        tk.Label(f, text="shy:", **_LBL).grid(row=0, column=2, padx=6, pady=6, sticky="e")
        self._shy = _entry(f, "0.0")
        self._shy.grid(row=0, column=3, padx=6, pady=6)
        self._frames_params["cisalhamento"] = f

    def _on_tipo_changed(self):
        tipo = self.transf_tipo.get()
        for key, frame in self._frames_params.items():
            if key == tipo:
                frame.pack(fill="x", pady=2)
            else:
                frame.pack_forget()

    # ---- Helpers de canvas / matriz ----

    def _draw_axes(self, canvas):
        canvas.create_line(0, CY, CANVAS_W, CY, fill="#2a2a2a")
        canvas.create_line(CX, 0, CX, CANVAS_H, fill="#2a2a2a")

    def _set_pixel_t(self, x, y, cor="white"):
        px = int(round(x)) + CX
        py = CY - int(round(y))
        self.canvas_t.create_rectangle(px, py, px+1, py+1,
                                       outline=cor, fill=cor)

    # ---- Leitura de parametros ----

    def _get_poly_vertices(self):
        try:
            n = int(self.ent_t["lados"].get())
            r = float(self.ent_t["raio"].get())
            if n < 3:
                raise ValueError("Minimo de 3 lados.")
            if r <= 0:
                raise ValueError("Raio deve ser positivo.")
        except ValueError as exc:
            messagebox.showerror("Erro", str(exc))
            return None
        verts = poligono_regular(n, r)
        min_x = min(x for x, y in verts)
        min_y = min(y for x, y in verts)
        return [(x - min_x, y - min_y) for x, y in verts]

    def _build_transform_matrix(self):
        """Constroi a matriz 3x3 conforme o tipo selecionado."""
        tipo = self.transf_tipo.get()
        try:
            if tipo == "translacao":
                return translacao(float(self._tx.get()),
                                  float(self._ty.get()))
            if tipo == "escala":
                return escala(float(self._sx.get()),
                              float(self._sy.get()))
            if tipo == "rotacao":
                return rotacao(float(self._angulo.get()))
            if tipo == "reflexao":
                return reflexao(self._eixo_refl.get())
            if tipo == "cisalhamento":
                return cisalhamento(float(self._shx.get()),
                                    float(self._shy.get()))
        except ValueError:
            messagebox.showerror("Erro", "Parametros invalidos.")
            return None
        return identidade()

    # ---- Desenho do poligono via Bresenham geral ----

    def _draw_polygon_t(self, vertices, cor):
        n = len(vertices)
        for i in range(n):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % n]
            bresenham_geral(
                int(round(x1)), int(round(y1)),
                int(round(x2)), int(round(y2)),
                lambda px, py, c=cor: self._set_pixel_t(px, py, c),
            )

    # ---- Acoes dos botoes ----

    def _log_t(self, msg=""):
        self.log_t.insert("end", msg + "\n")
        self.log_t.see("end")

    def _draw_original(self):
        verts = self._get_poly_vertices()
        if verts is None:
            return
        self.canvas_t.delete("all")
        self._draw_axes(self.canvas_t)
        self._draw_polygon_t(verts, "#2196F3")
        self.log_t.delete("1.0", "end")
        self._log_t("=== Poligono original ===")
        for i, (x, y) in enumerate(verts):
            self._log_t(f"  V{i+1} = ({x:7.2f}, {y:7.2f}, 1)")

    def _apply_transform(self):
        verts = self._get_poly_vertices()
        if verts is None:
            return
        M = self._build_transform_matrix()
        if M is None:
            return
        verts_t = aplicar_transformacao(verts, M)
        self.canvas_t.delete("all")
        self._draw_axes(self.canvas_t)
        self._draw_polygon_t(verts_t, "#2196F3")
        self.log_t.delete("1.0", "end")
        self._log_t(f"=== {self.transf_tipo.get().capitalize()} ===")
        self._log_t("--- Vertices transformados ---")
        for i, (x, y) in enumerate(verts_t):
            self._log_t(f"  V{i+1}' = ({x:7.2f}, {y:7.2f}, 1)")

    def _reset_transf(self):
        self.canvas_t.delete("all")
        self._draw_axes(self.canvas_t)
        self.log_t.delete("1.0", "end")


# ---------------------------------------------------------------------------
def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
