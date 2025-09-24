import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from lexical_analyzer import LexicalAnalyzer, TokenType, ProgrammingLanguage
import json
from datetime import datetime

class ModernLexicalAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Analizador Léxico Avanzado v2.0")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)
        
        # Variables de tema
        self.setup_themes()
        
        # Inicializar el analizador
        self.analyzer = LexicalAnalyzer()
        
        # Variables para almacenar resultados
        self.current_tokens = []
        self.current_errors = []
        self.current_language = ProgrammingLanguage.UNKNOWN
        self.analysis_stats = {}
        self.analysis_time = 0
        
        # Configurar el icono de la ventana (si existe)
        self.setup_icon()
        
        # Crear la interfaz
        self.create_widgets()
        
        # Aplicar tema inicial
        self.apply_theme()
        
        # Configurar atajos de teclado
        self.setup_shortcuts()
        
        # Inicializar widgets con contenido vacío
        self.initialize_empty_widgets()
        
    def setup_icon(self):
        """Configurar icono de la aplicación"""
        try:
            # Si tienes un archivo .ico, descomenta la siguiente línea
            # self.root.iconbitmap("icon.ico")
            pass
        except:
            pass
    
    def setup_themes(self):
        """Configurar temas claro y oscuro"""
        self.themes = {
            'dark': {
                'bg': '#2b2b2b',
                'fg': '#ffffff',
                'select_bg': '#404040',
                'select_fg': '#ffffff',
                'accent': '#0078d4',
                'error': '#ff6b6b',
                'success': '#51cf66',
                'warning': '#ffd43b',
                'card_bg': '#363636',
                'border': '#555555'
            },
            'light': {
                'bg': '#ffffff',
                'fg': '#000000',
                'select_bg': '#e3f2fd',
                'select_fg': '#000000',
                'accent': '#1976d2',
                'error': '#d32f2f',
                'success': '#388e3c',
                'warning': '#f57c00',
                'card_bg': '#f5f5f5',
                'border': '#cccccc'
            }
        }
    
    def apply_theme(self):
        """Aplicar tema seleccionado"""
        theme_name = 'light'
        theme = self.themes[theme_name]
        
        # Configurar colores principales
        self.root.configure(bg=theme['bg'])
        
        # Configurar estilo ttk
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar estilos personalizados
        style.configure('Modern.TFrame', background=theme['bg'])
        style.configure('Card.TFrame', background=theme['card_bg'], relief='solid', borderwidth=1)
        style.configure('Modern.TLabel', background=theme['bg'], foreground=theme['fg'])
        style.configure('Card.TLabel', background=theme['card_bg'], foreground=theme['fg'])
        style.configure('Title.TLabel', background=theme['bg'], foreground=theme['accent'], 
                       font=('Segoe UI', 12, 'bold'))
        style.configure('Modern.TButton', focuscolor='none')
        style.configure('Accent.TButton', background=theme['accent'])
    
    def setup_shortcuts(self):
        """Configurar atajos de teclado"""
        self.root.bind('<Control-o>', lambda e: self.load_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<F5>', lambda e: self.analyze_code())
        self.root.bind('<Control-r>', lambda e: self.reset_analysis())
        self.root.bind('<F1>', lambda e: self.show_help())
    
    def create_widgets(self):
        """Crear todos los widgets de la interfaz"""
        
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, style='Modern.TFrame', padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ========== BARRA SUPERIOR ==========
        self.create_top_bar(main_frame)
        
        # ========== ÁREA PRINCIPAL ==========
        content_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        content_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Configurar grid para mejor distribución
        content_frame.grid_columnconfigure(0, weight=3)  # Código - más espacio
        content_frame.grid_columnconfigure(1, weight=1)  # Info rápida - menos espacio
        
        # Panel izquierdo (entrada de código)
        left_panel = ttk.Frame(content_frame, style='Card.TFrame', padding="10")
        left_panel.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        
        # Panel derecho (información rápida)
        right_panel = ttk.Frame(content_frame, style='Card.TFrame', padding="10")
        right_panel.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
        
        self.create_code_input_section(left_panel)
        self.create_quick_info_section(right_panel)
        
        # ========== ÁREA DE RESULTADOS ==========
        results_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.create_results_section(results_frame)
        
        # ========== BARRA DE ESTADO ==========
        self.create_status_bar(main_frame)
    
    def create_top_bar(self, parent):
        """Crear barra superior con controles principales"""
        top_bar = ttk.Frame(parent, style='Card.TFrame', padding="10")
        top_bar.pack(fill=tk.X, pady=(0, 10))
        
        # Título de la aplicación
        title_label = ttk.Label(top_bar, text="🔍 Analizador Léxico Avanzado", 
                               style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Controles del lado derecho
        controls_frame = ttk.Frame(top_bar, style='Card.TFrame')
        controls_frame.pack(side=tk.RIGHT)
        
        
        # Botón de ayuda
        ttk.Button(controls_frame, text="❓ Ayuda", 
                  command=self.show_help).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Botón de exportar
        ttk.Button(controls_frame, text="📤 Exportar", 
                  command=self.export_analysis).pack(side=tk.RIGHT, padx=(10, 0))
    
    def create_code_input_section(self, parent):
        """Crear sección de entrada de código"""
        # Header con botones
        header_frame = ttk.Frame(parent, style='Card.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="📝 Código Fuente", 
                 style='Card.TLabel', font=('Segoe UI', 11, 'bold')).pack(side=tk.LEFT)
        
        # Botones de archivo
        btn_frame = ttk.Frame(header_frame, style='Card.TFrame')
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame, text="📁 Abrir", command=self.load_file).pack(side=tk.LEFT)
        
        # Área de texto con números de línea
        text_frame = ttk.Frame(parent, style='Card.TFrame')
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # Frame para el área de texto principal
        editor_frame = ttk.Frame(text_frame, style='Card.TFrame')
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        # Números de línea
        self.line_numbers = tk.Text(editor_frame, width=4, padx=5, takefocus=0,
                                   border=0, state='disabled', wrap='none',
                                   font=('Consolas', 10), bg='#f0f0f0', fg='#666666')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Área de código principal
        self.code_text = scrolledtext.ScrolledText(editor_frame, font=('Consolas', 10),
                                                  wrap=tk.NONE, undo=True, maxundo=50, height=10)
        self.code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configurar eventos para sincronizar números de línea
        self.code_text.bind('<KeyRelease>', self.update_line_numbers)
        self.code_text.bind('<Button-1>', self.update_line_numbers)
        self.code_text.bind('<MouseWheel>', self.update_line_numbers)
        
        # Botones de análisis
        analysis_frame = ttk.Frame(parent, style='Card.TFrame')
        analysis_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(analysis_frame, text="🔍 Analizar Código", 
                  command=self.analyze_code, style='Accent.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(analysis_frame, text="🔄 Limpiar", 
                  command=self.reset_analysis).pack(side=tk.LEFT)
        
        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(analysis_frame, variable=self.progress_var, 
                                          length=200, mode='determinate')
        self.progress_bar.pack(side=tk.RIGHT)
    
    def create_quick_info_section(self, parent):
        """Crear panel de información rápida"""
        # Header
        ttk.Label(parent, text="📊 Información Rápida", 
                 style='Card.TLabel', font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        # Métricas principales
        metrics_frame = ttk.LabelFrame(parent, text="Métricas", padding="8")
        metrics_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
        
        self.metrics_text = tk.Text(metrics_frame, height=5, state=tk.DISABLED, 
                                   font=('Consolas', 9), wrap=tk.WORD, bg='#f8f8f8')
        self.metrics_text.pack(fill=tk.BOTH, expand=True)
        
        # Detección de lenguaje
        lang_frame = ttk.LabelFrame(parent, text="Lenguaje", padding="8")
        lang_frame.pack(fill=tk.X, pady=(0, 8))
        
        self.language_label = ttk.Label(lang_frame, text="No detectado", 
                                       style='Card.TLabel', font=('Segoe UI', 10))
        self.language_label.pack()
        
        # Búsqueda rápida
        search_frame = ttk.LabelFrame(parent, text="Búsqueda", padding="8")
        search_frame.pack(fill=tk.X, pady=(0, 8))
        
        self.search_entry = ttk.Entry(search_frame)
        # Simular placeholder text
        self.search_entry.insert(0, "Buscar token...")
        self.search_entry.configure(foreground='gray')
        self.search_entry.bind('<FocusIn>', self._on_search_focus_in)
        self.search_entry.bind('<FocusOut>', self._on_search_focus_out)
        self.search_entry.pack(fill=tk.X, pady=(0, 5))
        self.search_entry.bind('<Return>', self.quick_search)
        
        ttk.Button(search_frame, text="🔍 Buscar", 
                  command=self.quick_search).pack(fill=tk.X)
    
    def create_results_section(self, parent):
        """Crear sección de resultados con pestañas mejoradas"""
        # Notebook con pestañas
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de tokens
        self.create_enhanced_tokens_tab()
        
        # Pestaña de estadísticas
        self.create_detailed_stats_tab()
        
        # Pestaña de errores
        self.create_enhanced_errors_tab()
        
        # Pestaña de análisis
        self.create_analysis_tab()
    
    def create_enhanced_tokens_tab(self):
        """Crear pestaña mejorada de tokens"""
        tokens_frame = ttk.Frame(self.notebook)
        self.notebook.add(tokens_frame, text="🏷️ Tokens")
        
        # Controles superiores
        controls = ttk.Frame(tokens_frame)
        controls.pack(fill=tk.X, padx=10, pady=10)
        
        # Filtros
        ttk.Label(controls, text="Filtrar:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.filter_var = tk.StringVar(value="Todos")
        filter_combo = ttk.Combobox(controls, textvariable=self.filter_var, 
                                   state="readonly", width=15)
        filter_combo['values'] = ["Todos"] + [token_type.value for token_type in TokenType]
        filter_combo.pack(side=tk.LEFT, padx=(0, 10))
        filter_combo.bind('<<ComboboxSelected>>', self.filter_tokens)
        
        # Búsqueda
        ttk.Label(controls, text="Buscar:").pack(side=tk.LEFT, padx=(10, 5))
        self.token_search_var = tk.StringVar()
        search_entry = ttk.Entry(controls, textvariable=self.token_search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=(0, 5))
        search_entry.bind('<KeyRelease>', self.filter_tokens)
        
        # Contador
        self.token_count_var = tk.StringVar()
        ttk.Label(controls, textvariable=self.token_count_var).pack(side=tk.RIGHT)
        
        # Tabla de tokens mejorada
        table_frame = ttk.Frame(tokens_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        columns = ('Línea', 'Col', 'Tipo', 'Valor', 'Descripción')
        self.tokens_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        self.tokens_tree.heading('Línea', text='Línea')
        self.tokens_tree.heading('Col', text='Col')
        self.tokens_tree.heading('Tipo', text='Tipo')
        self.tokens_tree.heading('Valor', text='Valor')
        self.tokens_tree.heading('Descripción', text='Descripción del Patrón')
        
        self.tokens_tree.column('Línea', width=60, anchor=tk.CENTER)
        self.tokens_tree.column('Col', width=50, anchor=tk.CENTER)
        self.tokens_tree.column('Tipo', width=140, anchor=tk.W)
        self.tokens_tree.column('Valor', width=180, anchor=tk.W)
        self.tokens_tree.column('Descripción', width=350, anchor=tk.W)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tokens_tree.yview)
        h_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tokens_tree.xview)
        self.tokens_tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        # Grid layout
        self.tokens_tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Configurar colores
        self.setup_token_colors()
        
        # Menú contextual
        self.create_context_menu()
    
    def create_detailed_stats_tab(self):
        """Crear pestaña de estadísticas detalladas"""
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="📊 Estadísticas")
        
        # Crear subpestañas para diferentes tipos de estadísticas
        stats_notebook = ttk.Notebook(stats_frame)
        stats_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sub-pestaña: Resumen general
        self.create_general_stats_subtab(stats_notebook)
        
        # Sub-pestaña: Distribución
        self.create_distribution_subtab(stats_notebook)
        
        # Sub-pestaña: Complejidad
        self.create_complexity_subtab(stats_notebook)
    
    def create_enhanced_errors_tab(self):
        """Crear pestaña mejorada de errores"""
        errors_frame = ttk.Frame(self.notebook)
        self.notebook.add(errors_frame, text="⚠️ Errores")
        
        # Header con controles
        header = ttk.Frame(errors_frame)
        header.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        ttk.Label(header, text="Errores y Advertencias", 
                 font=('Segoe UI', 11, 'bold')).pack(side=tk.LEFT)
        
        # Botón para corregir errores automáticamente (si es posible)
        ttk.Button(header, text="🔧 Sugerir Correcciones", 
                  command=self.suggest_fixes).pack(side=tk.RIGHT)
        
        # Área de errores con categorización
        self.errors_text = scrolledtext.ScrolledText(errors_frame, font=('Consolas', 9), height=15)
        self.errors_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Configurar tags para diferentes tipos de errores
        self.errors_text.tag_configure("error", foreground="#ff6b6b", font=('Consolas', 10, 'bold'))
        self.errors_text.tag_configure("warning", foreground="#ffd43b")
        self.errors_text.tag_configure("info", foreground="#51cf66")
    
    def create_analysis_tab(self):
        """Crear pestaña de análisis avanzado"""
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text="🔬 Análisis")
        
        # Análisis de patrones
        patterns_frame = ttk.LabelFrame(analysis_frame, text="Patrones Detectados", padding="10")
        patterns_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.patterns_text = scrolledtext.ScrolledText(patterns_frame, height=10, 
                                                      font=('Consolas', 9))
        self.patterns_text.pack(fill=tk.X)
        
        # Sugerencias de mejora
        suggestions_frame = ttk.LabelFrame(analysis_frame, text="Sugerencias", padding="10")
        suggestions_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.suggestions_text = scrolledtext.ScrolledText(suggestions_frame, 
                                                        font=('Consolas', 9), height=15)
        self.suggestions_text.pack(fill=tk.BOTH, expand=True)
    
    def create_general_stats_subtab(self, parent):
        """Crear sub-pestaña de estadísticas generales"""
        general_frame = ttk.Frame(parent)
        parent.add(general_frame, text="General")
        
        self.general_stats_text = scrolledtext.ScrolledText(general_frame, 
                                                           font=('Consolas', 9), height=20)
        self.general_stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_distribution_subtab(self, parent):
        """Crear sub-pestaña de distribución"""
        dist_frame = ttk.Frame(parent)
        parent.add(dist_frame, text="Distribución")
        
        # Gráfico de distribución (simulado con texto)
        self.distribution_text = scrolledtext.ScrolledText(dist_frame, 
                                                          font=('Consolas', 9), height=20)
        self.distribution_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_complexity_subtab(self, parent):
        """Crear sub-pestaña de complejidad"""
        complexity_frame = ttk.Frame(parent)
        parent.add(complexity_frame, text="Complejidad")
        
        self.complexity_text = scrolledtext.ScrolledText(complexity_frame, 
                                                        font=('Consolas', 9), height=20)
        self.complexity_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_status_bar(self, parent):
        """Crear barra de estado mejorada"""
        status_frame = ttk.Frame(parent, style='Card.TFrame', padding="5")
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Status principal
        self.status_var = tk.StringVar(value="✅ Listo para analizar código")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                                style='Card.TLabel')
        status_label.pack(side=tk.LEFT)
        
        # Información adicional
        self.analysis_time_var = tk.StringVar()
        ttk.Label(status_frame, textvariable=self.analysis_time_var, 
                 style='Card.TLabel').pack(side=tk.RIGHT, padx=(10, 0))
        
        # Separador
        ttk.Separator(status_frame, orient='vertical').pack(side=tk.RIGHT, 
                                                           fill=tk.Y, padx=5)
        
        # Contador de líneas
        self.line_count_var = tk.StringVar(value="Líneas: 0")
        ttk.Label(status_frame, textvariable=self.line_count_var, 
                 style='Card.TLabel').pack(side=tk.RIGHT)
    
    def setup_token_colors(self):
        """Configurar colores para diferentes tipos de tokens"""
        colors = {
            TokenType.KEYWORD: '#569cd6',      # Azul para palabras clave
            TokenType.STRING: '#ce9178',       # Naranja para cadenas
            TokenType.COMMENT: '#6a9955',      # Verde para comentarios
            TokenType.NUMBER: '#b5cea8',       # Verde claro para números
            TokenType.OPERATOR: '#d4d4d4',     # Gris claro para operadores
            TokenType.IDENTIFIER: '#9cdcfe',   # Azul claro para identificadores
            TokenType.DELIMITER: '#ffd700',    # Amarillo para delimitadores
            TokenType.UNKNOWN: '#f44747'       # Rojo para tokens desconocidos
        }
        
        for token_type, color in colors.items():
            self.tokens_tree.tag_configure(token_type.value, foreground=color)
    
    def create_context_menu(self):
        """Crear menú contextual para la tabla de tokens"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Copiar valor", command=self.copy_token_value)
        self.context_menu.add_command(label="Buscar similares", command=self.find_similar_tokens)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Ir a línea", command=self.go_to_line)
        
        self.tokens_tree.bind("<Button-3>", self.show_context_menu)
    
    def initialize_empty_widgets(self):
        """Inicializar widgets con contenido vacío para evitar errores"""
        try:
            # Inicializar widgets de texto con mensajes de bienvenida
            welcome_msg = "Bienvenido al Analizador Léxico\nPara comenzar:\n1. Escriba o cargue código Python\n2. Haga clic en 'Analizar Código'\n3. Explore los resultados en las pestañas"
            
            # Métricas
            if hasattr(self, 'metrics_text'):
                self.metrics_text.config(state=tk.NORMAL)
                self.metrics_text.insert(1.0, "No hay métricas disponibles\nRealice un análisis para ver estadísticas")
                self.metrics_text.config(state=tk.DISABLED)
            
            # Estadísticas generales
            if hasattr(self, 'general_stats_text'):
                self.general_stats_text.insert(1.0, welcome_msg)
                
            # Distribución
            if hasattr(self, 'distribution_text'):
                self.distribution_text.insert(1.0, "No hay datos de distribución\nEjecute un análisis para ver la distribución de tokens")
                
            # Complejidad
            if hasattr(self, 'complexity_text'):
                self.complexity_text.insert(1.0, "No hay análisis de complejidad\nEjecute un análisis para ver métricas de complejidad")
                
            # Errores
            if hasattr(self, 'errors_text'):
                self.errors_text.insert(1.0, "✅ No hay errores que mostrar\nLos errores aparecerán aquí después del análisis")
                
            # Patrones
            if hasattr(self, 'patterns_text'):
                self.patterns_text.insert(1.0, "No hay patrones detectados\nLos patrones de código aparecerán después del análisis")
                
            # Sugerencias
            if hasattr(self, 'suggestions_text'):
                self.suggestions_text.insert(1.0, "No hay sugerencias disponibles\nLas recomendaciones aparecerán después del análisis")
            
            # Configurar colores de tokens
            if hasattr(self, 'tokens_tree'):
                self.setup_token_colors()
                
        except Exception as e:
            print(f"Error en inicialización: {e}")
    
    # ========== MÉTODOS DE FUNCIONALIDAD ==========
    
    
    def update_line_numbers(self, event=None):
        """Actualizar números de línea"""
        self.line_numbers.config(state='normal')
        self.line_numbers.delete(1.0, tk.END)
        
        # Obtener el número de líneas
        line_count = int(self.code_text.index('end').split('.')[0])
        
        # Generar números de línea
        line_numbers_text = '\n'.join(str(i) for i in range(1, line_count))
        self.line_numbers.insert(1.0, line_numbers_text)
        self.line_numbers.config(state='disabled')
        
        # Actualizar contador de líneas
        self.line_count_var.set(f"Líneas: {line_count - 1}")
        
        # Sincronizar scroll
        def sync_scroll(*args):
            self.line_numbers.yview_moveto(args[0])
        
        self.code_text.config(yscrollcommand=sync_scroll)
    
    
    def load_file(self):
        """Cargar archivo con manejo mejorado de errores"""
        file_types = [
            ('Archivos Python', '*.py'),
            ('Archivos Java', '*.java'),
            ('Archivos C/C++', '*.c *.cpp *.h *.hpp'),
            ('Archivos JavaScript', '*.js *.ts'),
            ('Archivos de texto', '*.txt'),
            ('Todos los archivos', '*.*')
        ]
        
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de código",
            filetypes=file_types
        )
        
        if filename:
            try:
                # Intentar diferentes encodings
                encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
                content = None
                
                for encoding in encodings:
                    try:
                        with open(filename, 'r', encoding=encoding) as file:
                            content = file.read()
                            break
                    except UnicodeDecodeError:
                        continue
                
                if content is not None:
                    self.code_text.delete(1.0, tk.END)
                    self.code_text.insert(1.0, content)
                    self.update_line_numbers()
                    self.status_var.set(f"📁 Archivo cargado: {os.path.basename(filename)}")
                else:
                    raise Exception("No se pudo decodificar el archivo con ningún encoding")
                    
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
                self.status_var.set("❌ Error al cargar archivo")
    
    
    def analyze_code(self):
        """Analizar código con progreso visual"""
        code = self.code_text.get(1.0, tk.END).strip()
        
        if not code:
            messagebox.showwarning("Advertencia", "Por favor, ingrese código para analizar")
            return
        
        # Mostrar progreso
        self.progress_var.set(0)
        self.status_var.set("🔍 Analizando código...")
        self.root.update()
        
        try:
            import time
            start_time = time.time()
            
            # Simular progreso
            for i in range(0, 101, 20):
                self.progress_var.set(i)
                self.root.update()
                time.sleep(0.1)
            
            # Realizar análisis
            tokens, lex_errors, language = self.analyzer.tokenize(code)
            syntax_errors = self.analyzer.validate_syntax_basic(tokens)
            
            # Obtener estadísticas detalladas
            self.analysis_stats = self.analyzer.get_analysis_stats(tokens)
            
            # Almacenar resultados
            self.current_tokens = tokens
            self.current_errors = lex_errors + syntax_errors
            self.current_language = language
            self.analysis_time = time.time() - start_time
            
            # Actualizar interfaz
            self.update_all_displays()
            
            # Finalizar progreso
            self.progress_var.set(100)
            self.status_var.set(f"✅ Análisis completado - {len(tokens)} tokens encontrados")
            self.analysis_time_var.set(f"⏱️ Tiempo: {self.analysis_time:.3f}s")
            
            # Resetear progreso después de un momento
            self.root.after(2000, lambda: self.progress_var.set(0))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el análisis:\n{str(e)}")
            self.status_var.set("❌ Error en el análisis")
            self.progress_var.set(0)
    
    def update_all_displays(self):
        """Actualizar todas las visualizaciones"""
        self.update_tokens_display()
        self.update_quick_info()
        self.update_detailed_stats()
        self.update_errors_display()
        self.update_analysis_display()
    
    def update_tokens_display(self):
        """Actualizar la tabla de tokens"""
        # Limpiar tabla
        for item in self.tokens_tree.get_children():
            self.tokens_tree.delete(item)
        
        # Insertar tokens con información extendida
        for i, token in enumerate(self.current_tokens):
            values = (
                token.line,
                token.column,
                token.type.value,
                token.value[:50] + ("..." if len(token.value) > 50 else ""),
                token.pattern_description
            )
            
            # Aplicar colores alternados y por tipo
            tags = ['oddrow' if i % 2 else 'evenrow', token.type.value]
            
            self.tokens_tree.insert('', tk.END, values=values, tags=tags)
        
        # Actualizar contador
        self.token_count_var.set(f"Total: {len(self.current_tokens)} tokens")
        
        # Resetear filtro
        self.filter_var.set("Todos")
        self.token_search_var.set("")
    
    def update_quick_info(self):
        """Actualizar panel de información rápida"""
        if not self.current_tokens:
            return
        
        # Actualizar métricas
        metrics_text = f"""📊 MÉTRICAS GENERALES
┌─────────────────────────────┐
│ Total de tokens: {len(self.current_tokens):>10} │
│ Líneas de código: {self.analysis_stats.get('total_lines', 0):>9} │
│ Errores encontrados: {len(self.current_errors):>6} │
│ Tiempo de análisis: {self.analysis_time:.3f}s │
└─────────────────────────────┘

🏷️ TIPOS DE TOKENS:
"""
        
        # Agregar distribución de tokens
        for token_type, count in sorted(self.analysis_stats.get('token_distribution', {}).items()):
            percentage = (count / len(self.current_tokens) * 100) if self.current_tokens else 0
            metrics_text += f"• {token_type}: {count} ({percentage:.1f}%)\\n"
        
        self.metrics_text.config(state=tk.NORMAL)
        self.metrics_text.delete(1.0, tk.END)
        self.metrics_text.insert(1.0, metrics_text)
        self.metrics_text.config(state=tk.DISABLED)
        
        # Actualizar detección de lenguaje
        confidence = "Alta" if len(self.current_tokens) > 20 else "Media"
        self.language_label.config(text=f"{self.current_language.value}\\n({confidence} confianza)")
    
    def update_detailed_stats(self):
        """Actualizar estadísticas detalladas"""
        if not hasattr(self, 'analysis_stats') or not self.analysis_stats:
            return
        
        # Estadísticas generales
        general_text = self.generate_general_stats_text()
        self.general_stats_text.delete(1.0, tk.END)
        self.general_stats_text.insert(1.0, general_text)
        
        # Distribución
        distribution_text = self.generate_distribution_text()
        self.distribution_text.delete(1.0, tk.END)
        self.distribution_text.insert(1.0, distribution_text)
        
        # Complejidad
        complexity_text = self.generate_complexity_text()
        self.complexity_text.delete(1.0, tk.END)
        self.complexity_text.insert(1.0, complexity_text)
    
    def generate_general_stats_text(self):
        """Generar texto de estadísticas generales"""
        stats = self.analysis_stats
        
        text = f"""📈 ESTADÍSTICAS GENERALES DEL CÓDIGO
{'='*50}

🎯 RESUMEN EJECUTIVO:
• Total de tokens analizados: {stats.get('total_tokens', 0)}
• Líneas de código procesadas: {stats.get('total_lines', 0)}
• Lenguaje detectado: {self.current_language.value}
• Tiempo de procesamiento: {self.analysis_time:.3f} segundos
• Velocidad de análisis: {stats.get('total_tokens', 0)/self.analysis_time:.0f} tokens/segundo

🔤 ANÁLISIS LÉXICO:
• Identificadores únicos: {len(stats.get('unique_identifiers', []))}
• Palabras clave utilizadas: {len(stats.get('keywords_used', []))}
• Densidad de comentarios: {(stats.get('token_distribution', {}).get('COMENTARIO', 0)/stats.get('total_tokens', 1)*100):.1f}%

📝 IDENTIFICADORES ENCONTRADOS:
{', '.join(stats.get('unique_identifiers', [])[:20])}
{'...' if len(stats.get('unique_identifiers', [])) > 20 else ''}

🔑 PALABRAS CLAVE UTILIZADAS:
{', '.join(stats.get('keywords_used', []))}
"""
        return text
    
    def generate_distribution_text(self):
        """Generar texto de distribución de tokens"""
        distribution = self.analysis_stats.get('token_distribution', {})
        total = sum(distribution.values())
        
        text = f"""📊 DISTRIBUCIÓN DE TOKENS
{'='*50}

Gráfico de distribución (representación textual):

"""
        
        # Crear un gráfico de barras ASCII
        max_count = max(distribution.values()) if distribution else 1
        
        for token_type, count in sorted(distribution.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total * 100) if total > 0 else 0
            bar_length = int(count / max_count * 40)
            bar = '█' * bar_length + '░' * (40 - bar_length)
            
            text += f"{token_type:<15} │{bar}│ {count:>4} ({percentage:5.1f}%)\\n"
        
        text += f"""
{'='*60}
Total de tokens: {total}

📈 ANÁLISIS DE DISTRIBUCIÓN:
• Tipo más frecuente: {max(distribution.keys(), key=distribution.get) if distribution else 'N/A'}
• Tipo menos frecuente: {min(distribution.keys(), key=distribution.get) if distribution else 'N/A'}
• Variedad de tipos: {len(distribution)} tipos diferentes
"""
        
        return text
    
    def generate_complexity_text(self):
        """Generar texto de análisis de complejidad"""
        complexity = self.analysis_stats.get('complexity_indicators', {})
        
        text = f"""🔬 ANÁLISIS DE COMPLEJIDAD
{'='*50}

📐 MÉTRICAS DE COMPLEJIDAD:

🏗️ Estructura del código:
• Definiciones de función: {complexity.get('function_definitions', 0)}
• Bucles detectados: {complexity.get('loops', 0)}
• Estructuras condicionales: {complexity.get('conditionals', 0)}
• Máximo nivel de anidación: {complexity.get('nested_blocks', 0)}

📊 EVALUACIÓN DE COMPLEJIDAD:
"""
        
        # Calcular puntuación de complejidad
        complexity_score = (
            complexity.get('function_definitions', 0) * 2 +
            complexity.get('loops', 0) * 3 +
            complexity.get('conditionals', 0) * 2 +
            complexity.get('nested_blocks', 0) * 5
        )
        
        if complexity_score < 10:
            complexity_level = "🟢 BAJA - Código simple y fácil de mantener"
        elif complexity_score < 30:
            complexity_level = "🟡 MEDIA - Complejidad moderada"
        else:
            complexity_level = "🔴 ALTA - Código complejo, considere refactorización"
        
        text += f"• Puntuación de complejidad: {complexity_score}\\n"
        text += f"• Nivel de complejidad: {complexity_level}\\n\\n"
        
        # Recomendaciones
        text += "💡 RECOMENDACIONES:\\n"
        if complexity.get('nested_blocks', 0) > 3:
            text += "• Considere reducir el nivel de anidación\\n"
        if complexity.get('function_definitions', 0) == 0:
            text += "• Considere organizar el código en funciones\\n"
        if len(self.analysis_stats.get('unique_identifiers', [])) > 50:
            text += "• Gran cantidad de identificadores, considere revisar el naming\\n"
        if not text.endswith("RECOMENDACIONES:\\n"):
            text += "• El código tiene una estructura apropiada\\n"
        
        return text
    
    def update_errors_display(self):
        """Actualizar visualización de errores mejorada"""
        self.errors_text.delete(1.0, tk.END)
        
        if not self.current_errors:
            self.errors_text.insert(tk.END, "✅ ANÁLISIS EXITOSO\\n\\n", "info")
            self.errors_text.insert(tk.END, "🎉 ¡Excelente! No se encontraron errores en el código.\\n\\n")
            self.errors_text.insert(tk.END, "📋 VALIDACIONES REALIZADAS:\\n")
            self.errors_text.insert(tk.END, "• ✓ Sintaxis léxica válida\\n")
            self.errors_text.insert(tk.END, "• ✓ Delimitadores balanceados\\n")
            self.errors_text.insert(tk.END, "• ✓ Tokens reconocidos correctamente\\n")
        else:
            self.errors_text.insert(tk.END, f"⚠️ ERRORES ENCONTRADOS ({len(self.current_errors)})\\n\\n", "error")
            
            # Categorizar errores
            lexical_errors = [e for e in self.current_errors if "no reconocido" in e.lower()]
            syntax_errors = [e for e in self.current_errors if e not in lexical_errors]
            
            if lexical_errors:
                self.errors_text.insert(tk.END, "🔤 ERRORES LÉXICOS:\\n", "error")
                for i, error in enumerate(lexical_errors, 1):
                    self.errors_text.insert(tk.END, f"{i}. {error}\\n")
                self.errors_text.insert(tk.END, "\\n")
            
            if syntax_errors:
                self.errors_text.insert(tk.END, "⚙️ ERRORES SINTÁCTICOS:\\n", "warning")
                for i, error in enumerate(syntax_errors, 1):
                    self.errors_text.insert(tk.END, f"{i}. {error}\\n")
    
    def update_analysis_display(self):
        """Actualizar visualización de análisis avanzado"""
        # Patrones detectados
        patterns_text = "🔍 PATRONES DETECTADOS:\\n\\n"
        
        # Analizar patrones comunes
        if self.current_language == ProgrammingLanguage.PYTHON:
            patterns_text += self.analyze_python_patterns()
        elif self.current_language == ProgrammingLanguage.JAVA:
            patterns_text += self.analyze_java_patterns()
        elif self.current_language == ProgrammingLanguage.C:
            patterns_text += self.analyze_c_patterns()
        else:
            patterns_text += "• Análisis de patrones específicos disponible para Python, Java y C\\n"
        
        self.patterns_text.delete(1.0, tk.END)
        self.patterns_text.insert(1.0, patterns_text)
        
        # Sugerencias
        suggestions_text = self.generate_suggestions()
        self.suggestions_text.delete(1.0, tk.END)
        self.suggestions_text.insert(1.0, suggestions_text)
    
    def analyze_python_patterns(self):
        """Analizar patrones específicos de Python"""
        text = ""
        keywords = self.analysis_stats.get('keywords_used', [])
        
        if 'def' in keywords:
            text += "• ✓ Definiciones de función encontradas\\n"
        if 'class' in keywords:
            text += "• ✓ Definiciones de clase encontradas\\n"
        if 'import' in keywords or 'from' in keywords:
            text += "• ✓ Importaciones detectadas\\n"
        if 'if' in keywords:
            text += "• ✓ Estructuras condicionales presentes\\n"
        if 'for' in keywords or 'while' in keywords:
            text += "• ✓ Bucles detectados\\n"
        
        return text
    
    def analyze_java_patterns(self):
        """Analizar patrones específicos de Java"""
        text = ""
        keywords = self.analysis_stats.get('keywords_used', [])
        
        if 'public' in keywords:
            text += "• ✓ Modificadores de acceso público\\n"
        if 'class' in keywords:
            text += "• ✓ Definiciones de clase\\n"
        if 'static' in keywords:
            text += "• ✓ Miembros estáticos\\n"
        if 'main' in self.analysis_stats.get('unique_identifiers', []):
            text += "• ✓ Método main detectado\\n"
        
        return text
    
    def analyze_c_patterns(self):
        """Analizar patrones específicos de C"""
        text = ""
        keywords = self.analysis_stats.get('keywords_used', [])
        
        if 'include' in keywords:
            text += "• ✓ Directivas de preprocesador\\n"
        if 'int' in keywords or 'char' in keywords or 'float' in keywords:
            text += "• ✓ Declaraciones de variables\\n"
        if 'main' in self.analysis_stats.get('unique_identifiers', []):
            text += "• ✓ Función main detectada\\n"
        
        return text
    
    def generate_suggestions(self):
        """Generar sugerencias de mejora"""
        suggestions = "💡 SUGERENCIAS DE MEJORA:\\n\\n"
        
        # Análisis de comentarios
        comment_ratio = (self.analysis_stats.get('token_distribution', {}).get('COMENTARIO', 0) / 
                        len(self.current_tokens) * 100) if self.current_tokens else 0
        
        if comment_ratio < 5:
            suggestions += "📝 Documentación:\\n"
            suggestions += "• Considere agregar más comentarios para mejorar la legibilidad\\n\\n"
        
        # Análisis de nombres
        identifiers = self.analysis_stats.get('unique_identifiers', [])
        short_names = [name for name in identifiers if len(name) <= 2 and not name in ['i', 'j', 'k']]
        
        if short_names:
            suggestions += "🏷️ Nomenclatura:\\n"
            suggestions += f"• Considere usar nombres más descriptivos para: {', '.join(short_names[:5])}\\n\\n"
        
        # Análisis de complejidad
        complexity = self.analysis_stats.get('complexity_indicators', {})
        if complexity.get('nested_blocks', 0) > 4:
            suggestions += "🏗️ Estructura:\\n"
            suggestions += "• El código tiene alta anidación, considere refactorizar\\n\\n"
        
        if not suggestions.endswith("SUGERENCIAS DE MEJORA:\\n\\n"):
            suggestions += "✅ El código sigue buenas prácticas generales\\n"
        
        return suggestions
    
    def filter_tokens(self, event=None):
        """Filtrar tokens por tipo y búsqueda"""
        filter_type = self.filter_var.get()
        search_term = self.token_search_var.get().lower()
        
        # Limpiar tabla
        for item in self.tokens_tree.get_children():
            self.tokens_tree.delete(item)
        
        # Filtrar tokens
        filtered_tokens = []
        for token in self.current_tokens:
            # Filtro por tipo
            if filter_type != "Todos" and token.type.value != filter_type:
                continue
            
            # Filtro por búsqueda
            if search_term and search_term not in token.value.lower():
                continue
            
            filtered_tokens.append(token)
        
        # Mostrar tokens filtrados
        for i, token in enumerate(filtered_tokens):
            values = (
                token.line,
                token.column,
                token.type.value,
                token.value[:50] + ("..." if len(token.value) > 50 else ""),
                token.pattern_description
            )
            
            tags = ['oddrow' if i % 2 else 'evenrow', token.type.value]
            self.tokens_tree.insert('', tk.END, values=values, tags=tags)
        
        # Actualizar contador
        if filter_type == "Todos" and not search_term:
            self.token_count_var.set(f"Total: {len(self.current_tokens)} tokens")
        else:
            self.token_count_var.set(f"Mostrando: {len(filtered_tokens)} de {len(self.current_tokens)} tokens")
    
    def quick_search(self, event=None):
        """Búsqueda rápida de tokens"""
        search_term = self.search_entry.get()
        if not search_term or search_term == "Buscar token..." or not self.current_tokens:
            return
        
        matching_tokens = self.analyzer.find_tokens_by_pattern(self.current_tokens, search_term)
        
        if matching_tokens:
            # Mostrar resultados en una ventana emergente
            self.show_search_results(matching_tokens, search_term)
        else:
            messagebox.showinfo("Búsqueda", f"No se encontraron tokens que coincidan con '{search_term}'")
    
    def show_search_results(self, tokens, search_term):
        """Mostrar resultados de búsqueda"""
        results_window = tk.Toplevel(self.root)
        results_window.title(f"Resultados de búsqueda: '{search_term}'")
        results_window.geometry("600x400")
        
        # Lista de resultados
        listbox = tk.Listbox(results_window, font=('Consolas', 10))
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for token in tokens:
            listbox.insert(tk.END, f"Línea {token.line}: {token.value} ({token.type.value})")
        
        # Botón para cerrar
        ttk.Button(results_window, text="Cerrar", 
                  command=results_window.destroy).pack(pady=10)
    
    def reset_analysis(self):
        """Reiniciar análisis"""
        # Limpiar datos
        self.current_tokens = []
        self.current_errors = []
        self.current_language = ProgrammingLanguage.UNKNOWN
        self.analysis_stats = {}
        self.analysis_time = 0
        
        # Limpiar código fuente
        self.code_text.delete(1.0, tk.END)
        self.update_line_numbers()  # Actualizar números de línea
        
        # Limpiar interfaces
        for item in self.tokens_tree.get_children():
            self.tokens_tree.delete(item)
        
        # Limpiar textos y restaurar mensajes de bienvenida
        try:
            # Métricas
            if hasattr(self, 'metrics_text'):
                self.metrics_text.config(state=tk.NORMAL)
                self.metrics_text.delete(1.0, tk.END)
                self.metrics_text.insert(1.0, "No hay métricas disponibles\nRealice un análisis para ver estadísticas")
                self.metrics_text.config(state=tk.DISABLED)
            
            # Estadísticas generales
            if hasattr(self, 'general_stats_text'):
                self.general_stats_text.delete(1.0, tk.END)
                self.general_stats_text.insert(1.0, "Bienvenido al Analizador Léxico\nPara comenzar:\n1. Escriba o cargue código Python\n2. Haga clic en 'Analizar Código'\n3. Explore los resultados en las pestañas")
            
            # Distribución
            if hasattr(self, 'distribution_text'):
                self.distribution_text.delete(1.0, tk.END)
                self.distribution_text.insert(1.0, "No hay datos de distribución\nEjecute un análisis para ver la distribución de tokens")
            
            # Complejidad
            if hasattr(self, 'complexity_text'):
                self.complexity_text.delete(1.0, tk.END)
                self.complexity_text.insert(1.0, "No hay análisis de complejidad\nEjecute un análisis para ver métricas de complejidad")
            
            # Errores
            if hasattr(self, 'errors_text'):
                self.errors_text.delete(1.0, tk.END)
                self.errors_text.insert(1.0, "✅ No hay errores que mostrar\nLos errores aparecerán aquí después del análisis")
            
            # Patrones
            if hasattr(self, 'patterns_text'):
                self.patterns_text.delete(1.0, tk.END)
                self.patterns_text.insert(1.0, "No hay patrones detectados\nLos patrones de código aparecerán después del análisis")
            
            # Sugerencias
            if hasattr(self, 'suggestions_text'):
                self.suggestions_text.delete(1.0, tk.END)
                self.suggestions_text.insert(1.0, "No hay sugerencias disponibles\nLas recomendaciones aparecerán después del análisis")
                
        except Exception as e:
            print(f"Error al limpiar widgets: {e}")
        
        # Resetear variables
        self.language_label.config(text="No detectado")
        self.token_count_var.set("")
        self.filter_var.set("Todos")
        self.token_search_var.set("")
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, "Buscar token...")
        self.search_entry.configure(foreground='gray')
        self.analysis_time_var.set("")
        self.progress_var.set(0)
        
        self.status_var.set("🔄 Análisis reiniciado - Listo para nuevo código")
    
    def export_analysis(self):
        """Exportar análisis completo"""
        if not self.current_tokens:
            messagebox.showwarning("Advertencia", "No hay análisis para exportar")
            return
        
        # Opciones de exportación
        export_window = tk.Toplevel(self.root)
        export_window.title("Exportar Análisis")
        export_window.geometry("400x300")
        export_window.resizable(False, False)
        
        ttk.Label(export_window, text="Seleccione el formato de exportación:", 
                 font=('Segoe UI', 11, 'bold')).pack(pady=20)
        
        export_var = tk.StringVar(value="csv")
        
        options = [
            ("CSV - Lista de tokens", "csv"),
            ("JSON - Análisis completo", "json"),
            ("TXT - Reporte detallado", "txt")
        ]
        
        for text, value in options:
            ttk.Radiobutton(export_window, text=text, variable=export_var, 
                           value=value).pack(anchor=tk.W, padx=40, pady=5)
        
        def do_export():
            export_type = export_var.get()
            export_window.destroy()
            
            if export_type == "csv":
                self.export_csv()
            elif export_type == "json":
                self.export_json()
            elif export_type == "txt":
                self.export_txt()
        
        ttk.Button(export_window, text="Exportar", 
                  command=do_export).pack(pady=20)
        ttk.Button(export_window, text="Cancelar", 
                  command=export_window.destroy).pack()
    
    def export_csv(self):
        """Exportar a CSV"""
        filename = filedialog.asksaveasfilename(
            title="Exportar tokens a CSV",
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv")]
        )
        
        if filename:
            if self.analyzer.export_tokens_to_csv(self.current_tokens, filename):
                messagebox.showinfo("Éxito", f"Tokens exportados a {filename}")
            else:
                messagebox.showerror("Error", "No se pudo exportar el archivo")
    
    def export_json(self):
        """Exportar análisis completo a JSON"""
        filename = filedialog.asksaveasfilename(
            title="Exportar análisis a JSON",
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json")]
        )
        
        if filename:
            try:
                export_data = {
                    "metadata": {
                        "timestamp": datetime.now().isoformat(),
                        "analyzer_version": "2.0",
                        "language_detected": self.current_language.value,
                        "analysis_time": self.analysis_time
                    },
                    "tokens": [
                        {
                            "line": token.line,
                            "column": token.column,
                            "type": token.type.value,
                            "value": token.value,
                            "description": token.pattern_description
                        } for token in self.current_tokens
                    ],
                    "errors": self.current_errors,
                    "statistics": self.analysis_stats
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
                
                messagebox.showinfo("Éxito", f"Análisis exportado a {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar: {e}")
    
    def export_txt(self):
        """Exportar reporte detallado a TXT"""
        filename = filedialog.asksaveasfilename(
            title="Exportar reporte a TXT",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"REPORTE DE ANÁLISIS LÉXICO\n")
                    f.write(f"{'='*50}\n\n")
                    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Lenguaje detectado: {self.current_language.value}\n")
                    f.write(f"Tiempo de análisis: {self.analysis_time:.3f}s\n\n")
                    
                    # Estadísticas
                    f.write(self.generate_general_stats_text())
                    f.write("\n\n")
                    f.write(self.generate_distribution_text())
                    f.write("\n\n")
                    f.write(self.generate_complexity_text())
                    
                    # Errores
                    if self.current_errors:
                        f.write(f"\n\nERRORES ENCONTRADOS:\n")
                        f.write("-" * 30 + "\n")
                        for i, error in enumerate(self.current_errors, 1):
                            f.write(f"{i}. {error}\n")
                
                messagebox.showinfo("Éxito", f"Reporte exportado a {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar: {e}")
    
    def show_help(self):
        """Mostrar ayuda"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Ayuda - Analizador Léxico")
        help_window.geometry("700x500")
        
        help_text = scrolledtext.ScrolledText(help_window, font=('Consolas', 10))
        help_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        help_content = """🔍 ANALIZADOR LÉXICO AVANZADO v2.0
{'='*50}

📖 DESCRIPCIÓN:
Esta aplicación analiza código fuente y identifica todos los elementos léxicos (tokens)
presentes en el código, proporcionando estadísticas detalladas y análisis de complejidad.

⌨️ ATAJOS DE TECLADO:
• Ctrl+O: Abrir archivo
• Ctrl+S: Guardar archivo  
• F5: Analizar código
• Ctrl+R: Reiniciar análisis
• F1: Mostrar esta ayuda

🎯 CARACTERÍSTICAS PRINCIPALES:
• Soporte para Python, Java, C/C++ y JavaScript
• Detección automática de lenguaje
• Análisis de complejidad de código
• Exportación en múltiples formatos
• Búsqueda y filtrado de tokens
• Tema claro y oscuro
• Numeración de líneas
• Validación sintáctica básica

🔧 CÓMO USAR:
1. Escriba o cargue código en el área de texto
2. Presione "Analizar Código" o F5
3. Explore los resultados en las diferentes pestañas
4. Use los filtros para encontrar tokens específicos
5. Exporte los resultados si es necesario

🏷️ TIPOS DE TOKENS RECONOCIDOS:
• Palabras reservadas (keywords)
• Identificadores (variables, funciones)
• Números (enteros, decimales, hexadecimales)
• Cadenas de texto
• Operadores (+, -, *, /, ==, etc.)
• Delimitadores (paréntesis, llaves, etc.)
• Comentarios

💡 CONSEJOS:
• Use el tema oscuro para trabajar en ambientes con poca luz
• Los colores en la tabla de tokens ayudan a identificar tipos
• La búsqueda acepta expresiones regulares
• El análisis de complejidad ayuda a evaluar la calidad del código

🆘 SOPORTE:
Para reportar problemas o sugerir mejoras, consulte la documentación
del proyecto o contacte al desarrollador.

Versión: 2.0
Desarrollado con Python y Tkinter
"""
        
        help_text.insert(1.0, help_content)
        help_text.config(state=tk.DISABLED)
        
        # Botón para cerrar
        ttk.Button(help_window, text="Cerrar", 
                  command=help_window.destroy).pack(pady=10)
    
    def suggest_fixes(self):
        """Sugerir correcciones para errores"""
        if not self.current_errors:
            messagebox.showinfo("Información", "No hay errores para corregir")
            return
        
        # Ventana de sugerencias
        fixes_window = tk.Toplevel(self.root)
        fixes_window.title("Sugerencias de Corrección")
        fixes_window.geometry("600x400")
        
        fixes_text = scrolledtext.ScrolledText(fixes_window, font=('Consolas', 10))
        fixes_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        suggestions = "🔧 SUGERENCIAS DE CORRECCIÓN\\n\\n"
        
        for error in self.current_errors:
            suggestions += f"❌ Error: {error}\\n"
            
            if "no reconocido" in error.lower():
                suggestions += "💡 Sugerencia: Verifique la ortografía del token\\n"
            elif "sin cerrar" in error.lower():
                suggestions += "💡 Sugerencia: Agregue el delimitador de cierre correspondiente\\n"
            elif "sin" in error.lower() and "correspondiente" in error.lower():
                suggestions += "💡 Sugerencia: Verifique el balanceo de delimitadores\\n"
            else:
                suggestions += "💡 Sugerencia: Revise la sintaxis en la línea indicada\\n"
            
            suggestions += "\\n"
        
        fixes_text.insert(1.0, suggestions)
        fixes_text.config(state=tk.DISABLED)
        
        ttk.Button(fixes_window, text="Cerrar", 
                  command=fixes_window.destroy).pack(pady=10)
    
    # Métodos del menú contextual
    def show_context_menu(self, event):
        """Mostrar menú contextual"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def copy_token_value(self):
        """Copiar valor del token seleccionado"""
        selection = self.tokens_tree.selection()
        if selection:
            item = self.tokens_tree.item(selection[0])
            token_value = item['values'][3]  # El valor está en la columna 3
            self.root.clipboard_clear()
            self.root.clipboard_append(token_value)
            self.status_var.set(f"✂️ Copiado: '{token_value}'")
    
    def find_similar_tokens(self):
        """Buscar tokens similares"""
        selection = self.tokens_tree.selection()
        if selection:
            item = self.tokens_tree.item(selection[0])
            token_value = item['values'][3]
            
            # Filtrar por el valor del token
            self.token_search_var.set(token_value)
            self.filter_tokens()
            self.status_var.set(f"🔍 Buscando tokens similares a '{token_value}'")
    
    def go_to_line(self):
        """Ir a la línea del token seleccionado"""
        selection = self.tokens_tree.selection()
        if selection:
            item = self.tokens_tree.item(selection[0])
            line_number = item['values'][0]
            
            # Enfocar el editor de código y ir a la línea
            self.code_text.focus_set()
            self.code_text.mark_set("insert", f"{line_number}.0")
            self.code_text.see(f"{line_number}.0")
            self.status_var.set(f"📍 Navegando a línea {line_number}")
    
    def _on_search_focus_in(self, event):
        """Manejar cuando el campo de búsqueda recibe foco"""
        if self.search_entry.get() == "Buscar token...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.configure(foreground='black')
    
    def _on_search_focus_out(self, event):
        """Manejar cuando el campo de búsqueda pierde foco"""
        if not self.search_entry.get():
            self.search_entry.insert(0, "Buscar token...")
            self.search_entry.configure(foreground='gray')


def main():
    """Función principal mejorada"""
    root = tk.Tk()
    
    # Configurar la ventana principal
    root.state('zoomed') if os.name == 'nt' else root.attributes('-zoomed', True)
    
    app = ModernLexicalAnalyzerGUI(root)
    
    # Configurar el cierre de la aplicación
    def on_closing():
        if messagebox.askokcancel("Salir", "¿Está seguro que desea salir del analizador léxico?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Mostrar mensaje de bienvenida
    root.after(1000, lambda: app.status_var.set("🚀 Analizador Léxico Avanzado v2.0 - ¡Listo para usar!"))
    
    # Ejecutar la aplicación
    root.mainloop()


if __name__ == "__main__":
    main()