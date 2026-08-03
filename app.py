import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILOS COCA-COLA / REGINALD LEE
# ---------------------------------------------------------
st.set_page_config(
    page_title="Reginald Lee - Dashboard Presupuestario",
    page_icon="🥤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado estilo Dashboard BI (Cards, Sombras, Colores Coca-Cola)
st.markdown("""
    <style>
    /* Fondo General */
    .stApp {
        background-color: #F3F4F6;
    }
    
    /* Header Corporativo */
    .main-header {
        background: linear-gradient(90deg, #1E1E1E 0%, #E61C24 100%);
        padding: 15px 25px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .main-header h2 {
        color: white !important;
        margin: 0;
        font-weight: 700;
    }
    .main-header p {
        margin: 0;
        opacity: 0.9;
        font-size: 14px;
    }

    /* Cards Visuales */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        padding: 15px 20px;
        border-radius: 10px;
        border-left: 5px solid #E61C24;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        font-weight: bold;
        color: #1E1E1E;
    }
    
    /* Cajas contenedoras para gráficos */
    .chart-card {
        background-color: #FFFFFF;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    
    /* Botones */
    .stButton>button {
        background-color: #E61C24;
        color: white;
        border-radius: 6px;
        border: none;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #BA1219;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# CARGA DE DATOS
# ---------------------------------------------------------
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

# Base inicial
@st.cache_data
def obtener_base_inicial():
    try:
        return cargar_datos("Base Dashboard.xlsx")
    except Exception:
        return None

# Estado de la sesión para mantener login y datos
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = None
if 'is_admin' not in st.session_state:
    st.session_state['is_admin'] = False
if 'df_data' not in st.session_state:
    st.session_state['df_data'] = obtener_base_inicial()

# ---------------------------------------------------------
# MÓDULO DE AUTENTICACIÓN (LOGIN)
# ---------------------------------------------------------
if not st.session_state['logged_in']:
    col_l1, col_l2, col_l3 = st.columns([1, 1.5, 1])
    with col_l2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background-color: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center;">
                <h2 style="color: #E61C24; margin-bottom: 5px;">🥤 Reginald Lee S.A.</h2>
                <p style="color: #6B7280; margin-bottom: 20px;">Control Presupuestario y Gastos Fijos</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            user_input = st.text_input("Usuario (Responsable)", placeholder="ej: galdeman o admin").strip()
            pass_input = st.text_input("Contraseña", type="password").strip()
            submit_login = st.form_submit_button("Ingresar al Sistema")
            
            if submit_login:
                if user_input and pass_input:
                    df_temp = st.session_state['df_data']
                    
                    # Validación Admin
                    if user_input.lower() == "admin" and pass_input == "admin@":
                        st.session_state['logged_in'] = True
                        st.session_state['user'] = "ADMINISTRADOR"
                        st.session_state['is_admin'] = True
                        st.rerun()
                    
                    # Validación Usuarios (Responsables)
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
                            st.error("❌ Usuario o contraseña incorrectos.")
                    else:
                        st.error("⚠️ Base de datos no disponible.")
                else:
                    st.warning("Por favor complete todos los campos.")
    st.stop()

# ---------------------------------------------------------
# PANELES Y NAVEGACIÓN (USUARIO AUTENTICADO)
# ---------------------------------------------------------
df = st.session_state['df_data']

# Sidebar de Usuario y Filtros
st.sidebar.markdown(f"👤 **Usuario:** `{st.session_state['user']}`")
if st.session_state['is_admin']:
    st.sidebar.caption("🔑 Rol: Administrador General")
else:
    st.sidebar.caption("📊 Rol: Responsable de Sector")

if st.sidebar.button("Cerrar Sesión"):
    st.session_state['logged_in'] = False
    st.session_state['user'] = None
    st.session_state['is_admin'] = False
    st.rerun()

st.sidebar.markdown("---")

# SOLO EL ADMIN PUEDE SUBIR EL EXCEL
if st.session_state['is_admin']:
    st.sidebar.subheader("📤 Actualizar Base de Datos")
    new_file = st.sidebar.file_uploader("Subir nuevo Excel (Pisar Base)", type=["xlsx"])
    if new_file is not None:
        st.session_state['df_data'] = cargar_datos(new_file)
        df = st.session_state['df_data']
        st.sidebar.success("✅ Base de datos actualizada correctamente")

# Header Principal
st.markdown(f"""
    <div class="main-header">
        <h2>📊 Dashboard de Control Presupuestario</h2>
        <p>Reginald Lee S.A. | Vista de Gestión Visual — Usuario: <b>{st.session_state['user']}</b></p>
    </div>
""", unsafe_allow_html=True)

if df is not None:
    # FILTRADO DE SEGURIDAD POR USUARIO
    if not st.session_state['is_admin']:
        # Forzar filtro por el Responsable logueado
        df_user = df[df['RESPONSABLE'].astype(str).str.upper() == st.session_state['user']]
    else:
        df_user = df.copy()

    # Filtros Dinámicos
    st.sidebar.subheader("🎯 Filtros Visuales")
    meses_disponibles = sorted(df_user['MES_NOMBRE'].dropna().unique())
    locaciones_disponibles = sorted(df_user['LOCACION'].dropna().unique())
    grupos_disponibles = sorted(df_user['GRUPO DE CUENTAS'].dropna().unique())

    f_mes = st.sidebar.multiselect("Meses", meses_disponibles, default=meses_disponibles)
    f_loc = st.sidebar.multiselect("Locación / Planta", locaciones_disponibles, default=locaciones_disponibles)
    f_grupo = st.sidebar.multiselect("Grupo de Cuentas", grupos_disponibles, default=grupos_disponibles)

    # Si es admin, puede filtrar por otros responsables
    if st.session_state['is_admin']:
        resps_disponibles = sorted(df_user['RESPONSABLE'].dropna().unique())
        f_resp = st.sidebar.multiselect("Responsable", resps_disponibles, default=resps_disponibles)
    else:
        f_resp = [st.session_state['user']]

    # Dataset Filtrado Final
    df_f = df_user[
        (df_user['MES_NOMBRE'].isin(f_mes)) &
        (df_user['LOCACION'].isin(f_loc)) &
        (df_user['GRUPO DE CUENTAS'].isin(f_grupo)) &
        (df_user['RESPONSABLE'].astype(str).str.upper().isin(f_resp))
    ]

    presupuesto_df = df_f[df_f['TIPO2'] == 'PRESUPUESTO']
    gasto_df = df_f[df_f['TIPO2'] == 'GASTO']

    tot_presupuesto = presupuesto_df['SALDO'].sum()
    tot_gasto = gasto_df['SALDO'].sum()
    desviacion = tot_gasto - tot_presupuesto
    pct_ejecucion = (tot_gasto / tot_presupuesto * 100) if tot_presupuesto > 0 else 0

    # ---------------------------------------------------------
    # 1. FILA DE METRICAS VISUALES (CARDS DENSE STYLE)
    # ---------------------------------------------------------
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Presupuesto Asignado", f"$ {tot_presupuesto:,.0f}")
    k2.metric("Gasto Real Ejecutado", f"$ {tot_gasto:,.0f}")
    k3.metric("Desviación ($)", f"$ {desviacion:,.0f}", delta=f"$ {desviacion:,.0f}", delta_color="inverse")
    k4.metric("% Ejecución Presupuestaria", f"{pct_ejecucion:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 2. GRID PRINCIPAL DE GRÁFICOS
    # ---------------------------------------------------------
    c_col1, c_col2, c_col3 = st.columns([1.5, 1.2, 1])

    # Chart 1: Evolución Mensual
    with c_col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("📅 Presupuesto vs Real por Mes")
        p_mes = presupuesto_df.groupby('MES_NOMBRE')['SALDO'].sum().reset_index().rename(columns={'SALDO': 'Presupuesto'})
        g_mes = gasto_df.groupby('MES_NOMBRE')['SALDO'].sum().reset_index().rename(columns={'SALDO': 'Gasto Real'})
        comp_mes = pd.merge(p_mes, g_mes, on='MES_NOMBRE', how='outer').fillna(0)

        fig_mes = go.Figure()
        fig_mes.add_trace(go.Bar(x=comp_mes['MES_NOMBRE'], y=comp_mes['Presupuesto'], name='Presupuesto', marker_color='#1E1E1E'))
        fig_mes.add_trace(go.Bar(x=comp_mes['MES_NOMBRE'], y=comp_mes['Gasto Real'], name='Gasto Real', marker_color='#E61C24'))
        fig_mes.update_layout(barmode='group', template='plotly_white', height=300, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_mes, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Chart 2: Top Grupos de Cuentas
    with c_col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("📊 Gasto por Grupo de Cuentas")
        g_grupo = gasto_df.groupby('GRUPO DE CUENTAS')['SALDO'].sum().reset_index().sort_values(by='SALDO', ascending=True).tail(7)
        fig_grupo = px.bar(g_grupo, x='SALDO', y='GRUPO DE CUENTAS', orientation='h', color_discrete_sequence=['#E61C24'])
        fig_grupo.update_layout(template='plotly_white', height=300, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="", yaxis_title="")
        st.plotly_chart(fig_grupo, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Chart 3: Gauge de Ejecución Total
    with c_col3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("🎯 Nivel de Ejecución")
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = pct_ejecucion,
            number = {'suffix': "%"},
            gauge = {
                'axis': {'range': [0, max(120, pct_ejecucion)]},
                'bar': {'color': "#E61C24" if pct_ejecucion > 100 else "#1E1E1E"},
                'steps': [
                    {'range': [0, 80], 'color': "#E5E7EB"},
                    {'range': [80, 100], 'color': "#D1D5DB"},
                    {'range': [100, max(120, pct_ejecucion)], 'color': "#FCA5A5"}
                ]
            }
        ))
        fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 3. SEGUNDA FILA VISUAL: LOCACIONES Y TOP DESVIACIONES
    # ---------------------------------------------------------
    c_row2_1, c_row2_2 = st.columns([1, 1.5])

    with c_row2_1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("🏢 Distribución por Locación")
        g_loc = gasto_df.groupby('LOCACION')['SALDO'].sum().reset_index()
        fig_loc = px.pie(
            g_loc, values='SALDO', names='LOCACION',
            hole=0.4,
            color_discrete_sequence=['#E61C24', '#1E1E1E', '#7F1D1D', '#9CA3AF', '#D1D5DB', '#4B5563']
        )
        fig_loc.update_traces(textposition='inside', textinfo='percent+label')
        fig_loc.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_loc, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c_row2_2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("⚠️ Top Cuentas Contables con Mayor Desviación")
        p_cta = presupuesto_df.groupby('DESC CTA CBLE')['SALDO'].sum().rename('Presupuesto')
        g_cta = gasto_df.groupby('DESC CTA CBLE')['SALDO'].sum().rename('Gasto Real')
        comp_cta = pd.concat([p_cta, g_cta], axis=1).fillna(0)
        comp_cta['Desviacion'] = comp_cta['Gasto Real'] - comp_cta['Presupuesto']
        top_desv = comp_cta.sort_values(by='Desviacion', ascending=False).head(5).reset_index()

        fig_desv = px.bar(
            top_desv, x='Desviacion', y='DESC CTA CBLE', orientation='h',
            color='Desviacion', color_continuous_scale=['#1E1E1E', '#E61C24']
        )
        fig_desv.update_layout(template='plotly_white', height=320, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="Desviación en $", yaxis_title="")
        st.plotly_chart(fig_desv, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 4. TABLA DETALLADA SOLO PARA CONSULTA RÁPIDA (EXPANDER)
    # ---------------------------------------------------------
    with st.expander("🔎 Ver Tabla Transaccional de Gastos"):
        cols_mostrar = ['FECHA', 'MES_NOMBRE', 'LOCACION', 'RESPONSABLE', 'GRUPO DE CUENTAS', 'DESC CTA CBLE', 'DES1', 'TEXTO INTERNO', 'SALDO']
        st.dataframe(
            gasto_df[cols_mostrar].rename(columns={'MES_NOMBRE': 'MES', 'DESC CTA CBLE': 'CUENTA', 'DES1': 'PROVEEDOR', 'SALDO': 'MONTO ($)'}),
            use_container_width=True
        )
