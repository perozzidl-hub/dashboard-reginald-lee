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

# Configuración de reescalado para Plotly
PLOTLY_CONFIG = {
    'responsive': True,
    'displayModeBar': False
}

# ---------------------------------------------------------
# ESTILOS CSS (Nitidez, Zoom & Contenedores)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* 1. TIPOGRAFÍA Y NITIDEZ GLOBAL */
    html, body, [class*="css"], .stApp {
        font-family: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
        text-rendering: optimizeLegibility !important;
    }

    .stApp {
        background-color: #0E1117 !important;
    }

    /* Ocultar textos sr-only */
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

    /* ------------------------------------
       ESTILIZACIÓN DE TÍTULOS DE GRÁFICOS (FIX ZOOM)
    ------------------------------------ */
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

    /* ------------------------------------
       TARJETA DE LOGIN Y CAMPOS
    ------------------------------------ */
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

    /* ------------------------------------
       SIDEBAR Y FILE UPLOADER
    ------------------------------------ */
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

    /* ------------------------------------
       MENÚS DESPLEGABLES (MULTISELECTS)
    ------------------------------------ */
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

    /* ------------------------------------
       ESTILOS DEL DASHBOARD PRINCIPAL
    ------------------------------------ */
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
# FUNCIONES AUXILIARES Y DATOS
# ---------------------------------------------------------
def formato_moneda(valor, con_decimales=False):
    if pd.isna(valor):
        return "$ 0"
    if con_decimales:
        res = f"{valor:,.2f}"
    else:
        res = f"{valor:,.0f}"
    return "$ " + res.replace(',', 'X').replace('.', ',').replace('X', '.')

@st.cache_data
def cargar_datos(file):
    df = pd.read_excel(file)
    if 'MES' in df.columns:
        df['MES_DT'] = pd.to_datetime(df['MES'])
        df['MES_NOMBRE'] = df['MES_DT'].dt.strftime('%Y-%m')
    
    cols_texto = ['INTERNO', 'DES1', 'DES2', 'TEXTO INTERNO', 'DESC CTA CBLE', 'RAZON', 'COMPROBANTE']
    for c in cols_texto:
        if c in df.columns:
            df[c] = df[c].fillna('-')
            
    return df

@st.cache_data
def obtener_base_inicial():
    try:
        return cargar_datos("Base Dashboard.xlsx")
    except Exception:
        return None

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = None
if 'is_admin' not in st.session_state:
    st.session_state['is_admin'] = False
if 'df_data' not in st.session_state:
    st.session_state['df_data'] = obtener_base_inicial()

# ---------------------------------------------------------
# LOGIN SCREEN (CON ÍCONO 🥤)
# ---------------------------------------------------------
if not st.session_state['logged_in']:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 1.1, 1])
    
    with col_l2:
        with st.form("login_form"):
            # ÍCONO DE VASO CON SORBETE 🥤
            st.markdown("""
                <div style="text-align: center; font-size: 55px; margin-bottom: 10px; line-height: 1;">
                    🥤
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="login-title">Reginald Lee S.A.</div>', unsafe_allow_html=True)
            st.markdown('<div class="login-subtitle">Plataforma de Control Presupuestario</div>', unsafe_allow_html=True)
            
            user_input = st.text_input("Usuario (Responsable)", placeholder="Ej: galdeman o admin").strip()
            pass_input = st.text_input("Contraseña", type="password").strip()
            submit_login = st.form_submit_button("🔑 Ingresar al Dashboard")
            
            if submit_login:
                if user_input and pass_input:
                    df_temp = st.session_state['df_data']
                    
                    if user_input.lower() == "admin" and pass_input == "admin@":
                        st.session_state['logged_in'] = True
                        st.session_state['user'] = "ADMINISTRADOR"
                        st.session_state['is_admin'] = True
                        st.rerun()
                    elif df_temp is not None:
                        responsables = [str(r).upper() for r in df_temp['RESPONSABLE'].dropna().unique()]
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
# MAIN DASHBOARD
# ---------------------------------------------------------
df = st.session_state['df_data']

# Sidebar
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

if st.session_state['is_admin']:
    st.sidebar.subheader("📤 Actualizar Base de Datos")
    new_file = st.sidebar.file_uploader("Subir Excel Principal", type=["xlsx"])
    if new_file is not None:
        st.session_state['df_data'] = cargar_datos(new_file)
        df = st.session_state['df_data']
        st.sidebar.success("✅ Base de datos actualizada")

# Header Principal
st.markdown(f"""
    <div class="main-header">
        <h2>📊 Control de Presupuesto y Gastos Fijos</h2>
        <p>Reginald Lee S.A. | Vista Ejecutiva — Usuario: <b>{st.session_state['user']}</b></p>
    </div>
""", unsafe_allow_html=True)

if df is not None:
    if not st.session_state['is_admin']:
        df_user = df[df['RESPONSABLE'].astype(str).str.upper() == st.session_state['user']]
    else:
        df_user = df.copy()

    # Filtros
    st.sidebar.subheader("🎯 Filtros Generales")
    meses_disponibles = sorted(df_user['MES_NOMBRE'].dropna().unique())
    locaciones_disponibles = sorted(df_user['LOCACION'].dropna().unique())
    grupos_disponibles = sorted(df_user['GRUPO DE CUENTAS'].dropna().unique())

    f_mes = st.sidebar.multiselect("Meses", meses_disponibles, default=meses_disponibles)
    f_loc = st.sidebar.multiselect("Locación / Planta", locaciones_disponibles, default=locaciones_disponibles)
    f_grupo = st.sidebar.multiselect("Grupo de Cuentas", grupos_disponibles, default=grupos_disponibles)

    if st.session_state['is_admin']:
        resps_disponibles = sorted(df_user['RESPONSABLE'].dropna().unique())
        f_resp = st.sidebar.multiselect("Responsable Sector", resps_disponibles, default=resps_disponibles)
    else:
        f_resp = [st.session_state['user']]

    # Dataset Filtrado
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

    # KPI Cards
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(f"""
            <div class="custom-card">
                <div class="card-title">Presupuesto Asignado</div>
                <div class="card-value">{formato_moneda(tot_presupuesto)}</div>
            </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
            <div class="custom-card">
                <div class="card-title">Gasto Real Ejecutado</div>
                <div class="card-value">{formato_moneda(tot_gasto)}</div>
            </div>
        """, unsafe_allow_html=True)

    with k3:
        sub_color = "text-red" if desviacion > 0 else "text-green"
        st.markdown(f"""
            <div class="custom-card">
                <div class="card-title">Desviación Presupuestaria</div>
                <div class="card-value">{formato_moneda(desviacion)}</div>
                <div class="card-sub {sub_color}">Diferencia acumulada</div>
            </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
            <div class="custom-card">
                <div class="card-title">% Ejecución Presupuestaria</div>
                <div class="card-value">{pct_ejecucion:.1f}%</div>
                <div class="card-sub text-red" style="visibility: {'visible' if pct_ejecucion > 100 else 'hidden'};">Excedido de Presupuesto</div>
            </div>
        """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # SECCIÓN GRÁFICOS
    # ---------------------------------------------------------
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
            autosize=True,
            paper_bgcolor='#1F2937', plot_bgcolor='#1F2937', font=dict(color='#FFFFFF'),
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
            autosize=True,
            paper_bgcolor='#1F2937', plot_bgcolor='#1F2937', font=dict(color='#FFFFFF'),
            xaxis=dict(gridcolor='#374151', tickfont=dict(color='#FFFFFF', size=11), automargin=True),
            yaxis=dict(gridcolor='#374151', tickfont=dict(color='#FFFFFF', size=10), automargin=True),
            height=310, margin=dict(l=10, r=15, t=10, b=25), xaxis_title="", yaxis_title=""
        )
        st.plotly_chart(fig_grupo, use_container_width=True, config=PLOTLY_CONFIG)

    with col_g3:
        st.markdown('<div class="chart-box-title">🎯 Nivel de Ejecución</div>', unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = pct_ejecucion,
            number = {'suffix': "%", 'font': {'size': 26, 'color': '#FFFFFF', 'family': 'Arial'}},
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
            autosize=True,
            paper_bgcolor='#1F2937', plot_bgcolor='#1F2937', font=dict(color='#FFFFFF'),
            height=310, margin=dict(l=35, r=35, t=35, b=25)
        )
        st.plotly_chart(fig_gauge, use_container_width=True, config=PLOTLY_CONFIG)

    # Segunda fila
    c_r2_1, c_r2_2 = st.columns([1, 1.5])

    with c_r2_1:
        st.markdown('<div class="chart-box-title">🏢 Gastos por Locación</div>', unsafe_allow_html=True)
        g_loc = gasto_df.groupby('LOCACION')['SALDO'].apply(lambda x: abs(x.sum())).reset_index()
        fig_loc = px.pie(
            g_loc, values='SALDO', names='LOCACION', hole=0.4,
            color_discrete_sequence=['#E61C24', '#6B7280', '#9CA3AF', '#D1D5DB', '#374151']
        )
        fig_loc.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(color='#FFFFFF'))
        fig_loc.update_layout(
            autosize=True,
            paper_bgcolor='#1F2937', plot_bgcolor='#1F2937', font=dict(color='#FFFFFF'),
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

        fig_desv = px.bar(
            top_desv, x='Desviacion', y='DESC CTA CBLE', orientation='h',
            color='Desviacion', color_continuous_scale=['#6B7280', '#E61C24']
        )
        fig_desv.update_layout(
            autosize=True,
            paper_bgcolor='#1F2937', plot_bgcolor='#1F2937', font=dict(color='#FFFFFF'),
            xaxis=dict(gridcolor='#374151', tickfont=dict(color='#FFFFFF'), automargin=True),
            yaxis=dict(gridcolor='#374151', tickfont=dict(color='#FFFFFF'), automargin=True),
            height=300, margin=dict(l=15, r=15, t=15, b=15), xaxis_title="Desviación en $", yaxis_title=""
        )
        st.plotly_chart(fig_desv, use_container_width=True, config=PLOTLY_CONFIG)

    # Tabla Transaccional
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

    cols_tabla = [
        'FECHA', 'MES_NOMBRE', 'LOCACION', 'RESPONSABLE', 
        'GRUPO DE CUENTAS', 'DESC CTA CBLE', 'DES1', 'INTERNO', 'MONTO_FORMATO'
    ]

    df_render = df_auditoria[cols_tabla].rename(columns={
        'MES_NOMBRE': 'MES',
        'DESC CTA CBLE': 'CUENTA CONTABLE',
        'DES1': 'PROVEEDOR / ENTIDAD',
        'INTERNO': 'N° INTERNO',
        'MONTO_FORMATO': 'MONTO ($)'
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
    else:
        st.info("No hay registros disponibles para inspeccionar con los filtros actuales.")
