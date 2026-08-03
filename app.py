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

# ---------------------------------------------------------
# ESTILOS CSS RESPONSIVE, ALTO CONTRASTE Y BORDES REDONDEADOS
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Fondo General de la App */
    .stApp {
        background-color: #F8F9FA !important;
    }
    
    /* 1. CORRECCIÓN BARRA LATERAL (SIDEBAR): TEXTOS EN BLANCO Y LEGIBLES */
    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] h4, 
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stSelectbox label {
        color: #E5E7EB !important;
    }

    /* FORZAR COLOR NEGRO VISIBLE EN TÍTULOS DEL CUERPO PRINCIPAL */
    .main h1, .main h2, .main h3, .main h4, .main h5,
    div[data-testid="stMarkdownContainer"] h3 {
        color: #111827 !important;
        font-weight: 700 !important;
    }

    /* Header Corporativo Coca-Cola */
    .main-header {
        background: linear-gradient(135deg, #111111 0%, #E61C24 100%);
        padding: 20px 25px;
        border-radius: 16px; /* Bordes suaves */
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(230, 28, 36, 0.2);
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

    /* CARDS DE KPI (BORDES SUAVES Y REDONDEADOS) */
    .custom-card {
        background-color: #FFFFFF;
        border-radius: 16px !important; /* Bordes redondeados */
        padding: 18px 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
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
        color: #4B5563 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    .card-value {
        font-size: 20px;
        font-weight: 800;
        color: #111827 !important;
        margin-bottom: 2px;
    }
    .card-sub {
        font-size: 11px;
        font-weight: 600;
    }
    .text-red { color: #E61C24 !important; }
    .text-green { color: #10B981 !important; }

    /* 3. BORDES SUAVES Y REDONDEADOS PARA CONTENEDORES DE GRÁFICOS */
    .chart-container {
        background-color: #0E1117;
        border-radius: 16px !important; /* Suaviza bordes a 16px */
        padding: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        overflow: hidden;
        margin-bottom: 15px;
    }

    /* Inspección de Texto Interno */
    .detail-popup {
        background-color: #FFFBEB;
        border-left: 5px solid #F59E0B;
        padding: 15px 20px;
        border-radius: 12px;
        margin: 15px 0;
    }

    /* RESPONSIVE MÓVIL */
    @media (max-width: 768px) {
        .main-header { padding: 15px 18px; }
        .main-header h2 { font-size: 18px !important; }
        .custom-card { padding: 12px 15px; }
        .card-value { font-size: 18px !important; }
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# FUNCIONES AUXILIARES (FORMATO ARGENTINO $ 10.000,85)
# ---------------------------------------------------------
def formato_moneda(valor, con_decimales=False):
    if pd.isna(valor):
        return "$ 0"
    if con_decimales:
        res = f"{valor:,.2f}"
    else:
        res = f"{valor:,.0f}"
    return "$ " + res.replace(',', 'X').replace('.', ',').replace('X', '.')

# ---------------------------------------------------------
# CARGA Y PROCESAMIENTO DE DATOS
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
# MÓDULO DE LOGIN
# ---------------------------------------------------------
if not st.session_state['logged_in']:
    col_l1, col_l2, col_l3 = st.columns([1, 1.4, 1])
    with col_l2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background-color: white; padding: 25px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; border-top: 6px solid #E61C24;">
                <h2 style="color: #E61C24 !important; margin-bottom: 5px; font-size: 24px;">🥤 Reginald Lee S.A.</h2>
                <p style="color: #4B5563 !important; font-weight: 600; margin-bottom: 20px;">Plataforma de Control Presupuestario</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
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
# DASHBOARD DE GESTIÓN (SESIÓN INICIADA)
# ---------------------------------------------------------
df = st.session_state['df_data']

# Sidebar con estilos claros
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

# Carga exclusiva Administrador
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
    # Seguridad por Usuario
    if not st.session_state['is_admin']:
        df_user = df[df['RESPONSABLE'].astype(str).str.upper() == st.session_state['user']]
    else:
        df_user = df.copy()

    # Filtros Barra Lateral
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

    # ---------------------------------------------------------
    # 1. CARDS DE KPI (BORDES REDONDEADOS)
    # ---------------------------------------------------------
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
    # 2. PRIMERA FILA DE GRÁFICOS (BORDES SUAVES Y % EN BLANCO)
    # ---------------------------------------------------------
    col_g1, col_g2, col_g3 = st.columns([1.5, 1.2, 1])

    with col_g1:
        st.markdown("<h3 style='color: #111827 !important; margin-bottom: 10px;'>📅 Presupuesto vs Real por Mes</h3>", unsafe_allow_html=True)
        p_mes = presupuesto_df.groupby('MES_NOMBRE')['SALDO'].sum().reset_index().rename(columns={'SALDO': 'Presupuesto'})
        g_mes = gasto_df.groupby('MES_NOMBRE')['SALDO'].apply(lambda x: abs(x.sum())).reset_index().rename(columns={'SALDO': 'Gasto Real'})
        comp_mes = pd.merge(p_mes, g_mes, on='MES_NOMBRE', how='outer').fillna(0)

        fig_mes = go.Figure()
        fig_mes.add_trace(go.Bar(x=comp_mes['MES_NOMBRE'], y=comp_mes['Presupuesto'], name='Presupuesto', marker_color='#9CA3AF'))
        fig_mes.add_trace(go.Bar(x=comp_mes['MES_NOMBRE'], y=comp_mes['Gasto Real'], name='Gasto Real', marker_color='#E61C24'))
        fig_mes.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            barmode='group',
            height=310,
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", y=1.15)
        )
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig_mes, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_g2:
        st.markdown("<h3 style='color: #111827 !important; margin-bottom: 10px;'>📊 Gasto por Grupo de Cuentas</h3>", unsafe_allow_html=True)
        g_grupo = gasto_df.groupby('GRUPO DE CUENTAS')['SALDO'].apply(lambda x: abs(x.sum())).reset_index().sort_values(by='SALDO', ascending=True).tail(7)
        fig_grupo = px.bar(g_grupo, x='SALDO', y='GRUPO DE CUENTAS', orientation='h', color_discrete_sequence=['#E61C24'])
        fig_grupo.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=310,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="",
            yaxis_title=""
        )
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig_grupo, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_g3:
        st.markdown("<h3 style='color: #111827 !important; margin-bottom: 10px;'>🎯 Nivel de Ejecución</h3>", unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = pct_ejecucion,
            # FUENTE DEL % CAMBIADA A BLANCO BRILLANTE (#FFFFFF)
            number = {'suffix': "%", 'font': {'size': 26, 'color': '#FFFFFF', 'family': 'Arial'}},
            gauge = {
                'axis': {'range': [0, max(120, pct_ejecucion)], 'tickcolor': "#FFFFFF"},
                'bar': {'color': "#E61C24" if pct_ejecucion > 100 else "#6B7280"},
                'steps': [
                    {'range': [0, 80], 'color': "#374151"},
                    {'range': [80, 100], 'color': "#4B5563"},
                    {'range': [100, max(120, pct_ejecucion)], 'color': "#991B1B"}
                ]
            }
        ))
        fig_gauge.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=310,
            margin=dict(l=15, r=15, t=15, b=15)
        )
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 3. SEGUNDA FILA DE GRÁFICOS
    # ---------------------------------------------------------
    c_r2_1, c_r2_2 = st.columns([1, 1.5])

    with c_r2_1:
        st.markdown("<h3 style='color: #111827 !important; margin-bottom: 10px;'>🏢 Gastos por Locación</h3>", unsafe_allow_html=True)
        g_loc = gasto_df.groupby('LOCACION')['SALDO'].apply(lambda x: abs(x.sum())).reset_index()
        fig_loc = px.pie(
            g_loc, values='SALDO', names='LOCACION', hole=0.4,
            color_discrete_sequence=['#E61C24', '#4B5563', '#9CA3AF', '#D1D5DB', '#F3F4F6']
        )
        fig_loc.update_traces(textposition='inside', textinfo='percent+label')
        fig_loc.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=310,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig_loc, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c_r2_2:
        st.markdown("<h3 style='color: #111827 !important; margin-bottom: 10px;'>⚠️ Cuentas con Mayor Desviación</h3>", unsafe_allow_html=True)
        p_cta = presupuesto_df.groupby('DESC CTA CBLE')['SALDO'].sum().rename('Presupuesto')
        g_cta = gasto_df.groupby('DESC CTA CBLE')['SALDO'].apply(lambda x: abs(x.sum())).rename('Gasto Real')
        comp_cta = pd.concat([p_cta, g_cta], axis=1).fillna(0)
        comp_cta['Desviacion'] = comp_cta['Gasto Real'] - comp_cta['Presupuesto']
        top_desv = comp_cta.sort_values(by='Desviacion', ascending=False).head(5).reset_index()

        fig_desv = px.bar(
            top_desv, x='Desviacion', y='DESC CTA CBLE', orientation='h',
            color='Desviacion', color_continuous_scale=['#4B5563', '#E61C24']
        )
        fig_desv.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=310,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Desviación en $",
            yaxis_title=""
        )
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig_desv, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 4. TABLA TRANSACCIONAL DE GASTOS
    # ---------------------------------------------------------
    st.markdown("---")
    st.markdown("<h3 style='color: #111827 !important;'>🔍 Consulta y Auditoría Transaccional de Gastos</h3>", unsafe_allow_html=True)

    df_auditoria = gasto_df.copy()

    # MULTISELECT CUENTAS Y BÚSQUEDA
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

    # Inversión de signo
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

    st.dataframe(
        df_render,
        use_container_width=True,
        height=380
    )

    # ---------------------------------------------------------
    # INSPECTOR DE TEXTO INTERNO (POP-UP DETALLE)
    # ---------------------------------------------------------
    st.markdown("<h4 style='color: #111827 !important; margin-top: 15px;'>📌 Inspeccionar 'Texto Interno' de un Gasto Específico</h4>", unsafe_allow_html=True)
    
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
                    <h5 style="color: #B45309 !important; margin: 0 0 8px 0;">📝 Texto Interno / Detalle Completo de la Compra</h5>
                    <p style="font-size: 15px; font-weight: 600; color: #1F2937 !important; margin: 0;">"{item_row['TEXTO INTERNO']}"</p>
                    <hr style="margin: 10px 0; border-color: #FDE68A;">
                    <small style="color: #4B5563 !important;"><b>Proveedor:</b> {item_row['DES1']} | <b>Cuenta:</b> {item_row['DESC CTA CBLE']} | <b>N° Interno:</b> {item_row['INTERNO']} | <b>Comprobante:</b> {item_row['COMPROBANTE']}</small>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No hay registros disponibles para inspeccionar con los filtros actuales.")
