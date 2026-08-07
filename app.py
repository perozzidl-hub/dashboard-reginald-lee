import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Control de Gastos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuración global para gráficos Plotly
PLOTLY_CONFIG = {
    'displayModeBar': False,
    'responsive': True
}

# ---------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (DARK THEME PROFESIONAL)
# ---------------------------------------------------------
st.markdown("""
<style>
    .main {
        background-color: #111827;
        color: #F9FAFB;
    }
    .stApp {
        background-color: #111827;
    }
    .css-1d3con0, [data-testid="stSidebar"] {
        background-color: #1F2937 !important;
    }
    .custom-card {
        background-color: #1F2937;
        border-radius: 8px;
        padding: 16px;
        border-left: 4px solid #E61C24;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        margin-bottom: 12px;
    }
    .card-title {
        font-size: 0.82rem;
        color: #9CA3AF;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .card-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-top: 4px;
    }
    .main-header {
        background: linear-gradient(90deg, #1F2937 0%, #111827 100%);
        padding: 20px;
        border-radius: 8px;
        border-bottom: 3px solid #E61C24;
        margin-bottom: 20px;
    }
    .main-header h2 {
        color: #FFFFFF;
        margin: 0;
        font-size: 1.6rem;
    }
    .main-header p {
        color: #9CA3AF;
        margin: 5px 0 0 0;
        font-size: 0.9rem;
    }
    .chart-box-title {
        color: #F9FAFB;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# FUNCIONES AUXILIARES
# ---------------------------------------------------------
def formato_moneda(valor, con_decimales=False):
    if pd.isna(valor) or valor == 0:
        return "$ 0,00" if con_decimales else "$ 0"
    fmt = "{:,.2f}" if con_decimales else "{:,.0f}"
    res = fmt.format(valor)
    res = res.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"$ {res}"

def obtener_columna(df, posibles_nombres):
    for col in df.columns:
        clean_col = str(col).strip().upper()
        for pos in posibles_nombres:
            if clean_col == pos.strip().upper():
                return col
    return None

# ---------------------------------------------------------
# CARGA Y PROCESAMIENTO DE DATOS MULTI-HOJA
# ---------------------------------------------------------
@st.cache_data
def cargar_datos_multihoja(file):
    xls = pd.ExcelFile(file)
    hojas = xls.sheet_names

    # 1. Hoja Principal (Presupuesto y Gastos)
    df_main = pd.read_excel(xls, sheet_name=0)
    if 'MES' in df_main.columns:
        df_main['MES_DT'] = pd.to_datetime(df_main['MES'], errors='coerce')
        df_main['MES_NOMBRE'] = df_main['MES_DT'].dt.strftime('%Y-%m')
    for c in ['INTERNO', 'DES1', 'DES2', 'TEXTO INTERNO', 'DESC CTA CBLE', 'RAZON', 'COMPROBANTE']:
        if c in df_main.columns:
            df_main[c] = df_main[c].fillna('-')

    # 2. Hoja Vales de Consumo
    df_vales = pd.DataFrame()
    if len(hojas) > 1:
        df_vales = pd.read_excel(xls, sheet_name=1)
        if not df_vales.empty:
            df_vales.columns = [str(c).strip() for c in df_vales.columns]
            col_fecha_v = obtener_columna(df_vales, ['FECHA', 'MES', 'FEC CMPTE', 'FEC OP'])
            if col_fecha_v:
                df_vales['MES_DT'] = pd.to_datetime(df_vales[col_fecha_v], errors='coerce')
                df_vales['MES_NOMBRE'] = df_vales['MES_DT'].dt.strftime('%Y-%m')

    # 3. Hoja Compras
    df_compras = pd.DataFrame()
    if len(hojas) > 2:
        df_compras = pd.read_excel(xls, sheet_name=2)
        if not df_compras.empty:
            df_compras.columns = [str(c).strip() for c in df_compras.columns]
            col_fecha_c = obtener_columna(df_compras, ['FEC CMPTE', 'FEC OP', 'FEC PED', 'FECHA', 'MES'])
            if col_fecha_c:
                df_compras['MES_DT'] = pd.to_datetime(df_compras[col_fecha_c], errors='coerce')
                df_compras['MES_NOMBRE'] = df_compras['MES_DT'].dt.strftime('%Y-%m')

    return {'main': df_main, 'vales': df_vales, 'compras': df_compras}

# ---------------------------------------------------------
# SISTEMA DE AUTENTICACIÓN
# ---------------------------------------------------------
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = ''
if 'is_admin' not in st.session_state:
    st.session_state['is_admin'] = False

USERS = {
    'ADMINISTRADOR': {'pass': 'admin123', 'admin': True},
    'MANTENIMIENTO': {'pass': 'mante123', 'admin': False},
    'OPERACIONES': {'pass': 'opera123', 'admin': False},
    'LOGISTICA': {'pass': 'logis123', 'admin': False}
}

if not st.session_state['logged_in']:
    st.markdown("<h2 style='text-align: center; color: #FFFFFF;'>🔒 Control de Acceso al Dashboard</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        user_input = st.selectbox("Usuario:", [""] + list(USERS.keys()))
        pass_input = st.text_input("Contraseña:", type="password")
        if st.button("Iniciar Sesión", use_container_width=True):
            if user_input in USERS and USERS[user_input]['pass'] == pass_input:
                st.session_state['logged_in'] = True
                st.session_state['user'] = user_input
                st.session_state['is_admin'] = USERS[user_input]['admin']
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")
    st.stop()

# ---------------------------------------------------------
# BARRA LATERAL (SIDEBAR)
# ---------------------------------------------------------
st.sidebar.markdown(f"👤 **Usuario Activo:** `{st.session_state['user']}`")
st.sidebar.caption(f"🔑 Perfil: {'Administrador General' if st.session_state['is_admin'] else 'Usuario Sectorial'}")

if st.sidebar.button("🚪 Cerrar Sesión"):
    st.session_state['logged_in'] = False
    st.rerun()

st.sidebar.markdown("---")

# Carga de archivo
st.sidebar.subheader("📥 Actualizar Base de Datos")
uploaded_file = st.sidebar.file_uploader("Subir Excel Completo (Multi-hoja)", type=['xlsx'])

if uploaded_file:
    data_dict = cargar_datos_multihoja(uploaded_file)
else:
    try:
        data_dict = cargar_datos_multihoja("Base Dashboard.xlsx")
    except Exception as e:
        data_dict = None

st.sidebar.markdown("---")
st.sidebar.subheader("📌 Módulos de Control")

modulo_seleccionado = st.sidebar.radio(
    "Seleccione Vista:",
    ["📊 Presupuesto y Gastos", "🎟️ Vales de Consumo", "🛒 Compras"]
)

st.sidebar.markdown("---")

# ---------------------------------------------------------
# MÓDULO 1: PRESUPUESTO Y GASTOS (SECCIÓN ORIGINAL)
# ---------------------------------------------------------
if modulo_seleccionado == "📊 Presupuesto y Gastos":
    st.markdown(f"""
        <div class="main-header">
            <h2>📊 Dashboard de Control Presupuestario y Gastos</h2>
            <p>Análisis de Gastos Reales vs Presupuesto | Usuario: <b>{st.session_state['user']}</b></p>
        </div>
    """, unsafe_allow_html=True)

    if not data_dict or data_dict['main'].empty:
        st.warning("⚠️ No se han cargado datos principales. Suba el archivo 'Base Dashboard.xlsx'.")
        st.stop()

    df = data_dict['main'].copy()

    # Selección de Responsable según perfil
    if not st.session_state['is_admin']:
        user_resp = st.session_state['user']
        df_filtered = df[df['RESPONSABLE'].astype(str).str.upper() == user_resp]
    else:
        st.sidebar.subheader("🎯 Filtros Presupuesto")
        responsables = sorted(df['RESPONSABLE'].dropna().unique())
        selected_resp = st.sidebar.multiselect("Filtrar Responsables:", responsables, default=responsables)
        df_filtered = df[df['RESPONSABLE'].isin(selected_resp)]

    # Filtro de Meses
    if 'MES_NOMBRE' in df_filtered.columns:
        meses_disp = sorted(df_filtered['MES_NOMBRE'].dropna().unique())
        selected_meses = st.sidebar.multiselect("Filtrar Meses:", meses_disp, default=meses_disp)
        if selected_meses:
            df_filtered = df_filtered[df_filtered['MES_NOMBRE'].isin(selected_meses)]

    # Cálculo de Métricas Presupuestarias
    monto_presupuestado = df_filtered['IMPORTE BASE'].sum() if 'IMPORTE BASE' in df_filtered.columns else 0
    monto_real = df_filtered['REAL'].sum() if 'REAL' in df_filtered.columns else 0
    monto_desviacion = df_filtered['DESVIACION'].sum() if 'DESVIACION' in df_filtered.columns else (monto_presupuestado - monto_real)
    pct_ejecucion = (monto_real / monto_presupuestado * 100) if monto_presupuestado > 0 else 0

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f'<div class="custom-card"><div class="card-title">Presupuesto Asignado</div><div class="card-value">{formato_moneda(monto_presupuestado)}</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="custom-card"><div class="card-title">Gasto Real Ejecutado</div><div class="card-value">{formato_moneda(monto_real)}</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="custom-card"><div class="card-title">Desviación Presupuestaria</div><div class="card-value">{formato_moneda(monto_desviacion)}</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div class="custom-card"><div class="card-title">% Ejecución Presupuesto</div><div class="card-value">{pct_ejecucion:.1f}%</div></div>', unsafe_allow_html=True)

    # Gráficos
    col_g1, col_g2 = st.columns([1.2, 1])
    with col_g1:
        st.markdown('<div class="chart-box-title">📈 Comparativo Mensual: Presupuesto vs Real</div>', unsafe_allow_html=True)
        if 'MES_NOMBRE' in df_filtered.columns and 'IMPORTE BASE' in df_filtered.columns and 'REAL' in df_filtered.columns:
            df_monthly = df_filtered.groupby('MES_NOMBRE')[['IMPORTE BASE', 'REAL']].sum().reset_index()
            fig_monthly = px.bar(
                df_monthly, barmode='group', x='MES_NOMBRE', y=['IMPORTE BASE', 'REAL'],
                labels={'value': 'Monto ($)', 'variable': 'Concepto', 'MES_NOMBRE': 'Mes'},
                color_discrete_map={'IMPORTE BASE': '#4B5563', 'REAL': '#E61C24'}
            )
            fig_monthly.update_layout(
                autosize=True, paper_bgcolor='#1F2937', plot_bgcolor='#1F2937', font=dict(color='#FFFFFF'),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(gridcolor='#374151', tickfont=dict(color='#FFFFFF'), automargin=True),
                yaxis=dict(gridcolor='#374151', tickfont=dict(color='#FFFFFF'), automargin=True),
                height=320, margin=dict(l=15, r=15, t=15, b=25)
            )
            st.plotly_chart(fig_monthly, use_container_width=True, config=PLOTLY_CONFIG)

    with col_g2:
        st.markdown('<div class="chart-box-title">🏢 Gastos por Sector / Rubro</div>', unsafe_allow_html=True)
        if 'DES1' in df_filtered.columns and 'REAL' in df_filtered.columns:
            df_rubro = df_filtered.groupby('DES1')['REAL'].sum().reset_index().sort_values(by='REAL', ascending=True).tail(6)
            fig_rubro = px.bar(
                df_rubro, x='REAL', y='DES1', orientation='h',
                color_discrete_sequence=['#E61C24']
            )
            fig_rubro.update_layout(
                autosize=True, paper_bgcolor='#1F2937', plot_bgcolor='#1F2937', font=dict(color='#FFFFFF'),
                xaxis=dict(gridcolor='#374151', tickfont=dict(color='#FFFFFF'), automargin=True),
                yaxis=dict(gridcolor='#374151', tickfont=dict(color='#FFFFFF'), automargin=True),
                height=320, margin=dict(l=15, r=15, t=15, b=15), xaxis_title="", yaxis_title=""
            )
            st.plotly_chart(fig_rubro, use_container_width=True, config=PLOTLY_CONFIG)

    # Tabla Detallada
    st.markdown("---")
    st.markdown("### 🔍 Detalle General de Movimientos")
    search_term = st.text_input("🔎 Buscar en Gastos:", "")
    df_show = df_filtered.copy()
    if search_term:
        mask = df_show.astype(str).apply(lambda x: x.str.lower().str.contains(search_term.lower())).any(axis=1)
        df_show = df_show[mask]
    
    st.dataframe(df_show, use_container_width=True, height=380)

# ---------------------------------------------------------
# MÓDULO 2: VALES DE CONSUMO
# ---------------------------------------------------------
elif modulo_seleccionado == "🎟️ Vales de Consumo":
    st.markdown(f"""
        <div class="main-header">
            <h2>🎟️ Registro y Control de Vales de Consumo</h2>
            <p>Consumos Internos por Sector | Usuario: <b>{st.session_state['user']}</b></p>
        </div>
    """, unsafe_allow_html=True)

    df_vales = data_dict['vales'] if data_dict else pd.DataFrame()

    if df_vales.empty:
        st.info("ℹ️ No se encontraron datos en la pestaña de Vales de Consumo.")
    else:
        st.dataframe(df_vales, use_container_width=True, height=450)

# ---------------------------------------------------------
# MÓDULO 3: COMPRAS
# ---------------------------------------------------------
elif modulo_seleccionado == "🛒 Compras":
    st.markdown(f"""
        <div class="main-header">
            <h2>🛒 Gestión y Consulta de Compras</h2>
            <p>Histórico de Adquisiciones | Usuario: <b>{st.session_state['user']}</b></p>
        </div>
    """, unsafe_allow_html=True)

    df_compras = data_dict['compras'] if data_dict else pd.DataFrame()

    if df_compras.empty:
        st.info("ℹ️ No se encontraron datos en la pestaña de Compras.")
    else:
        col_monto_c = obtener_columna(df_compras, ['NETO_TOTAL_FACTURA', 'MONTO', 'TOTAL', 'IMPORTE'])
        col_prov_c = obtener_columna(df_compras, ['RAZ_SOCIAL', 'PROVEEDOR', 'RAZON SOCIAL'])
        col_mes_c = 'MES_NOMBRE' if 'MES_NOMBRE' in df_compras.columns else obtener_columna(df_compras, ['FEC CMPTE', 'FEC OP', 'FECHA', 'MES'])

        # Filtros Sidebar
        st.sidebar.subheader("🎯 Filtros de Compras")

        df_c_user = df_compras.copy()

        if col_mes_c and col_mes_c in df_c_user.columns:
            meses_c = sorted(df_c_user[col_mes_c].dropna().unique())
            f_mes_c = st.sidebar.multiselect("Filtrar Mes:", meses_c, default=meses_c)
            if f_mes_c:
                df_c_user = df_c_user[df_c_user[col_mes_c].isin(f_mes_c)]

        # Métricas
        compras_totales = len(df_c_user)
        monto_total_c = abs(pd.to_numeric(df_c_user[col_monto_c], errors='coerce').sum()) if col_monto_c else 0
        compra_maxima = abs(pd.to_numeric(df_c_user[col_monto_c], errors='coerce').max()) if col_monto_c and not df_c_user.empty else 0

        kc1, kc2, kc3 = st.columns(3)
        with kc1:
            st.markdown(f'<div class="custom-card"><div class="card-title">Monto Total de Compras</div><div class="card-value">{formato_moneda(monto_total_c, con_decimales=True)}</div></div>', unsafe_allow_html=True)
        with kc2:
            st.markdown(f'<div class="custom-card"><div class="card-title">Operaciones de Compra</div><div class="card-value">{compras_totales:,}</div></div>', unsafe_allow_html=True)
        with kc3:
            st.markdown(f'<div class="custom-card"><div class="card-title">Mayor Compra Registrada</div><div class="card-value">{formato_moneda(compra_maxima, con_decimales=True)}</div></div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🛍️ Listado General de Compras")

        search_c = st.text_input("🔎 Buscar en Compras:", "")
        df_c_render = df_c_user.copy()

        if search_c:
            mask_c = df_c_render.astype(str).apply(lambda x: x.str.lower().str.contains(search_c.lower())).any(axis=1)
            df_c_render = df_c_render[mask_c]

        st.dataframe(df_c_render, use_container_width=True, height=400)
