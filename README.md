# 🔍 Analizador Léxico de Python v2.0

> **Herramienta educativa para análisis léxico de código Python**  
> Interfaz gráfica moderna con análisis detallado, estadísticas y exportación

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-red.svg)
![Status](https://img.shields.io/badge/Status-Estable-brightgreen.svg)

---

## 🚀 **Instalación Rápida**

### **Requisitos:**
- Python 3.7 o superior
- Tkinter (incluido por defecto)

### **Pasos:**
1. Descargar los archivos:
   ```
   📄 lexical_analyzer.py
   📄 gui_analyzer_improved.py
   ```

2. Ejecutar:
   ```bash
   python gui_analyzer_improved.py
   ```

## ⚡ **Uso Rápido**

1. **📝 Escribir código** o usar "📁 Abrir" para cargar archivo
2. **🔍 Analizar** - Clic en "Analizar Código" 
3. **📊 Explorar** - Revisar pestañas de resultados
4. **📤 Exportar** - Guardar en CSV, JSON o TXT (opcional)

## ⌨️ **Atajos de Teclado**

|    Atajo   |     Función     |
|------------|-----------------|
| **Ctrl+O** | Abrir archivo   |
| **Ctrl+S** | Guardar archivo |
| **F5**     | Analizar código |
| **Ctrl+R** | Limpiar todo    |
| **F1**     | Ayuda           |

## 🏷️ **Características Principales**

- ✅ **Tokenización completa** - Identifica todos los elementos del código
- ✅ **10 tipos de tokens** - Keywords, strings, números, operadores, etc.
- ✅ **Análisis de errores** - Detección automática de problemas
- ✅ **Estadísticas detalladas** - Métricas de complejidad y distribución
- ✅ **Interfaz moderna** - Diseño limpio con números de línea
- ✅ **Exportación múltiple** - CSV, JSON y reportes TXT
- ✅ **Búsqueda avanzada** - Filtros y patrones regex

## 📊 **Tipos de Análisis**

### **🏷️ Tokens**
Tabla detallada con línea, columna, tipo y valor de cada token

### **📈 Estadísticas**  
- **General**: Métricas totales y resumen
- **Distribución**: Porcentajes por tipo de token
- **Complejidad**: Indicadores de calidad de código

### **⚠️ Errores**
Detección automática con sugerencias de corrección

### **🔬 Análisis**
Patrones detectados y recomendaciones de mejora

## 📤 **Formatos de Exportación**

| Formato     | Uso          | Descripción                       |
|-------------|--------------|-----------------------------------|
| **📊 CSV**  | Excel/Calc   | Tabla de tokens para análisis     |
| **📋 JSON** | Programático | Datos estructurados con metadatos |
| **📄 TXT**  | Reportes     | Documento legible para humanos    |

## 🛠️ **Solución de Problemas**

### **Error "Module not found"**
- Asegurar que ambos archivos `.py` estén en la misma carpeta
- Ejecutar desde el directorio correcto

### **Aplicación no inicia**
```bash
# Verificar Python
python --version

# Verificar Tkinter
python -c "import tkinter; print('OK')"
```

### **Análisis lento**
- Usar código de menos de 10,000 líneas
- Cerrar otras aplicaciones pesadas

## 📚 **Documentación Completa**

Para documentación técnica detallada, ver:
📄 **[DOCUMENTACION_ANALIZADOR_LEXICO.md](DOCUMENTACION_ANALIZADOR_LEXICO.md)**

Incluye:
- Arquitectura técnica completa
- API y métodos detallados  
- Patrones regex explicados
- Guía de desarrollo y extensión
- Casos de uso educativos
- Resolución de problemas avanzada

## 🎓 **Ejemplo de Código para Probar**

```python
def fibonacci(n):
    """Calcula fibonacci recursivamente"""
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Generar secuencia
numeros = [fibonacci(i) for i in range(10)]
print(f"Fibonacci: {numeros}")

# Clase ejemplo
class Calculadora:
    def __init__(self):
        self.historial = []
    
    def sumar(self, a, b):
        resultado = a + b
        self.historial.append(f"{a} + {b} = {resultado}")
        return resultado

# Uso
calc = Calculadora()
resultado = calc.sumar(5, 3)
print(f"Resultado: {resultado}")
```

## 📁 **Estructura del Proyecto**

```
📂 analizador/
├── 📄 lexical_analyzer.py           # Motor del analizador
├── 📄 gui_analyzer_improved.py     # Interfaz gráfica
├── 📄 README.md                     # Esta guía rápida
└── 📄 DOCUMENTACION_ANALIZADOR_LEXICO.md  # Documentación técnica
```

## 🎯 **¿Para Quién Es?**

- 🎓 **Estudiantes** - Aprender análisis léxico y compiladores
- 👨‍🏫 **Profesores** - Demostrar conceptos de compiladores  
- 👨‍💻 **Desarrolladores** - Analizar estructura de código Python
- 🔍 **Investigadores** - Estudiar patrones de código

## 🏆 **Características v2.0**

Esta versión incluye todas las correcciones y mejoras:

- ✅ **Botón limpiar corregido** - Borra código y datos completamente
- ✅ **Inicialización perfecta** - Sin errores en primera ejecución  
- ✅ **Exportación funcional** - CSV, JSON y TXT funcionando
- ✅ **Interfaz moderna** - Diseño profesional y responsivo
- ✅ **Documentación completa** - Manual técnico exhaustivo

---

## 📞 **Soporte**

- 📖 **Documentación**: Ver `DOCUMENTACION_ANALIZADOR_LEXICO.md`
- 🐛 **Bugs**: Reportar con código que causa el error
- 💡 **Sugerencias**: Describir funcionalidad deseada
- ❓ **Ayuda**: Usar F1 dentro de la aplicación

---

**¡Disfruta analizando código Python!** 🐍✨

> **Versión**: 2.0 | **Autor**: Z3R0-86 | **Licencia**: MIT