import re
from enum import Enum
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
import time

class TokenType(Enum):
    # Tipos de tokens específicos para Python y C
    KEYWORD = "PALABRA_RESERVADA"
    IDENTIFIER = "IDENTIFICADOR"
    NUMBER = "NUMERO"
    STRING = "CADENA"
    OPERATOR = "OPERADOR"
    DELIMITER = "DELIMITADOR"
    COMMENT = "COMENTARIO"
    PREPROCESSOR = "DIRECTIVA_PREPROCESADOR"  # Específico para C
    SPECIAL = "ESPECIAL"
    UNKNOWN = "DESCONOCIDO"

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int
    
    def __str__(self):
        return f"Token({self.type.value}, '{self.value}', {self.line}:{self.column})"
    
    @property
    def pattern_description(self):
        """Retorna la descripción del patrón que coincidió con este token"""
        patterns = {
            TokenType.KEYWORD: "Palabra reservada del lenguaje",
            TokenType.IDENTIFIER: "Nombre de variable, función o clase",
            TokenType.NUMBER: "Literal numérico (entero, decimal, hexadecimal)",
            TokenType.STRING: "Cadena de texto entre comillas",
            TokenType.OPERATOR: "Operador aritmético, lógico o de comparación",
            TokenType.DELIMITER: "Delimitador de estructura (paréntesis, llaves, etc.)",
            TokenType.COMMENT: "Comentario de código",
            TokenType.PREPROCESSOR: "Directiva del preprocesador (#include, #define)",
            TokenType.SPECIAL: "Carácter especial",
            TokenType.UNKNOWN: "Token no reconocido"
        }
        return patterns.get(self.type, "Descripción no disponible")

class ProgrammingLanguage(Enum):
    PYTHON = "Python"
    C = "C"
    UNKNOWN = "Desconocido"

class LexicalAnalyzer:
    def __init__(self):
        # Patrones optimizados para Python y C
        self.patterns = {
            # Comentarios (orden importante: procesamos primero)
            TokenType.COMMENT: [
                r'/\*[\s\S]*?\*/',        # Comentario bloque C /* */
                r'//.*',                  # Comentario línea C //
                r'#.*',                   # Comentario Python # (también #include)
                r'"""[\s\S]*?"""',        # Docstring Python triple comillas dobles
                r"'''[\s\S]*?'''",        # Docstring Python triple comillas simples
            ],
            
            # Directivas preprocesador C (después de comentarios)
            TokenType.PREPROCESSOR: [
                r'#include\s*<[^>]+>',    # #include <stdio.h>
                r'#include\s*"[^"]+"',    # #include "header.h"
                r'#define\s+\w+.*',       # #define MACRO value
                r'#ifdef\s+\w+',          # #ifdef DEBUG
                r'#ifndef\s+\w+',         # #ifndef HEADER_H
                r'#endif',                # #endif
                r'#if\s+.*',              # #if condition
                r'#else',                 # #else
                r'#undef\s+\w+',          # #undef MACRO
            ],
            
            # Cadenas de texto
            TokenType.STRING: [
                r'"([^"\\]|\\.)*"',       # Cadenas dobles con escape
                r"'([^'\\]|\\.)*'",       # Cadenas simples con escape
                r'f"([^"\\]|\\.)*"',      # f-strings Python
                r"f'([^'\\]|\\.)*'",      # f-strings Python comillas simples
                r'r"[^"]*"',              # raw strings Python
                r"r'[^']*'",              # raw strings Python comillas simples
            ],
            
            # Números
            TokenType.NUMBER: [
                r'\b0x[0-9A-Fa-f]+[LlUu]*\b',  # Hexadecimal con sufijos C
                r'\b0[0-7]+[LlUu]*\b',         # Octal con sufijos C
                r'\b\d+\.\d*[fFlL]?\b',        # Decimal con sufijos C/Python
                r'\b\d+[LlUu]*\b',             # Enteros con sufijos C
                r'\b\d+e[+-]?\d+\b',           # Notación científica
            ],
            
            # Operadores (orden por longitud descendente)
            TokenType.OPERATOR: [
                # Operadores de 3 caracteres
                r'<<=|>>=',
                # Operadores de 2 caracteres
                r'\+\+|--|<<|>>|<=|>=|==|!=|&&|\|\||->|\+=|-=|\*=|/=|%=|&=|\|=|\^=',
                # Operadores de 1 caracter
                r'[+\-*/%=<>!&|^~]',
            ],
            
            # Delimitadores
            TokenType.DELIMITER: [
                r'[(){}\[\];,.]'
            ],
            
            # Identificadores (después de números y operadores)
            TokenType.IDENTIFIER: [
                r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
            ]
        }
        
        # Palabras reservadas optimizadas para Python y C
        self.keywords = {
            ProgrammingLanguage.PYTHON: {
                # Palabras clave principales
                'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
                'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
                'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
                'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
                'try', 'while', 'with', 'yield',
                # Funciones built-in comunes
                'print', 'len', 'range', 'str', 'int', 'float', 'bool', 'list', 
                'dict', 'tuple', 'set', 'open', 'input', 'type', 'isinstance',
                'self', 'super', '__init__', '__main__'
            },
            
            ProgrammingLanguage.C: {
                # Tipos de datos
                'int', 'float', 'double', 'char', 'void', 'short', 'long', 
                'signed', 'unsigned', 'bool', 'size_t',
                # Palabras clave de control
                'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'default',
                'break', 'continue', 'return', 'goto',
                # Modificadores
                'static', 'extern', 'auto', 'register', 'const', 'volatile',
                'inline', 'restrict',
                # Estructuras
                'struct', 'union', 'enum', 'typedef',
                # Otros
                'sizeof', 'NULL', 'true', 'false',
                # Funciones de biblioteca estándar comunes
                'printf', 'scanf', 'malloc', 'free', 'strlen', 'strcpy', 'strcmp',
                'main', 'include', 'define'
            }
        }
        
        # Indicadores mejorados para detectar lenguaje
        self.language_indicators = {
            ProgrammingLanguage.PYTHON: [
                r'def\s+\w+\s*\(',          # definición función
                r'class\s+\w+\s*[:\(]',     # definición clase
                r'import\s+\w+',            # import
                r'from\s+\w+\s+import',     # from import
                r'print\s*\(',              # función print
                r'if\s+.*:',                # if con dos puntos
                r'elif\s+.*:',              # elif
                r'for\s+\w+\s+in\s+',       # for in
                r'with\s+.*:',              # with statement
                r'self\.',                  # self
                r'__\w+__',                 # métodos especiales
                r'#\s*.*',                  # comentarios #
                r'""".*?"""',               # docstrings
            ],
            
            ProgrammingLanguage.C: [
                r'#include\s*[<"]',         # includes
                r'int\s+main\s*\(',         # función main
                r'printf\s*\(',             # printf
                r'scanf\s*\(',              # scanf
                r'malloc\s*\(',             # malloc
                r'struct\s+\w+',            # estructuras
                r'/\*.*?\*/',               # comentarios /* */
                r'//.*',                    # comentarios //
                r'\w+\s*\*\s*\w+',          # punteros
                r'#define\s+',              # defines
                r'sizeof\s*\(',             # sizeof
                r'->',                      # acceso a miembro por puntero
                r'{\s*$',                   # llaves abiertas al final de línea
            ]
        }
    
    def detect_language(self, code: str) -> ProgrammingLanguage:
        """Detecta si el código es Python o C con mayor precisión"""
        scores = {ProgrammingLanguage.PYTHON: 0, ProgrammingLanguage.C: 0}
        
        # Verificar indicadores específicos
        for language, indicators in self.language_indicators.items():
            for pattern in indicators:
                matches = re.findall(pattern, code, re.MULTILINE | re.IGNORECASE)
                scores[language] += len(matches) * 2  # Mayor peso a indicadores
        
        # Verificar palabras clave
        words = re.findall(r'\b\w+\b', code)
        for word in words:
            for language, keywords in self.keywords.items():
                if word in keywords:
                    scores[language] += 1
        
        # Verificar patrones sintácticos específicos
        if ':' in code and re.search(r'if\s+.*:', code):
            scores[ProgrammingLanguage.PYTHON] += 5
        if '{' in code and '}' in code:
            scores[ProgrammingLanguage.C] += 3
        if re.search(r'#include', code):
            scores[ProgrammingLanguage.C] += 10
        if re.search(r'def\s+\w+', code):
            scores[ProgrammingLanguage.PYTHON] += 10
            
        # Retornar el lenguaje con mayor puntaje
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        return ProgrammingLanguage.UNKNOWN
    
    def tokenize(self, code: str) -> Tuple[List[Token], List[str], ProgrammingLanguage]:
        """Analiza el código y retorna tokens, errores y lenguaje detectado"""
        tokens = []
        errors = []
        language = self.detect_language(code)
        
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            column = 1
            i = 0
            
            while i < len(line):
                # Saltar espacios en blanco
                if line[i].isspace():
                    i += 1
                    column += 1
                    continue
                
                token_found = False
                
                # Verificar patrones en orden de prioridad
                for token_type, patterns in self.patterns.items():
                    for pattern in patterns:
                        match = re.match(pattern, line[i:])
                        if match:
                            value = match.group()
                            
                            # Verificar si es palabra reservada
                            if token_type == TokenType.IDENTIFIER:
                                if language != ProgrammingLanguage.UNKNOWN:
                                    if value in self.keywords[language]:
                                        token_type = TokenType.KEYWORD
                            
                            # Manejar directivas de preprocesador que parecen comentarios
                            if token_type == TokenType.COMMENT and value.startswith('#'):
                                if language == ProgrammingLanguage.C and any(directive in value for directive in 
                                    ['include', 'define', 'ifdef', 'ifndef', 'endif', 'if', 'else', 'undef']):
                                    token_type = TokenType.PREPROCESSOR
                            
                            tokens.append(Token(token_type, value, line_num, column))
                            i += len(value)
                            column += len(value)
                            token_found = True
                            break
                    
                    if token_found:
                        break
                
                # Si no se encontró ningún patrón válido
                if not token_found:
                    char = line[i]
                    tokens.append(Token(TokenType.UNKNOWN, char, line_num, column))
                    errors.append(f"Línea {line_num}, Columna {column}: Carácter no reconocido '{char}'")
                    i += 1
                    column += 1
        
        return tokens, errors, language
    
    def validate_syntax_basic(self, tokens: List[Token]) -> List[str]:
        """Validación básica de sintaxis para Python y C"""
        errors = []
        parentheses = []
        brackets = []
        braces = []
        
        for token in tokens:
            if token.value == '(':
                parentheses.append(token)
            elif token.value == ')':
                if not parentheses:
                    errors.append(f"Línea {token.line}: ')' sin '(' correspondiente")
                else:
                    parentheses.pop()
            elif token.value == '[':
                brackets.append(token)
            elif token.value == ']':
                if not brackets:
                    errors.append(f"Línea {token.line}: ']' sin '[' correspondiente")
                else:
                    brackets.pop()
            elif token.value == '{':
                braces.append(token)
            elif token.value == '}':
                if not braces:
                    errors.append(f"Línea {token.line}: '}}' sin '{{' correspondiente")
                else:
                    braces.pop()
        
        # Verificar delimitadores sin cerrar
        for token in parentheses:
            errors.append(f"Línea {token.line}: '(' sin cerrar")
        for token in brackets:
            errors.append(f"Línea {token.line}: '[' sin cerrar")
        for token in braces:
            errors.append(f"Línea {token.line}: '{{' sin cerrar")
        
        return errors
    
    def get_analysis_stats(self, tokens: List[Token]) -> Dict:
        """Genera estadísticas detalladas del análisis específicas para Python y C"""
        stats = {
            'total_tokens': len(tokens),
            'total_lines': max([token.line for token in tokens], default=0),
            'token_distribution': {},
            'unique_identifiers': set(),
            'keywords_used': set(),
            'language_features': {
                'functions_defined': 0,
                'classes_defined': 0,      # Python
                'structs_defined': 0,      # C
                'includes_used': 0,        # C
                'imports_used': 0,         # Python
                'loops_detected': 0,
                'conditionals': 0,
                'pointers_used': 0,        # C
                'preprocessor_directives': 0  # C
            }
        }
        
        # Análisis básico de tokens
        for token in tokens:
            token_type = token.type.value
            stats['token_distribution'][token_type] = stats['token_distribution'].get(token_type, 0) + 1
            
            if token.type == TokenType.IDENTIFIER:
                stats['unique_identifiers'].add(token.value)
            elif token.type == TokenType.KEYWORD:
                stats['keywords_used'].add(token.value)
            elif token.type == TokenType.PREPROCESSOR:
                stats['language_features']['preprocessor_directives'] += 1
        
        # Análisis de características del lenguaje
        token_values = [token.value for token in tokens]
        for i, token in enumerate(tokens):
            # Funciones
            if token.value == 'def' and i+1 < len(tokens):
                stats['language_features']['functions_defined'] += 1
            elif token.value in ['int', 'void', 'float', 'char', 'double'] and i+1 < len(tokens):
                if tokens[i+1].type == TokenType.IDENTIFIER:
                    # Posible definición de función en C
                    for j in range(i+2, min(i+5, len(tokens))):
                        if j < len(tokens) and tokens[j].value == '(':
                            stats['language_features']['functions_defined'] += 1
                            break
            
            # Clases (Python)
            if token.value == 'class':
                stats['language_features']['classes_defined'] += 1
            
            # Estructuras (C)
            if token.value == 'struct':
                stats['language_features']['structs_defined'] += 1
            
            # Imports (Python)
            if token.value in ['import', 'from']:
                stats['language_features']['imports_used'] += 1
            
            # Includes (C)
            if token.value.startswith('#include'):
                stats['language_features']['includes_used'] += 1
            
            # Bucles
            if token.value in ['for', 'while', 'do']:
                stats['language_features']['loops_detected'] += 1
            
            # Condicionales
            if token.value in ['if', 'switch']:
                stats['language_features']['conditionals'] += 1
            
            # Punteros (C)
            if token.value == '->' or (token.value == '*' and i+1 < len(tokens) 
                                      and tokens[i+1].type == TokenType.IDENTIFIER):
                stats['language_features']['pointers_used'] += 1
        
        # Convertir sets a listas para serialización
        stats['unique_identifiers'] = list(stats['unique_identifiers'])
        stats['keywords_used'] = list(stats['keywords_used'])
        
        return stats
    
    def export_tokens_to_csv(self, tokens: List[Token], filename: str) -> bool:
        """Exporta los tokens a un archivo CSV"""
        try:
            import csv
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Línea', 'Columna', 'Tipo', 'Valor', 'Descripción del Patrón'])
                for token in tokens:
                    writer.writerow([token.line, token.column, token.type.value, 
                                   token.value, token.pattern_description])
            return True
        except Exception as e:
            print(f"Error al exportar CSV: {e}")
            return False
    
    def find_tokens_by_pattern(self, tokens: List[Token], pattern: str) -> List[Token]:
        """Busca tokens que coincidan con un patrón regex"""
        matching_tokens = []
        try:
            regex_pattern = re.compile(pattern, re.IGNORECASE)
            for token in tokens:
                if regex_pattern.search(token.value):
                    matching_tokens.append(token)
        except re.error:
            pass  # Patrón inválido
        return matching_tokens