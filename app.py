import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Reginald Lee - Dashboard Presupuestario",
    page_icon="🥤",
    layout="wide",
    initial_sidebar_state="auto"
)

PLOTLY_CONFIG = {
    'responsive': True,
    'displayModeBar': False
}

# ---------------------------------------------------------
# ESTILOS CSS
# ---------------------------------------------------------
st.markdown("""
    <style>
    html, body, [class*="css"], .stApp {
        font-family: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
        text-rendering: optimizeLegibility !important;
    }

    .stApp {
        background-color: #0E1117 !important;
    }

    .sr-only, 
    [data-testid="stSidebar"] .sr-only, 
    div[data-baseweb="input"] span[class*="sr-only"],
    span[class*="sr-only"] {
        position: absolute !important;
        width: 1px !important;
        height: 1px !important;
        padding: 0 !important;
        margin: -1px !important;
        overflow: hidden !important;
        clip: rect(0, 0, 0, 0) !important;
        white-space: nowrap !important;
        border: 0 !important;
    }

    .chart-box-title {
        font-size: 16px !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        min-height: 48px;
        display: flex;
        align-items: center;
        margin-bottom: 8px;
        line-height: 1.2;
    }

    div[data-testid="stForm"] {
        background-color: #1A1D24 !important;
        border-radius: 16px !important;
        padding: 35px 30px !important;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4) !important;
        border-top: 5px solid #E61C24 !important;
        border-left: 1px solid #2D3139 !important;
        border-right: 1px solid #2D3139 !important;
        border-bottom: 1px solid #2D3139 !important;
        max-width: 400px;
        margin: 0 auto;
    }

    .login-title {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 22px !important;
        text-align: center;
        margin-top: 5px !important;
        margin-bottom: 2px !important;
        letter-spacing: -0.3px;
    }

    .login-subtitle {
        color: #9CA3AF !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        text-align: center;
        margin-bottom: 25px !important;
    }

    div[data-testid="stForm"] label p {
        color: #E5E7EB !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }

    div[data-testid="stForm"] div[data-baseweb="input"] {
        background-color: #262A33 !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
    }

    div[data-testid="stForm"] input {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        background-color: transparent !important;
    }

    div[data-testid="stForm"] input::placeholder {
        color: #6B7280 !important;
        -webkit-text-fill-color: #6B7280 !important;
    }

    div[data-testid="stForm"] button[kind="secondaryFormSubmit"] {
        background-color: #E61C24 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 12px 20px !important;
        width: 100% !important;
        margin-top: 15px !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stForm"] button[kind="secondaryFormSubmit"]:hover {
        background-color: #CC1219 !important;
        box-shadow: 0 4px 12px rgba(230, 28, 36, 0.4) !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
    }

    [data-testid="stFileUploader"] section {
        background-color: #1A1D24 !important;
        border: 1px dashed #374151 !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }

    [data-testid="stFileUploader"] section button {
        background-color: #262A33 !important;
        color: #FFFFFF !important;
        border: 1px solid #374151 !important;
        border-radius: 6px !important;
    }

    section[data-testid="stSidebar"] button {
        border-radius: 8px !important;
        border: 1px solid #374151 !important;
        background-color: #1F2937 !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    section[data-testid="stSidebar"] button:hover {
        background-color: #E61C24 !important;
        color: #FFFFFF !important;
        border-color: #E61C24 !important;
    }

    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"] {
        background-color: #1F2937 !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5) !important;
    }

    li[role="option"], div[role="option"] {
        color: #F3F4F6 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 8px 12px !important;
    }

    li[role="option"]:hover, div[role="option"]:hover {
        background-color: #E61C24 !important;
        color: #FFFFFF !important;
    }

    span[data-baseweb="tag"] {
        background-color: #E61C24 !important;
        border-radius: 4px !important;
    }
    
    span[data-baseweb="tag"] span {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    .main-header {
        background: linear-gradient(135deg, #111827 0%, #E61C24 100%);
        padding: 20px 25px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    .main-header h2 {
        color: #FFFFFF !important;
        margin: 0;
        font-weight: 800;
        font-size: 24px;
    }
    .main-header p {
        margin-top: 5px;
        color: #F3F4F6 !important;
        font-size: 13px;
        margin-bottom: 0;
    }

    .custom-card {
        background-color: #1F2937;
        border-radius: 12px !important;
        padding: 18px 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        border-top: 4px solid #E61C24;
        margin-bottom: 15px;
        min-height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .card-title {
        font-size: 12px;
        font-weight: 700;
        color: #9CA3AF !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    .card-value {
        font-size: 20px;
        font-weight: 800;
        color: #FFFFFF !important;
        margin-bottom: 2px;
    }
    .card-sub {
        font-size: 11px;
        font-weight: 600;
    }
    .text-red { color: #EF4444 !important; }
    .text-green { color: #10B981 !important; }

    div[data-testid="stPlotlyChart"] {
        background-color: #1F2937 !important;
        border-radius: 14px !important;
        padding: 10px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
        overflow: hidden !important;
    }

    .detail-popup {
        background-color: #2A2111 !important;
        border-left: 6px solid #D97706 !important;
        padding: 18px 22px !important;
        border-radius: 12px !important;
        margin: 15px 0 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }
    .detail-popup h5 {
        color: #F59E0B !important;
        font-weight: 800 !important;
        margin: 0 0 10px 0 !important;
        font-size: 16px !important;
    }
    .detail-popup p {
        font-size: 15px !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        margin: 0 !important;
        line-height: 1.5 !important;
    }
    .detail-popup small {
        color: #D1D5DB !important;
        font-size: 12px !important;
        font-weight: 600 !important;
    }
    .detail-popup hr {
        margin: 12px 0 !important;
        border-color: #78350F !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# FUNCIONES AUXILIARES Y LECTURA MULTI-HOJA
# ---------------------------------------------------------
def formato_moneda(valor, con_decimales=False):
    if pd.isna(valor):
        return "$ 0"
    if con_decimales:
        res = f"{valor:,.2f}"
    else:
        res = f"{valor:,.0f}"
    return "$ " + res.replace(',', 'X').replace('.', ',').replace('X', '.')

def obtener_columna(df, opciones):
    for op in opciones:
        for c in df.columns:
            if str(c).strip().upper() == op.upper():
                return c
    return None

@st.cache_data
def cargar_datos_multihoja(file):
    xls = pd.ExcelFile(file)
    hojas = xls.sheet_names

    # 1. Hoja Principal (Presupuesto y Gastos)
    df_main = pd.read_excel(xls, sheet_name=hojas[0])
    df_main.columns = [str(c).strip() for c in df_main.columns]
    
    if 'MES' in df_main.columns:
        df_main['MES_DT'] = pd.to_datetime(df_main['MES'], errors='coerce')
        df_main['MES_NOMBRE'] = df_main['MES_DT'].dt.strftime('%Y-%m')
    for c in ['INTERNO', 'DES1', 'DES2', 'TEXTO INTERNO', 'DESC CTA CBLE', 'RAZON', 'COMPROBANTE']:
        if c in df_main.columns:
            df_main[c] = df_main[c].fillna('-')

    # Normalizar columna de cuenta contable
    col_cta_m = obtener_columna(df_main, ['CUENTA', 'CTA CBLE', 'CUENTA CONTABLE', 'DESC CTA CBLE', 'CTA_CBLE'])
    if col_cta_m:
        df_main['CUENTA_NORMALIZADA'] = df_main[col_cta_m].astype(str).str.strip()

    # 2. Hoja Vales de Consumo
    df_vales = pd.DataFrame()
    nombre_hoja_vales = next((h for h in hojas if 'VALE' in h.upper()), None)
    if nombre_hoja_vales:
        df_vales = pd.read_excel(xls, sheet_name=nombre_hoja_vales)
    elif len(hojas) > 1:
        df_vales = pd.read_excel(xls, sheet_name=hojas[1])

    if not df_vales.empty:
        df_vales.columns = [str(c).strip() for c in df_vales.columns]
        col_fecha_v = obtener_columna(df_vales, ['FECHA', 'MES', 'FEC CMPTE', 'FEC OP'])
        if col_fecha_v:
            df_vales['MES_DT'] = pd.to_datetime(df_vales[col_fecha_v], errors='coerce')
            df_vales['MES_NOMBRE'] = df_vales['MES_DT'].dt.strftime('%Y-%m')
            
        col_cta_v = obtener_columna(df_vales, ['DESC CTA CBLE', 'CUENTA', 'CTA CBLE', 'CUENTA CONTABLE', 'CONCEPTO', 'CATEGORIA'])
        if col_cta_v:
            df_vales['CUENTA_NORMALIZADA'] = df_vales[col_cta_v].astype(str).str.strip()

    # 3. Hoja Compras
    df_compras = pd.DataFrame()
    nombre_hoja_compras = next((h for h in hojas if 'COMPRA' in h.upper()), None)
    if nombre_hoja_compras:
        df_compras = pd.read_excel(xls, sheet_name=nombre_hoja_compras)
    elif len(hojas) > 2:
        df_compras = pd.read_excel(xls, sheet_name=hojas[2])

    if not df_compras.empty:
        df_compras.columns = [str(c).strip() for c in df_compras.columns]
        col_fecha_c = obtener_columna(df_compras, ['FECHA', 'MES', 'FEC CMPTE', 'FEC OP'])
        if col_fecha_c:
            df_compras['MES_DT'] = pd.to_datetime(df_compras[col_fecha_c], errors='coerce')
            df_compras['MES_NOMBRE'] = df_compras['MES_DT'].dt.strftime('%Y-%m')

        col_cta_c = obtener_columna(df_compras, ['DESC CTA CBLE', 'CUENTA', 'CTA CBLE', 'CUENTA CONTABLE', 'CONCEPTO'])
        if col_cta_c:
            df_compras['CUENTA_NORMALIZADA'] = df_compras[col_cta_c].astype(str).str.strip()

    return {'main': df_main, 'vales': df_vales, 'compras': df_compras}

@st.cache_data
def obtener_base_inicial():
    try:
        return cargar_datos_multihoja("Base Dashboard.xlsx")
    except Exception:
        return None

def obtener_cuentas_de_responsables(df_main, lista_responsables):
    """Devuelve el conjunto de cuentas contables (serie 6) asignadas a los responsables indicados"""
    if df_main.empty or 'RESPONSABLE' not in df_main.columns:
        return set()
    
    resps_upper = [str(r).upper() for r in lista_responsables]
    mask_resp = df_main['RESPONSABLE'].astype(str).str.upper().isin(resps_upper)
    
    col_cta_name = 'DESC CTA CBLE' if 'DESC CTA CBLE' in df_main.columns else 'CUENTA_NORMALIZADA'
    if col_cta_name in df_main.columns:
        cuentas = df_main[mask_resp][col_cta_name].dropna().unique()
        return set([str(c).strip() for c in cuentas])
    return set()

# Estado de sesión
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = None
if 'is_admin' not in st.session_state:
    st.session_state['is_admin'] = False
if 'df_data' not in st.session_state:
    st.session_state['df_data'] = obtener_base_inicial()

# ---------------------------------------------------------
# LOGIN SCREEN
# ---------------------------------------------------------
if not st.session_state['logged_in']:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 1.1, 1])
    
    with col_l2:
        with st.form("login_form"):
            st.markdown("""
                <div style="text-align: center; font-size: 55px; margin-bottom: 10px; line-height: 1;">
                    🥤
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="login-title">Reginald Lee S.A.</div>', unsafe_allow_html=True)
            st.markdown('<div class="login-subtitle">Plataforma de Control Presupuestario</div>', unsafe_allow_html=True)
            
            user_input = st.text_input("Usuario (Responsable)", placeholder="Ej: amores o admin").strip()
            pass_input = st.text_input("Contraseña", type="password").strip()
            submit_login = st.form_submit_button("🔑 Ingresar al Dashboard")
            
            if submit_login:
                if user_input and pass_input:
                    data_dict = st.session_state['df_data']
                    
                    if user_input.lower() == "admin" and pass_input == "admin@":
                        st.session_state['logged_in'] = True
                        st.session_state['user'] = "ADMINISTRADOR"
                        st.session_state['is_admin'] = True
                        st.rerun()
                    elif data_dict is not None and not data_dict['main'].empty:
                        df_m = data_dict['main']
                        responsables = [str(r).upper() for r in df_m['RESPONSABLE'].dropna().unique()]
                        u_upper = user_input.upper()
                        pass_esperado = user_input.lower() + "@"
                        
                        if u_upper in responsables and pass_input == pass_esperado:
                            st.session_state['logged_in'] = True
                            st.session_state['user'] = u_upper
                            st.session_state['is_admin'] = False
                            st.rerun()
                        else:
                            st.error("❌ Credenciales inválidas.")
                    else:
                        st.error("⚠️ Base de datos no disponible.")
                else:
                    st.warning("Ingrese usuario y contraseña.")
    st.stop()

# ---------------------------------------------------------
# NAVEGACIÓN Y SIDEBAR GLOBAL
# ---------------------------------------------------------
data_dict = st.session_state['df_data']

st.sidebar.markdown(f"👤 **Usuario Activo:** `{st.session_state['user']}`")
if st.session_state['is_admin']:
    st.sidebar.caption("🔑 Perfil: Administrador General")
else:
    st.sidebar.caption("📊 Perfil: Responsable de Sector")

if st.sidebar.button("🚪 Cerrar Sesión"):
    st.session_state['logged_in'] = False
    st.session_state['user'] = None
    st.session_state['is_admin'] = False
    st.rerun()

st.sidebar.markdown("---")

# Carga de archivos para Administrador
if st.session_state['is_admin']:
    st.sidebar.subheader("📤 Actualizar Base de Datos")
    new_file = st.sidebar.file_uploader("Subir Excel Completo (Multi-hoja)", type=["xlsx"])
    if new_file is not None:
        st.session_state['df_data'] = cargar_datos_multihoja(new_file)
        data_dict = st.session_state['df_data']
        st.sidebar.success("✅ Base de datos actualizada")

# Selector de Módulo Principal
st.sidebar.subheader("📌 Módulos de Control")
modulo_seleccionado = st.sidebar.radio(
    "Seleccione Vista:",
    ["📊 Presupuesto y Gastos", "🎟️ Vales de Consumo", "🛒 Compras"],
    index=0
)

# ---------------------------------------------------------
# MÓDULO 1: PRESUPUESTO Y GASTOS
# ---------------------------------------------------------
if modulo_seleccionado == "📊 Presupuesto y Gastos":
    st.markdown(f"""
        <div class="main-header">
            <h2>📊 Control de Presupuesto y Gastos Fijos</h2>
            <p>Reginald Lee S.A. | Vista Ejecutiva — Usuario: <b>{st.session_state['user']}</b></p>
        </div>
    """, unsafe_allow_html=True)

    df_main = data_dict['main'] if data_dict else pd.DataFrame()

    if not df_main.empty:
        if not st.session_state['is_admin']:
            df_user = df_main[df_main['RESPONSABLE'].astype(str).str.upper() == st.session_state['user']]
        else:
            df_user = df_main.copy()

        st.sidebar.subheader("🎯 Filtros Presupuestarios")
        meses_disp = sorted(df_user['MES_NOMBRE'].dropna().unique())
        locs_disp = sorted(df_user['LOCACION'].dropna().unique())
        grupos_disp = sorted(df_user['GRUPO DE CUENTAS'].dropna().unique())

        f_mes = st.sidebar.multiselect("Meses", meses_disp, default=meses_disp)
        f_loc = st.sidebar.multiselect("Locación / Planta", locs_disp, default=locs_disp)
        f_grupo = st.sidebar.multiselect("Grupo de Cuentas", grupos_disp, default=grupos_disp)

        if st.session_state['is_admin']:
            resps_disp = sorted(df_user['RESPONSABLE'].dropna().unique())
            f_resp = st.sidebar.multiselect("Responsable Sector", resps_disp, default=resps_disp)
        else:
            f_resp = [st.session_state['user']]

        df_f = df_user[
            (df_user['MES_NOMBRE'].isin(f_mes)) &
            (df_user['LOCACION'].isin(f_loc)) &
            (df_user['GRUPO DE CUENTAS'].isin(f_grupo)) &
            (df_user['RESPONSABLE'].astype(str).str.upper().isin(f_resp))
        ]

        presupuesto_df = df_f[df_f['TIPO2'] == 'PRESUPUESTO']
        gasto_df = df_f[df_f['TIPO2'] == 'GASTO']

        tot_presupuesto = presupuesto_df['SALDO'].sum()
        tot_gasto = abs(gasto_df['SALDO'].sum())
        desviacion = tot_gasto - tot_presupuesto
        pct_ejecucion = (tot_gasto / tot_presupuesto * 100) if tot_presupuesto > 0 else 0

        # KPIs
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f'<div class="custom-card"><div class="card-title">Presupuesto Asignado</div><div class="card-value">{formato_moneda(tot_presupuesto)}</div></div>', unsafe_allow_html=True)
        with k2:
            st.markdown(f'<div class="custom-card"><div class="card-title">Gasto Real Ejecutado</div><div class="card-value">{formato_moneda(tot_gasto)}</div></div>', unsafe_allow_html=True)
        with k3:
            sub_color = "text-red" if desviacion > 0 else "text-green"
            st.markdown(f'<div class="custom-card"><div class="card-title">Desviación Presupuestaria</div><div class="card-value">{formato_moneda(desviacion)}</div><div class="card-sub {sub_color}">Diferencia acumulada</div></div>', unsafe_allow_html=True)
        with k4:
            st.markdown(f'<div class="custom-card"><div class="card-title">% Ejecución Presupuestaria</div><div class="card-value">{pct_ejecucion:.1f}%</div><div class="card-sub text-red" style="visibility: {"visible" if pct_ejecucion > 100 else "hidden"};">Excedido de Presupuesto</div></div>', unsafe_allow_html=True)

        # Gráficos
        col_g1, col_g2, col_g3 = st.columns([1.3, 1.1, 1.0])
        with col_g1:
            st.markdown('<div class="chart-box-title">📅 Presupuesto vs Real por Mes</div>', unsafe_allow_html=True)
            p_mes = presupuesto_df.groupby('MES_NOMBRE')['SALDO'].sum().reset_index().rename(columns={'SALDO': 'Presupuesto'})
            g_mes = gasto_df.groupby('MES_NOMBRE')['SALDO'].apply(lambda x: abs(x.sum())).reset_index().rename(columns={'SALDO': 'Gasto Real'})
            comp_mes = pd.merge(p_mes, g_mes, on='MES_NOMBRE', how='outer').fillna(0)

            fig_mes = go.Figure()
            fig_mes.add_trace(go.Bar(x=comp_mes['MES_NOMBRE'], y=comp_mes['Presupuesto'], name='Presupuesto', marker_color='#9CA3AF'))
            fig_mes.add_trace(go.Bar(x=comp_mes['MES_NOMBRE'], y=comp_mes['Gasto Real'], name='Gasto Real', marker_color='#E61C24'))
            fig_mes.update_layout(
                autosize=True, paper_bgcolor='#1F2937', plot_bgcolor='#1F2937', font=dict(color='#FFFFFF'),
                xaxis=dict(gridcolor='#374151', tickfont=dict(color='#FFFFFF', size=11), automargin=True),
                yaxis=dict(gridcolor='#374151', tickfont=dict(color='#FFFFFF', size=11), automargin=True),
                barmode='group', height=310, margin=dict(l=20, r=15, t=10, b=30),
                legend=dict(orientation="h", y=1.18, x=0, font=dict(color='#FFFFFF', size=11))
            )
            st.plotly_chart(fig_mes, use_container_width=True, config=PLOTLY_CONFIG)

        with col_g2:
            st.markdown('<div class="chart-box-title">📊 Gasto por Grupo de Cuentas</div>', unsafe_allow_html=True)
            g_grupo = gasto_df.groupby('GRUPO DE CUENTAS')['SALDO'].apply(lambda x: abs(x.sum())).reset_index().sort_values(by='SALDO', ascending=True).tail(7)
            fig_grupo = px.bar(g_grupo, x='SALDO', y='GRUPO DE CUENTAS', orientation='h', color_discrete_sequence=['#E61C24'])
            fig_grupo.update_layout(
                autosize=True, paper_bgcolor='#1F2937', plot_bgcolor='#1F2937', font=dict(color='#FFFFFF'),
                xaxis=dict(gridcolor='#374151', tickfont=dict(color='#FFFFFF', size=11), automargin=True),
                yaxis=dict(gridcolor='#374151', tickfont=dict(color='#FFFFFF', size=10), automargin=True),
                height=310, margin=dict(l=10, r=15, t=10, b=25), xaxis_title="", yaxis_title=""
            )
            st.plotly_chart(fig_grupo, use_container_width=True, config=PLOTLY_CONFIG)

        with col_g3:
            st.markdown('<div class="chart-box-title">🎯 Nivel de Ejecución</div>', unsafe_allow_html=True)
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number", value = pct_ejecucion,
                number = {'suffix': "%", 'font': {'size': 26, 'color': '#FFFFFF'}},
                gauge = {
                    'axis': {'range': [0, max(120, pct_ejecucion)], 'tickcolor': "#FFFFFF", 'tickfont': {'color': '#FFFFFF', 'size': 11}},
                    'bar': {'color': "#E61C24" if pct_ejecucion > 100 else "#9CA3AF"},
                    'steps': [
                        {'range': [0, 80], 'color': "#374151"},
                        {'range': [80, 100], 'color': "#4B5563"},
                        {'range': [100, max(120, pct_ejecucion)], 'color': "#991B1B"}
                    ]
                }
            ))
            fig_gauge.update_layout(
                autosize=True, paper_bgcolor='#1F2937', plot_bgcolor='#1F2937', font=dict(color='#FFFFFF'),
                height=310, margin=dict(l=35, r=35, t=35, b=25)
            )
            st.plotly_chart(fig_gauge, use_container_width=True, config=PLOTLY_CONFIG)

        # Fila 2
        c_r2_1, c_r2_2 = st.columns([1, 1.5])
        with c_r2_1:
            st.markdown('<div class="chart-box-title">🏢 Gastos por Locación</div>', unsafe_allow_html=True)
            g_loc = gasto_df.groupby('LOCACION')['SALDO'].apply(lambda x: abs(x.sum())).reset_index()
            fig_loc = px.pie(g_loc, values='SALDO', names='LOCACION', hole=0.4, color_discrete_sequence=['#E61C24', '#6B7280', '#9CA3AF', '#D1D5DB', '#374151'])
            fig_loc.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(color='#FFFFFF'))
            fig_loc.update_layout(
                autosize=True, paper_bgcolor='#1F2937', plot_bgcolor='#1F2937', font=dict(color='#FFFFFF'),
                height=300, margin=dict(l=15, r=15, t=15, b=15), legend=dict(font=dict(color='#FFFFFF'))
            )
            st.plotly_chart(fig_loc, use_container_width=True, config=PLOTLY_CONFIG)

        with c_r2_2:
            st.markdown('<div class="chart-box-title">⚠️ Cuentas con Mayor Desviación</div>', unsafe_allow_html=True)
            p_cta = presupuesto_df.groupby('DESC CTA CBLE')['SALDO'].sum().rename('Presupuesto')
            g_cta = gasto_df.groupby('DESC CTA CBLE')['SALDO'].apply(lambda x: abs(x.sum())).rename('Gasto Real')
            comp_cta = pd.concat([p_cta, g_cta], axis=1).fillna(0)
            comp_cta['Desviacion'] = comp_cta['Gasto Real'] - comp_cta['Presupuesto']
            top_desv = comp_cta.sort_values(by='Desviacion', ascending=False).head(5).reset_index()

            fig_desv = px.bar(top_desv, x='Desviacion', y='DESC CTA CBLE', orientation='h', color='Desviacion', color_continuous_scale=['#6B7280', '#E61C24'])
            fig_desv.update_layout(
                autosize=True, paper_bgcolor='#1F2937', plot_bgcolor='#1F2937', font=dict(color='#FFFFFF'),
                xaxis=dict(gridcolor='#374151', tickfont=dict(color='#FFFFFF'), automargin=True),
                yaxis=dict(gridcolor='#374151', tickfont=dict(color='#FFFFFF'), automargin=True),
                height=300, margin=dict(l=15, r=15, t=15, b=15), xaxis_title="Desviación en $", yaxis_title=""
            )
            st.plotly_chart(fig_desv, use_container_width=True, config=PLOTLY_CONFIG)

        # Auditoría Transaccional
        st.markdown("---")
        st.markdown("### 🔍 Consulta y Auditoría Transaccional de Gastos")

        df_auditoria = gasto_df.copy()
        cuentas_unicas = sorted(df_auditoria['DESC CTA CBLE'].dropna().unique())
        col_f1, col_f2 = st.columns([2, 1])
        with col_f1:
            f_cuentas_tabla = st.multiselect("🔎 Filtrar por Cuenta Contable:", cuentas_unicas, default=[])
        with col_f2:
            search_kw = st.text_input("💬 Buscar por Proveedor / N° Interno:", "")

        if f_cuentas_tabla:
            df_auditoria = df_auditoria[df_auditoria['DESC CTA CBLE'].isin(f_cuentas_tabla)]
        if search_kw:
            sk = search_kw.lower()
            mask = (
                df_auditoria['DES1'].astype(str).str.lower().str.contains(sk) |
                df_auditoria['INTERNO'].astype(str).str.lower().str.contains(sk) |
                df_auditoria['TEXTO INTERNO'].astype(str).str.lower().str.contains(sk)
            )
            df_auditoria = df_auditoria[mask]

        df_auditoria['MONTO_MOSTRAR'] = df_auditoria['SALDO'] * -1
        df_auditoria['MONTO_FORMATO'] = df_auditoria['MONTO_MOSTRAR'].apply(lambda v: formato_moneda(v, con_decimales=True))

        cols_tabla = ['FECHA', 'MES_NOMBRE', 'LOCACION', 'RESPONSABLE', 'GRUPO DE CUENTAS', 'DESC CTA CBLE', 'DES1', 'INTERNO', 'MONTO_FORMATO']
        df_render = df_auditoria[cols_tabla].rename(columns={
            'MES_NOMBRE': 'MES', 'DESC CTA CBLE': 'CUENTA CONTABLE', 'DES1': 'PROVEEDOR / ENTIDAD', 'INTERNO': 'N° INTERNO', 'MONTO_FORMATO': 'MONTO ($)'
        })
        st.dataframe(df_render, use_container_width=True, height=380)

        # Inspector
        st.markdown("#### 📌 Inspeccionar 'Texto Interno' de un Gasto Específico")
        if not df_auditoria.empty:
            opciones_inspeccion = df_auditoria.apply(
                lambda r: f"ID {r.name} | {r['FECHA']} | {r['DES1']} | {formato_moneda(r['MONTO_MOSTRAR'], con_decimales=True)} | {r['DESC CTA CBLE']}", axis=1
            ).tolist()
            selected_option = st.selectbox("Seleccione una transacción para desplegar su detalle completo:", opciones_inspeccion)
            if selected_option:
                selected_id = int(selected_option.split(" | ")[0].replace("ID ", ""))
                item_row = df_auditoria.loc[selected_id]
                st.markdown(f"""
                    <div class="detail-popup">
                        <h5>📝 Texto Interno / Detalle Completo de la Compra</h5>
                        <p>"{item_row['TEXTO INTERNO']}"</p>
                        <hr>
                        <small><b>Proveedor:</b> {item_row['DES1']} | <b>Cuenta:</b> {item_row['DESC CTA CBLE']} | <b>N° Interno:</b> {item_row['INTERNO']} | <b>Comprobante:</b> {item_row['COMPROBANTE']}</small>
                    </div>
                """, unsafe_allow_html=True)

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

    df_main = data_dict['main'] if data_dict else pd.DataFrame()
    df_vales = data_dict['vales'] if data_dict else pd.DataFrame()

    if df_vales.empty:
        st.info("ℹ️ No se encontraron datos en la pestaña de 'Vales de Consumo'. Asegúrese de agregar la hoja al Excel.")
    else:
        # ---------------------------------------------------------
        # 1. CRUCE LÓGICO DE INFORMACIÓN (MAIN <-> VALES)
        # ---------------------------------------------------------
        # Mapear columnas clave en hoja Main
        col_m_num_cta = obtener_columna(df_main, ['CUENTA', 'CTA CBLE', 'CUENTA CONTABLE', 'NRO CUENTA', 'CODIGO'])
        col_m_nom_cta = obtener_columna(df_main, ['DESC CTA CBLE', 'DESCRIPCION CUENTA', 'NOMBRE CUENTA', 'CUENTA_NORMALIZADA'])
        col_m_resp = 'RESPONSABLE'

        # Construir tabla de mapeo única de Cuentas -> Responsable y Nombre de Cuenta
        if col_m_num_cta and col_m_nom_cta and col_m_resp in df_main.columns:
            mapa_cuentas = df_main[[col_m_num_cta, col_m_nom_cta, col_m_resp]].drop_duplicates().copy()
            mapa_cuentas[col_m_num_cta] = mapa_cuentas[col_m_num_cta].astype(str).str.strip()
            mapa_cuentas[col_m_resp] = mapa_cuentas[col_m_resp].astype(str).str.strip().str.upper()
        else:
            mapa_cuentas = pd.DataFrame()

        # Mapear columna de número de cuenta en la hoja Vales
        col_v_num_cta = obtener_columna(df_vales, ['CUENTA', 'CTA CBLE', 'CUENTA CONTABLE', 'NRO CUENTA', 'CODIGO'])
        col_v_monto = obtener_columna(df_vales, ['MONTO', 'IMPORTE', 'TOTAL', 'SALDO', 'VALOR', 'PRECIO TOTAL', 'NETO_TOTAL_FACTURA', 'CANTIDAD'])
        col_v_mes = 'MES_NOMBRE' if 'MES_NOMBRE' in df_vales.columns else obtener_columna(df_vales, ['MES', 'FECHA'])

        df_v_trabajo = df_vales.copy()

        # Realizar el cruce de datos si existe el número de cuenta en Vales
        if col_v_num_cta and not mapa_cuentas.empty:
            df_v_trabajo['KEY_CTA'] = df_v_trabajo[col_v_num_cta].astype(str).str.strip()
            
            # Unir con la tabla de mapeo principal por Número de Cuenta
            df_v_trabajo = df_v_trabajo.merge(
                mapa_cuentas.rename(columns={
                    col_m_num_cta: 'KEY_CTA',
                    col_m_nom_cta: 'NOMBRE_CUENTA_MAP',
                    col_m_resp: 'RESPONSABLE_MAP'
                }),
                on='KEY_CTA',
                how='left'
            )
            
            # Nombre de la cuenta estandarizado
            col_nombre_mostrar = 'NOMBRE_CUENTA_MAP'
            col_resp_cruce = 'RESPONSABLE_MAP'
        else:
            # Fallback en caso de que no haya columna de número de cuenta
            col_nombre_mostrar = obtener_columna(df_v_trabajo, ['DESC CTA CBLE', 'CONCEPTO', 'CATEGORIA', 'RUBRO'])
            col_resp_cruce = obtener_columna(df_v_trabajo, ['RESPONSABLE', 'USUARIO', 'RETIRA'])

        # ---------------------------------------------------------
        # 2. FILTRADO POR RESPONSABLE LOGUEADO
        # ---------------------------------------------------------
        if not st.session_state['is_admin']:
            u_user = st.session_state['user'].upper()
            if col_resp_cruce in df_v_trabajo.columns:
                df_v_user = df_v_trabajo[df_v_trabajo[col_resp_cruce].astype(str).str.upper() == u_user].copy()
            else:
                df_v_user = df_v_trabajo.copy()
        else:
            st.sidebar.subheader("🎯 Filtros Administrador")
            resps_disp = sorted(df_main['RESPONSABLE'].dropna().unique()) if not df_main.empty else []
            f_resp_v = st.sidebar.multiselect("Filtrar por Responsables:", resps_disp, default=resps_disp)
            
            if f_resp_v and col_resp_cruce in df_v_trabajo.columns:
                resps_upper = [r.upper() for r in f_resp_v]
                df_v_user = df_v_trabajo[df_v_trabajo[col_resp_cruce].astype(str).str.upper().isin(resps_upper)].copy()
            else:
                df_v_user = df_v_trabajo.copy()

        # ---------------------------------------------------------
        # 3. FILTROS LATERALES (BUSQUEDA EXCLUSIVA POR NOMBRE DE CUENTA)
        # ---------------------------------------------------------
        st.sidebar.subheader("🎯 Filtros Vales de Consumo")
        
        # Filtro por Mes
        if col_v_mes and col_v_mes in df_v_user.columns:
            meses_v = sorted(df_v_user[col_v_mes].dropna().unique())
            f_mes_v = st.sidebar.multiselect("Filtrar Mes:", meses_v, default=meses_v)
            if f_mes_v:
                df_v_user = df_v_user[df_v_user[col_v_mes].isin(f_mes_v)]

        # Filtro por NOMBRE DE CUENTA (Sin números)
        if col_nombre_mostrar and col_nombre_mostrar in df_v_user.columns:
            nombres_cuentas_unicas = sorted(
                [str(c).strip() for c in df_v_user[col_nombre_mostrar].dropna().unique() if str(c).strip() != '-' and str(c).strip() != 'nan']
            )
            f_cta_nom = st.sidebar.multiselect("🔎 Filtrar Nombre de Cuenta Contable:", nombres_cuentas_unicas, default=[])
            if f_cta_nom:
                df_v_user = df_v_user[df_v_user[col_nombre_mostrar].astype(str).str.strip().isin(f_cta_nom)]

      # ---------------------------------------------------------
        # MÉTRICAS Y GRÁFICOS OPTIMIZADOS
        # ---------------------------------------------------------
        col_vg1, col_vg2 = st.columns([1.2, 1.1])
        
        with col_vg1:
            st.markdown('<div class="chart-box-title">📦 Top 5 Artículos más Consumidos</div>', unsafe_allow_html=True)
            col_v_art = obtener_columna(df_v_user, ['ARTICULO', 'ARTÍCULO', 'DESCRIPCION', 'DESCRIPCIÓN', 'DESCRIPCIÃ³N LARGA', 'DESCRIPCION LARGA', 'PRODUCTO', 'DETALLE'])
            
            if col_v_art and col_v_monto and col_v_art in df_v_user.columns:
                df_v_user[col_v_monto] = pd.to_numeric(df_v_user[col_v_monto], errors='coerce').fillna(0)
                
                # Agrupar por Artículo y obtener el Top 5 por monto
                g_art_v = df_v_user.groupby(col_v_art)[col_v_monto].apply(lambda x: abs(x.sum())).reset_index()
                g_art_v = g_art_v.sort_values(by=col_v_monto, ascending=True).tail(5)

                fig_art_v = px.bar(
                    g_art_v, 
                    x=col_v_monto, 
                    y=col_v_art, 
                    orientation='h',
                    color_discrete_sequence=['#E61C24']
                )
                
                fig_art_v.update_xaxes(title="", tickformat="$,.0f")
                fig_art_v.update_yaxes(title="")
                fig_art_v.update_traces(hovertemplate='<b>Artículo:</b> %{y}<br><b>Monto Consumido:</b> $%{x:,.0f}')
                
                fig_art_v.update_layout(
                    autosize=True, paper_bgcolor='#1F2937', plot_bgcolor='#1F2937', font=dict(color='#FFFFFF'),
                    height=300, margin=dict(l=15, r=15, t=15, b=25)
                )
                st.plotly_chart(fig_art_v, use_container_width=True, config=PLOTLY_CONFIG)
            else:
                st.info("ℹ️ No se detectó la columna de Artículos o Detalle en la hoja de Vales.")

        with col_vg2:
            st.markdown('<div class="chart-box-title">📊 Distribución por Nombre de Cuenta</div>', unsafe_allow_html=True)
            if col_nombre_mostrar and col_v_monto and col_nombre_mostrar in df_v_user.columns:
                df_v_user[col_v_monto] = pd.to_numeric(df_v_user[col_v_monto], errors='coerce').fillna(0)
                
                # Agrupar montos por cuenta
                g_cta_v = df_v_user.groupby(col_nombre_mostrar)[col_v_monto].apply(lambda x: abs(x.sum())).reset_index()
                total_monto = g_cta_v[col_v_monto].sum()

                if total_monto > 0:
                    # Agrupar cuentas con participación menor al 2% en "OTROS" para evitar desborde visual
                    g_cta_v['PCT'] = (g_cta_v[col_v_monto] / total_monto) * 100
                    principales = g_cta_v[g_cta_v['PCT'] >= 2.0].copy()
                    otros_monto = g_cta_v[g_cta_v['PCT'] < 2.0][col_v_monto].sum()

                    if otros_monto > 0:
                        fila_otros = pd.DataFrame([{col_nombre_mostrar: 'OTROS CONSUMOS', col_v_monto: otros_monto, 'PCT': (otros_monto/total_monto)*100}])
                        g_cta_v = pd.concat([principales, fila_otros], ignore_index=True)
                    else:
                        g_cta_v = principales
                
                g_cta_v = g_cta_v.sort_values(by=col_v_monto, ascending=False)
                
                fig_cv = px.pie(
                    g_cta_v, 
                    values=col_v_monto, 
                    names=col_nombre_mostrar, 
                    hole=0.45, 
                    color_discrete_sequence=['#E61C24', '#4B5563', '#9CA3AF', '#374151', '#D1D5DB']
                )
                
                # Solo muestra porcentaje dentro de la dona para evitar solapamientos de texto
                fig_cv.update_traces(
                    textposition='inside', 
                    textinfo='percent',
                    hovertemplate='<b>%{label}</b><br>Monto: $%{value:,.0f}<br>Porcentaje: %{percent}'
                )
                
                # Leyenda horizontal en la parte inferior para que no recorte nombres largos
                fig_cv.update_layout(
                    autosize=True, 
                    paper_bgcolor='#1F2937', 
                    plot_bgcolor='#1F2937', 
                    font=dict(color='#FFFFFF'),
                    height=300, 
                    margin=dict(l=15, r=15, t=10, b=45),
                    legend=dict(
                        orientation="h",
                        y=-0.2,
                        x=0,
                        font=dict(color='#FFFFFF', size=11)
                    )
                )
                st.plotly_chart(fig_cv, use_container_width=True, config=PLOTLY_CONFIG)
        # ---------------------------------------------------------
        # 5. TABLA GENERAL
        # ---------------------------------------------------------
        st.markdown("---")
        st.markdown("### 📋 Registro Detallado de Vales de Consumo")

        search_v = st.text_input("🔎 Buscar por Nombre de Cuenta, Artículos o Detalles:", "")
        
        # Ocultar columnas internas auxiliares usadas para el cruce
        cols_ocultar = ['KEY_CTA', 'RESPONSABLE_MAP']
        df_v_render = df_v_user.drop(columns=[c for c in cols_ocultar if c in df_v_user.columns]).copy()

        if search_v:
            mask_v = df_v_render.astype(str).apply(lambda x: x.str.lower().str.contains(search_v.lower())).any(axis=1)
            df_v_render = df_v_render[mask_v]

        st.dataframe(df_v_render, use_container_width=True, height=380)
# ---------------------------------------------------------
# MÓDULO 3: COMPRAS
# ---------------------------------------------------------
elif modulo_seleccionado == "🛒 Compras":
    st.markdown(f"""
        <div class="main-header">
            <h2>🛒 Registro y Control de Compras</h2>
            <p>Gestión de Órdenes y Proveedores | Usuario: <b>{st.session_state['user']}</b></p>
        </div>
    """, unsafe_allow_html=True)

    df_main = data_dict['main'] if data_dict else pd.DataFrame()
    df_compras = data_dict['compras'] if data_dict else pd.DataFrame()

    if df_compras.empty:
        st.info("ℹ️ No se encontraron datos en la pestaña de 'Compras'. Asegúrese de agregar la hoja al Excel.")
    else:
        # ---------------------------------------------------------
        # 1. CRUCE LÓGICO DE INFORMACIÓN (MAIN <-> COMPRAS)
        # ---------------------------------------------------------
        col_m_num_cta = obtener_columna(df_main, ['CUENTA', 'CTA CBLE', 'CUENTA CONTABLE', 'NRO CUENTA', 'CODIGO'])
        col_m_nom_cta = obtener_columna(df_main, ['DESC CTA CBLE', 'DESCRIPCION CUENTA', 'NOMBRE CUENTA', 'CUENTA_NORMALIZADA'])
        col_m_resp = 'RESPONSABLE'

        if col_m_num_cta and col_m_nom_cta and col_m_resp in df_main.columns:
            mapa_cuentas = df_main[[col_m_num_cta, col_m_nom_cta, col_m_resp]].drop_duplicates().copy()
            mapa_cuentas[col_m_num_cta] = mapa_cuentas[col_m_num_cta].astype(str).str.strip()
            mapa_cuentas[col_m_resp] = mapa_cuentas[col_m_resp].astype(str).str.strip().str.upper()
        else:
            mapa_cuentas = pd.DataFrame()

        col_c_num_cta = obtener_columna(df_compras, ['CUENTA', 'CTA CBLE', 'CUENTA CONTABLE', 'NRO CUENTA', 'CODIGO'])
        col_c_monto = obtener_columna(df_compras, ['MONTO', 'IMPORTE', 'TOTAL', 'SALDO', 'VALOR', 'PRECIO TOTAL', 'NETO_TOTAL_FACTURA', 'PRECIO', 'NETO'])
        col_c_mes = 'MES_NOMBRE' if 'MES_NOMBRE' in df_compras.columns else obtener_columna(df_compras, ['MES', 'FECHA'])

        df_c_trabajo = df_compras.copy()

        if col_c_num_cta and not mapa_cuentas.empty:
            df_c_trabajo['KEY_CTA'] = df_c_trabajo[col_c_num_cta].astype(str).str.strip()
            
            df_c_trabajo = df_c_trabajo.merge(
                mapa_cuentas.rename(columns={
                    col_m_num_cta: 'KEY_CTA',
                    col_m_nom_cta: 'NOMBRE_CUENTA_MAP',
                    col_m_resp: 'RESPONSABLE_MAP'
                }),
                on='KEY_CTA',
                how='left'
            )
            
            col_nombre_mostrar = 'NOMBRE_CUENTA_MAP'
            col_resp_cruce = 'RESPONSABLE_MAP'
        else:
            col_nombre_mostrar = obtener_columna(df_c_trabajo, ['DESC CTA CBLE', 'CONCEPTO', 'CATEGORIA', 'RUBRO', 'PROVEEDOR'])
            col_resp_cruce = obtener_columna(df_c_trabajo, ['RESPONSABLE', 'USUARIO', 'SOLICITANTE'])

        # ---------------------------------------------------------
        # 2. FILTRADO POR RESPONSABLE LOGUEADO
        # ---------------------------------------------------------
        if not st.session_state['is_admin']:
            u_user = st.session_state['user'].upper()
            if col_resp_cruce in df_c_trabajo.columns:
                df_c_user = df_c_trabajo[df_c_trabajo[col_resp_cruce].astype(str).str.upper() == u_user].copy()
            else:
                df_c_user = df_c_trabajo.copy()
        else:
            st.sidebar.subheader("🎯 Filtros Administrador")
            resps_disp = sorted(df_main['RESPONSABLE'].dropna().unique()) if not df_main.empty else []
            f_resp_c = st.sidebar.multiselect("Filtrar por Responsables:", resps_disp, default=resps_disp)
            
            if f_resp_c and col_resp_cruce in df_c_trabajo.columns:
                resps_upper = [r.upper() for r in f_resp_c]
                df_c_user = df_c_trabajo[df_c_trabajo[col_resp_cruce].astype(str).str.upper().isin(resps_upper)].copy()
            else:
                df_c_user = df_c_trabajo.copy()

        # ---------------------------------------------------------
        # 3. FILTROS LATERALES
        # ---------------------------------------------------------
        st.sidebar.subheader("🎯 Filtros Compras")
        
        if col_c_mes and col_c_mes in df_c_user.columns:
            meses_c = sorted(df_c_user[col_c_mes].dropna().unique())
            f_mes_c = st.sidebar.multiselect("Filtrar Mes:", meses_c, default=meses_c)
            if f_mes_c:
                df_c_user = df_c_user[df_c_user[col_c_mes].isin(f_mes_c)]

        if col_nombre_mostrar and col_nombre_mostrar in df_c_user.columns:
            nombres_cuentas_unicas = sorted(
                [str(c).strip() for c in df_c_user[col_nombre_mostrar].dropna().unique() if str(c).strip() != '-' and str(c).strip() != 'nan']
            )
            f_cta_nom_c = st.sidebar.multiselect("🔎 Filtrar Nombre de Cuenta Contable:", nombres_cuentas_unicas, default=[])
            if f_cta_nom_c:
                df_c_user = df_c_user[df_c_user[col_nombre_mostrar].astype(str).str.strip().isin(f_cta_nom_c)]

        # ---------------------------------------------------------
        # 4. MÉTRICAS Y GRÁFICOS OPTIMIZADOS
        # ---------------------------------------------------------
        compras_totales = len(df_c_user)
        monto_total_c = abs(pd.to_numeric(df_c_user[col_c_monto], errors='coerce').sum()) if col_c_monto else 0
        promedio_compra = (monto_total_c / compras_totales) if compras_totales > 0 else 0

        kc1, kc2, kc3 = st.columns(3)
        with kc1:
            st.markdown(f'<div class="custom-card"><div class="card-title">Monto Total Compras</div><div class="card-value">{formato_moneda(monto_total_c)}</div></div>', unsafe_allow_html=True)
        with kc2:
            st.markdown(f'<div class="custom-card"><div class="card-title">Cantidad de Registros</div><div class="card-value">{compras_totales:,}</div></div>', unsafe_allow_html=True)
        with kc3:
            st.markdown(f'<div class="custom-card"><div class="card-title">Promedio por Registro</div><div class="card-value">{formato_moneda(promedio_compra)}</div></div>', unsafe_allow_html=True)

       col_cg1, col_cg2 = st.columns([1.2, 1.1])
        
        with col_cg1:
            st.markdown('<div class="chart-box-title">🏢 Top 5 Proveedores más Solicitados</div>', unsafe_allow_html=True)
            # Priorizar nombre/razón social sobre el código numérico de proveedor
            col_c_prov = obtener_columna(df_c_user, ['NOMBRE PROVEEDOR', 'RAZON SOCIAL', 'RAZÓN SOCIAL', 'NOMBRE_PROVEEDOR', 'PROVEEDOR', 'PROVEEDORES'])
            
            if col_c_prov and col_c_monto and col_c_prov in df_c_user.columns:
                df_c_user[col_c_monto] = pd.to_numeric(df_c_user[col_c_monto], errors='coerce').fillna(0)
                
                # Convertir a texto para forzar etiquetas categóricas en Plotly
                df_c_user['PROVEEDOR_LABEL'] = df_c_user[col_c_prov].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
                df_c_clean = df_c_user[~df_c_user['PROVEEDOR_LABEL'].isin(['nan', 'None', '', '0', '-'])].copy()

                g_prov_c = df_c_clean.groupby('PROVEEDOR_LABEL')[col_c_monto].apply(lambda x: abs(x.sum())).reset_index()
                g_prov_c = g_prov_c.sort_values(by=col_c_monto, ascending=True).tail(5)

                fig_prov_c = px.bar(
                    g_prov_c, 
                    x=col_c_monto, 
                    y='PROVEEDOR_LABEL', 
                    orientation='h',
                    color_discrete_sequence=['#E61C24']
                )
                
                fig_prov_c.update_xaxes(title="", tickformat="$,.0f")
                fig_prov_c.update_yaxes(type='category', title="") # Forzar eje categórico
                fig_prov_c.update_traces(hovertemplate='<b>Proveedor:</b> %{y}<br><b>Monto Comprado:</b> $%{x:,.0f}')
                
                fig_prov_c.update_layout(
                    autosize=True, paper_bgcolor='#1F2937', plot_bgcolor='#1F2937', font=dict(color='#FFFFFF'),
                    height=300, margin=dict(l=15, r=15, t=15, b=25)
                )
                st.plotly_chart(fig_prov_c, use_container_width=True, config=PLOTLY_CONFIG)
            else:
                st.info("ℹ️ No se detectó la columna de Proveedores en la hoja de Compras.")

        with col_cg2:
            st.markdown('<div class="chart-box-title">📊 Distribución por Nombre de Cuenta</div>', unsafe_allow_html=True)
            if col_nombre_mostrar and col_c_monto and col_nombre_mostrar in df_c_user.columns:
                df_c_user[col_c_monto] = pd.to_numeric(df_c_user[col_c_monto], errors='coerce').fillna(0)
                
                g_cta_c = df_c_user.groupby(col_nombre_mostrar)[col_c_monto].apply(lambda x: abs(x.sum())).reset_index()
                total_monto_c = g_cta_c[col_c_monto].sum()

                if total_monto_c > 0:
                    g_cta_c['PCT'] = (g_cta_c[col_c_monto] / total_monto_c) * 100
                    principales_c = g_cta_c[g_cta_c['PCT'] >= 2.0].copy()
                    otros_monto_c = g_cta_c[g_cta_c['PCT'] < 2.0][col_c_monto].sum()

                    if otros_monto_c > 0:
                        fila_otros = pd.DataFrame([{col_nombre_mostrar: 'OTRAS COMPRAS', col_c_monto: otros_monto_c, 'PCT': (otros_monto_c/total_monto_c)*100}])
                        g_cta_c = pd.concat([principales_c, fila_otros], ignore_index=True)
                    else:
                        g_cta_c = principales_c
                
                g_cta_c = g_cta_c.sort_values(by=col_c_monto, ascending=False)
                
                fig_cc = px.pie(
                    g_cta_c, 
                    values=col_c_monto, 
                    names=col_nombre_mostrar, 
                    hole=0.45, 
                    color_discrete_sequence=['#E61C24', '#4B5563', '#9CA3AF', '#374151', '#D1D5DB']
                )
                
                fig_cc.update_traces(
                    textposition='inside', 
                    textinfo='percent',
                    hovertemplate='<b>%{label}</b><br>Monto: $%{value:,.0f}<br>Porcentaje: %{percent}'
                )
                
                fig_cc.update_layout(
                    autosize=True, paper_bgcolor='#1F2937', plot_bgcolor='#1F2937', font=dict(color='#FFFFFF'),
                    height=300, margin=dict(l=15, r=15, t=10, b=45),
                    legend=dict(
                        orientation="h",
                        y=-0.2,
                        x=0,
                        font=dict(color='#FFFFFF', size=11)
                    )
                )
                st.plotly_chart(fig_cc, use_container_width=True, config=PLOTLY_CONFIG)

        # ---------------------------------------------------------
        # 5. TABLA GENERAL
        # ---------------------------------------------------------
        st.markdown("---")
        st.markdown("### 📋 Registro Detallado de Compras")

        search_c = st.text_input("🔎 Buscar por Nombre de Cuenta, Proveedor o Detalles:", "")
        
        cols_ocultar_c = ['KEY_CTA', 'RESPONSABLE_MAP', 'MES_CATEGORIA']
        df_c_render = df_c_user.drop(columns=[c for c in cols_ocultar_c if c in df_c_user.columns]).copy()

        if search_c:
            mask_c = df_c_render.astype(str).apply(lambda x: x.str.lower().str.contains(search_c.lower())).any(axis=1)
            df_c_render = df_c_render[mask_c]

        st.dataframe(df_c_render, use_container_width=True, height=380)
