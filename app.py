import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# ───────────────────────────────────────────────────────────────
# Configuración de la página
# ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nueva Teoría del Comercio (Krugman)",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────────
# Título y descripción
# ──────────────────────────────────────────────────────────────
st.title("🌍 Nueva Teoría del Comercio (Krugman) - Interactiva")
st.markdown("""
Analiza el modelo de **Krugman** de comercio internacional con competencia monopolística 
y economías de escala internas.
- 🟢 **Costo Medio (CC)**: Curva de costos medios decreciente (economías de escala)
- 🟣 **Precio (PP)**: Curva de precio decreciente con el número de firmas
- ⚫ **Equilibrio**: Intersección CC = PP (precio y escala óptima)
""")

# ──────────────────────────────────────────────────────────────
# Parámetros base del modelo
# ──────────────────────────────────────────────────────────────
st.sidebar.header("⚙️ Parámetros Base")

# Curva CC: Costo Medio = F/Q + c
F_base = st.sidebar.number_input("Costos Fijos (F)", value=12.0, step=1.0, min_value=1.0)
c = st.sidebar.number_input("Costo Marginal (c)", value=1.5, step=0.1, min_value=0.1)

# Curva PP: Precio = a - b*Q
a_base = st.sidebar.number_input("Intercepto PP (a)", value=10.0, step=0.5)
b = st.sidebar.number_input("Pendiente PP (b)", value=0.8, step=0.1)

st.sidebar.markdown("---")

# ───────────────────────────────────────────────────────────────
# Desplazamientos de curvas
# ──────────────────────────────────────────────────────────────
st.sidebar.header("🔄 Desplazamientos de Curvas")

delta_F = st.sidebar.slider(
    "Desplazamiento CC (ΔF - Costos Fijos)",
    min_value=-8.0,
    max_value=8.0,
    value=0.0,
    step=0.5,
    format="%.1f"
)

delta_PP = st.sidebar.slider(
    "Desplazamiento PP (Δa - Precio)",
    min_value=-5.0,
    max_value=5.0,
    value=0.0,
    step=0.1,
    format="%.1f"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Leyenda:**")
st.sidebar.markdown("🟢 Verde = Costo Medio (CC)")
st.sidebar.markdown("🟣 Magenta = Precio (PP)")
st.sidebar.markdown("⚫ Negro = Punto de equilibrio")

# ───────────────────────────────────────────────────────────────
# Calcular curvas con desplazamientos
# ──────────────────────────────────────────────────────────────
Q = np.linspace(0.5, 9.5, 200)

# Parámetros actuales
F_actual = F_base + delta_F
a_actual = a_base + delta_PP

# Curva CC: Costo Medio = F/Q + c
CC = F_actual / Q + c

# Curva PP: Precio = a - b*Q
PP = a_actual - b * Q

# ───────────────────────────────────────────────────────────────
# Calcular punto de equilibrio
# ──────────────────────────────────────────────────────────────
# CC = PP → F/Q + c = a - b*Q
# b*Q² + (c - a)*Q + F = 0
# Q = [(a - c) ± sqrt((a-c)² - 4*b*F)] / (2*b)

discriminante = (a_actual - c)**2 - 4 * b * F_actual

if discriminante >= 0:
    Q_eq_1 = ((a_actual - c) + np.sqrt(discriminante)) / (2 * b)
    Q_eq_2 = ((a_actual - c) - np.sqrt(discriminante)) / (2 * b)
    
    # Tomar la solución positiva y realista
    Q_eq = Q_eq_1 if Q_eq_1 > 0 and Q_eq_1 < 10 else Q_eq_2
    P_eq = a_actual - b * Q_eq
    CC_eq = F_actual / Q_eq + c
else:
    Q_eq = None
    P_eq = None
    CC_eq = None

# Equilibrio original
disc_orig = (a_base - c)**2 - 4 * b * F_base
if disc_orig >= 0:
    Q_orig_1 = ((a_base - c) + np.sqrt(disc_orig)) / (2 * b)
    Q_orig_2 = ((a_base - c) - np.sqrt(disc_orig)) / (2 * b)
    Q_orig = Q_orig_1 if Q_orig_1 > 0 and Q_orig_1 < 10 else Q_orig_2
    P_orig = a_base - b * Q_orig
else:
    Q_orig = None
    P_orig = None

# ──────────────────────────────────────────────────────────────
# Mostrar métricas
# ──────────────────────────────────────────────────────────────
st.markdown("### 📊 Punto de Equilibrio")

if Q_eq is not None:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Escala de Producción (Q*)",
            value=f"{Q_eq:.2f}",
            delta=f"{Q_eq - Q_orig:+.2f}" if Q_orig else None
        )
    
    with col2:
        st.metric(
            label="Precio de Equilibrio (P*)",
            value=f"{P_eq:.2f}",
            delta=f"{P_eq - P_orig:+.2f}" if P_orig else None
        )
    
    with col3:
        st.metric(
            label="Costo Medio (CC*)",
            value=f"{CC_eq:.2f}"
        )
else:
    st.error("️ No hay equilibrio real con los parámetros actuales. Ajusta los valores.")

st.markdown("---")

# ───────────────────────────────────────────────────────────────
# Crear la gráfica
# ──────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 7))

# Grid
ax.grid(True, linestyle='--', alpha=0.6)
ax.set_axisbelow(True)

# Curva CC (verde sólida)
ax.plot(Q, CC, 'g-', linewidth=2.5, 
        label=f'Costo Medio (CC) [F={F_actual:.1f}]')

# Curva PP (magenta sólida)
ax.plot(Q, PP, 'm-', linewidth=2.5, 
        label=f'Precio (PP) [a={a_actual:.1f}]')

# Punto de equilibrio
if Q_eq is not None:
    ax.plot(Q_eq, P_eq, 'ko', markersize=12, 
            markeredgecolor='black', markerfacecolor='black', 
            markeredgewidth=2, zorder=10)
    
    # Líneas punteadas desde el equilibrio
    ax.axhline(y=P_eq, color='gray', linestyle=':', alpha=0.5, linewidth=1)
    ax.axvline(x=Q_eq, color='gray', linestyle=':', alpha=0.5, linewidth=1)
    
    # Etiqueta del punto de equilibrio
    ax.annotate(f'Eq. Original\n(Q={Q_eq:.1f}, P={P_eq:.1f})', 
                xy=(Q_eq, P_eq), 
                xytext=(Q_eq + 0.8, P_eq + 0.8),
                fontsize=10, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

# Configuración de ejes
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_xlabel('Escala de Producción (Q)', fontsize=13, fontweight='bold')
ax.set_ylabel('Precio / Costo (P/C)', fontsize=13, fontweight='bold')
ax.set_title('Nueva Teoría Comercio (Krugman)', 
             fontsize=15, fontweight='bold', pad=20)

# Leyenda
ax.legend(loc='upper right', fontsize=10, framealpha=0.9)

# Marcas en los ejes
ax.set_xticks(np.arange(0, 11, 2))
ax.set_yticks(np.arange(0, 11, 2))

plt.tight_layout()

# ───────────────────────────────────────────────────────────────
# Mostrar gráfica en Streamlit
# ─────────────────────────────────────────────────────────────
st.pyplot(fig)

# ───────────────────────────────────────────────────────────────
# Interpretación económica
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("###  Interpretación Económica")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🟢 Curva CC (Costo Medio)**")
    st.markdown(f"""
    - Ecuación: **CC = F/Q + c = {F_actual:.1f}/Q + {c:.1f}**
    - Representa **economías de escala internas**
    - A mayor producción (Q), menor costo medio
    - Los costos fijos (F) se diluyen entre más unidades
    """)
    
    if delta_F > 0:
        st.warning(f"""
        **️ Aumento de costos fijos** (ΔF = {delta_F:+.1f})
        
        **Causas:**
        - Mayor inversión en tecnología
        - Costos de entrada más altos
        - Regulaciones más estrictas
        
        **Efectos:**
        - CC se desplaza **hacia arriba**
        - Menos firmas en el mercado
        - Mayor precio de equilibrio
        - Menor escala de producción
        """)
    elif delta_F < 0:
        st.success(f"""
        **✅ Disminución de costos fijos** (ΔF = {delta_F:+.1f})
        
        **Causas:**
        - Avance tecnológico
        - Liberalización comercial
        - Reducción de barreras de entrada
        
        **Efectos:**
        - CC se desplaza **hacia abajo**
        - Más firmas en el mercado
        - Menor precio de equilibrio
        - Mayor escala de producción
        """)
    else:
        st.info("➡️ CC en posición original")

with col2:
    st.markdown("**🟣 Curva PP (Precio)**")
    st.markdown(f"""
    - Ecuación: **P = a - b*Q = {a_actual:.1f} - {b:.1f}*Q**
    - Representa la relación entre precio y número de firmas
    - A mayor competencia (más firmas), menor precio
    """)
    
    if delta_PP > 0:
        st.success(f"""
        **✅ Aumento de precio** (Δa = {delta_PP:+.1f})
        
        **Causas:**
        - Menor competencia
        - Aumento de preferencias por variedad
        - Integración de mercados (más consumidores)
        
        **Efectos:**
        - PP se desplaza **hacia arriba**
        - Mayor precio de equilibrio
        - Más firmas en el mercado
        """)
    elif delta_PP < 0:
        st.error(f"""
        **⬇️ Disminución de precio** (Δa = {delta_PP:+.1f})
        
        **Causas:**
        - Mayor competencia
        - Guerra de precios
        - Sustitutos más baratos
        
        **Efectos:**
        - PP se desplaza **hacia abajo**
        - Menor precio de equilibrio
        - Menos firmas en el mercado
        """)
    else:
        st.info("️ PP en posición original")

# ───────────────────────────────────────────────────────────────
# Análisis de comercio internacional
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🌍 Implicaciones para el Comercio Internacional")

st.markdown("""
El modelo de Krugman explica por qué países similares comercian entre sí 
(**comercio intraindustrial**) y por qué existe **variedad de productos**.
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**✨ Efectos del Libre Comercio:**")
    st.success("""
    1. **Mayor mercado** → Más consumidores
    2. **Más variedad** → Los consumidores tienen más opciones
    3. **Menor precio** → Competencia más intensa
    4. **Mayor escala** → Economías de escala más aprovechadas
    5. **Menos firmas domésticas** → Pero más variedad total
    """)

with col2:
    st.markdown("**🔄 Desplazamientos con Comercio:**")
    st.info("""
    - **CC se desplaza hacia abajo**: 
      - Costos fijos se diluyen en mercado más grande
      - Mayor escala de producción
    
    - **PP se desplaza hacia arriba**:
      - Mayor disposición a pagar por variedad
      - Más consumidores en el mercado integrado
    """)

# ───────────────────────────────────────────────────────────────
# Escenarios predefinidos
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🎯 Escenarios de Política Comercial")

scenario = st.selectbox(
    "Selecciona un escenario:",
    ["Selecciona...",
     "1. Apertura Comercial (Libre Comercio)",
     "2. Aumento de Costos Fijos (Barreras)",
     "3. Reducción de Costos Fijos (Tecnología)",
     "4. Mayor Competencia (↓ Precio)",
     "5. Menor Competencia (↑ Precio)",
     "6. Integración Económica Regional"]
)

if scenario == "1. Apertura Comercial (Libre Comercio)":
    st.success("🌐 **Libre Comercio:** Integración de mercados")
    st.markdown("- **CC se desplaza hacia abajo** (ΔF = -3.0)")
    st.markdown("  - Mayor mercado permite mayor escala")
    st.markdown("  - Costos fijos se diluyen más")
    st.markdown("- **PP se desplaza hacia arriba** (Δa = +1.5)")
    st.markdown("  - Más consumidores, mayor disposición a pagar")
    st.markdown("- **Resultado:** ↓P, ↑Q, ↑Variedad, ↑Bienestar")
    st.markdown(f"- **Sugerencia:** ΔF = -3.0, Δa = +1.5")

elif scenario == "2. Aumento de Costos Fijos (Barreras)":
    st.error(" **Barreras de entrada:** Regulaciones o costos altos")
    st.markdown("- **CC se desplaza hacia arriba** (ΔF = +4.0)")
    st.markdown("- Menos firmas pueden entrar al mercado")
    st.markdown("- **Resultado:** ↑P, ↓Q, ↓Variedad")
    st.markdown(f"- **Sugerencia:** ΔF = +4.0")

elif scenario == "3. Reducción de Costos Fijos (Tecnología)":
    st.success(" **Avance tecnológico:**")
    st.markdown("- **CC se desplaza hacia abajo** (ΔF = -4.0)")
    st.markdown("- Más firmas pueden entrar")
    st.markdown("- **Resultado:** ↓P, ↑Q, ↑Variedad")
    st.markdown(f"- **Sugerencia:** ΔF = -4.0")

elif scenario == "4. Mayor Competencia (↓ Precio)":
    st.info("📉 **Aumento de competencia:**")
    st.markdown("- **PP se desplaza hacia abajo** (Δa = -2.0)")
    st.markdown("- Más sustitutos disponibles")
    st.markdown("- **Resultado:** ↓P, ↓Q por firma, ↓Número de firmas")
    st.markdown(f"- **Sugerencia:** Δa = -2.0")

elif scenario == "5. Menor Competencia (↑ Precio)":
    st.warning(" **Menor competencia:**")
    st.markdown("- **PP se desplaza hacia arriba** (Δa = +2.0)")
    st.markdown("- Menos sustitutos, mayor poder de mercado")
    st.markdown("- **Resultado:** ↑P, ↑Q por firma, ↑Número de firmas")
    st.markdown(f"- **Sugerencia:** Δa = +2.0")

elif scenario == "6. Integración Económica Regional":
    st.success(" **Integración regional (UE, Mercosur, etc.):**")
    st.markdown("- Similar a apertura comercial pero más gradual")
    st.markdown("- **CC se desplaza hacia abajo** (ΔF = -2.0)")
    st.markdown("- **PP se desplaza hacia arriba** (Δa = +1.0)")
    st.markdown("- **Resultado:** ↑Comercio intraindustrial, ↑Variedad")
    st.markdown(f"- **Sugerencia:** ΔF = -2.0, Δa = +1.0")

# ───────────────────────────────────────────────────────────────
# Ecuaciones
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📐 Ecuaciones del Modelo")

col1, col2 = st.columns(2)

with col1:
    st.latex(rf"\text{{CC: }} P = \frac{{{F_actual:.1f}}}{{Q}} + {c:.1f}")

with col2:
    st.latex(rf"\text{{PP: }} P = {a_actual:.1f} - {b:.1f}Q")

if Q_eq is not None:
    st.markdown(f"""
    **Punto de equilibrio (CC = PP):**
    - Q* = {Q_eq:.2f}
    - P* = {P_eq:.2f}
    - CC* = {CC_eq:.2f}
    """)

# ──────────────────────────────────────────────────────────────
# Conceptos clave
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📖 Conceptos Clave del Modelo de Krugman")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**📉 Economías de Escala**")
    st.markdown("Costo medio decrece")
    st.markdown("con la producción")
    st.markdown("Curva CC descendente")
    st.markdown("Ventaja de producir en masa")

with col2:
    st.markdown("**🏪 Competencia Monopolística**")
    st.markdown("Muchas firmas")
    st.markdown("Productos diferenciados")
    st.markdown("Cada firma tiene poder")
    st.markdown("de mercado limitado")

with col3:
    st.markdown("**🌍 Comercio Intraindustrial**")
    st.markdown("Países similares")
    st.markdown("comercian entre sí")
    st.markdown("Intercambian variedades")
    st.markdown("del mismo producto")

# ───────────────────────────────────────────────────────────────
# Número de firmas en equilibrio
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🏭 Número de Firmas en Equilibrio")

if Q_eq is not None and Q_eq > 0:
    # En el modelo de Krugman: n = S / (Q * b) donde S es tamaño del mercado
    # Simplificado: n  1/Q (a menor escala por firma, más firmas)
    S = 100  # Tamaño del mercado (supuesto)
    n_firms = S / (Q_eq * 10)  # Normalizado
    
    st.markdown(f"""
    Con una escala de producción de **Q* = {Q_eq:.2f}** por firma:
    
    - **Número estimado de firmas:** n ≈ {n_firms:.1f}
    - **Variedad disponible:** {n_firms:.0f} productos diferentes
    """)
    
    if n_firms > 10:
        st.success("✅ **Alta competencia:** Muchas firmas, gran variedad para consumidores")
    elif n_firms > 5:
        st.info("📊 **Competencia moderada:** Balance entre variedad y escala")
    else:
        st.warning("⚠️ **Baja competencia:** Pocas firmas, limitada variedad")
