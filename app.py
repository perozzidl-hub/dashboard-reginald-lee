import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Reginald Lee - Dashboard Presupuestario",
    page_icon="🥤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS de Alta Definición y Alto Contraste
st.markdown("""
    <style>
    /* Fondo General */
    .stApp {
        background-color: #F4F6F9;
    }
    
    /* Header Corporativo */
    .main-header {
        background: linear-gradient(135deg, #111111 0%, #E61C24 100%);
        padding: 20px 25px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    .main-header h2 {
        color: #FFFFFF !important;
        margin: 0;
        font-weight: 800;
        font-size: 26px;
    }
    .main-header p {
        margin-top: 5px;
        color: #E5E7EB !important;
        font-size: 14px;
    }

    /* FORZAR VISIBILIDAD Y ALTO CONTRASTE EN MÉTRICAS Y TEXTOS */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        padding: 16px 20px !important;
        border-radius: 12px !important;
        border-top: 4px solid #E61C24 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08) !important;
    }
    
    /* Etiquetas / Títulos de las Métricas */
    div[data-testid="stMetricLabel"] label, div[data-testid="stMetricLabel"] div {
        color: #374151 !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }
    
    /* Valor numérico de las Métricas */
    div[data-testid="stMetricValue"] div {
        color: #111827 !important;
        font-size: 22px !important;
        font-weight: 800 !important;
    }

    /* Titulares de Secciones */
    .section-title {
        color: #111827 !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        margin-bottom: 15px !important;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Cards Visuales Contenedoras de Gráficos */
    .chart-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        border: 1px solid #E5E7EB;
    }

    /* Pop-up / Tarjeta de Inspección de Texto Interno */
    .detail-popup {
        background-color: #FFFBEB;
        border-left: 6px solid #F59E0B;
        padding: 15px 20px;
        border-radius: 8px;
        margin-top: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

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
# AUTENTICACIÓN (LOGIN)
# ---------------------------------------------------------
if not st.session_state['logged_in']:
    col_l1, col_l2, col_l3 = st.columns([1, 1.4, 1])
    with col_l2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background-color: white; padding: 35px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; border-top: 6px solid #E61C24;">
                <h2 style="color: #E61C24; margin-bottom: 5px; font-size: 28px;">🥤 Reginald Lee S.A.</h2>
                <p style="color: #4B5563; font-weight: 600; margin-bottom: 25px;">Plataforma de Control Presupuestario</p>
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

# Sidebar
st.sidebar.markdown(f"👤 **Usuario Activo:** `{st.session_state['user']}`")
if st.session_state['is_admin']:
    st.sidebar.caption("🔑 Perfil: Administrador")
else:
    st.sidebar.caption("📊 Perfil: Responsable de Sector")

if st.sidebar.button("🚪 Cerrar Sesión"):
    st.session_state['logged_in'] = False
    st.session_state['user'] = None
    st.session_state['is_admin'] = False
    st.rerun()

st.sidebar.markdown("---")

# Carga exclusiva para Administrador
if st.session_state['is_admin']:
    st.sidebar.subheader("📤 Carga de Datos")
    new_file = st.sidebar.file_uploader("Actualizar Excel Principal", type=["xlsx"])
    if new_file is not None:
        st.session_state['df_data'] = cargar_datos(new_file)
        df = st.session_state['df_data']
        st.sidebar.success("✅ Datos actualizados correctamente")

# Header Principal
st.markdown(f"""
    <div class="main-header">
        <h2>📊 Control de Presupuesto y Gastos Fijos</h2>
        <p>Reginald Lee S.A. | Vista Ejecutiva — Usuario: <b>{st.session_state['user']}</b></p>
    </div>
""", unsafe_allow_html=True)

if df is not None:
    # Filtro de Seguridad por Responsable
    if not st.session_state['is_admin']:
        df_user = df[df['RESPONSABLE'].astype(str).str.upper() == st.session_state['user']]
    else:
        df_user = df.copy()

    # Filtros Globales
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

    # Aplicar Filtros Generales
    df_f = df_user[
        (df_user['MES_NOMBRE'].isin(f_mes)) &
        (df_user['LOCACION'].isin(f_loc)) &
        (df_user['GRUPO DE CUENTAS'].isin(f_grupo)) &
        (df_user['RESPONSABLE'].astype(str).str.upper().isin(f_resp))
    ]

    presupuesto_df = df_f[df_f['TIPO2'] == 'PRESUPUESTO']
    gasto_df = df_f[df_f['TIPO2'] == 'GASTO']

    tot_presupuesto = presupuesto_df['SALDO'].sum()
    tot_gasto = abs(gasto_df['SALDO'].sum())  # Valor absoluto para visualización clara
    desviacion = tot_gasto - tot_presupuesto
    pct_ejecucion = (tot_gasto / tot_presupuesto * 100) if tot_presupuesto > 0 else 0

    # ---------------------------------------------------------
    # 1. TARJETAS DE KPIs (CON ALTO CONTRASTE Y FORMATO LIMPIO)
    # ---------------------------------------------------------
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Presupuesto Asignado", f"$ {tot_presupuesto:,.0f}")
    k2.metric("Gasto Real Ejecutado", f"$ {tot_gasto:,.0f}")
    k3.metric("Desviación Presupuestaria", f"$ {desviacion:,.0f}", delta=f"$ {desviacion:,.0f}", delta_color="inverse")
    k4.metric("% Ejecución Presupuestaria", f"{pct_ejecucion:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 2. SECCIÓN PRINCIPAL DE GRÁFICOS (GRID BI)
    # ---------------------------------------------------------
    col_g1, col_g2, col_g3 = st.columns([1.5, 1.2, 1])

    with col_g1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📅 Presupuesto vs Real por Mes</div>', unsafe_allow_html=True)
        p_mes = presupuesto_df.groupby('MES_NOMBRE')['SALDO'].sum().reset_index().rename(columns={'SALDO': 'Presupuesto'})
        g_mes = gasto_df.groupby('MES_NOMBRE')['SALDO'].apply(lambda x: abs(x.sum())).reset_index().rename(columns={'SALDO': 'Gasto Real'})
        comp_mes = pd.merge(p_mes, g_mes, on='MES_NOMBRE', how='outer').fillna(0)

        fig_mes = go.Figure()
        fig_mes.add_trace(go.Bar(x=comp_mes['MES_NOMBRE'], y=comp_mes['Presupuesto'], name='Presupuesto', marker_color='#1E1E1E'))
        fig_mes.add_trace(go.Bar(x=comp_mes['MES_NOMBRE'], y=comp_mes['Gasto Real'], name='Gasto Real', marker_color='#E61C24'))
        fig_mes.update_layout(barmode='group', template='plotly_white', height=290, margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig_mes, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_g2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Gasto por Grupo de Cuentas</div>', unsafe_allow_html=True)
        g_grupo = gasto_df.groupby('GRUPO DE CUENTAS')['SALDO'].apply(lambda x: abs(x.sum())).reset_index().sort_values(by='SALDO', ascending=True).tail(7)
        fig_grupo = px.bar(g_grupo, x='SALDO', y='GRUPO DE CUENTAS', orientation='h', color_discrete_sequence=['#E61C24'])
        fig_grupo.update_layout(template='plotly_white', height=290, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="", yaxis_title="")
        st.plotly_chart(fig_grupo, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_g3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🎯 Nivel de Ejecución</div>', unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = pct_ejecucion,
            number = {'suffix': "%", 'font': {'size': 24, 'color': '#111827'}},
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
        fig_gauge.update_layout(height=290, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 3. SEGUNDA FILA: LOCACIÓN Y TOP DESVIACIONES
    # ---------------------------------------------------------
    c_r2_1, c_r2_2 = st.columns([1, 1.5])

    with c_r2_1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🏢 Gastos por Locación</div>', unsafe_allow_html=True)
        g_loc = gasto_df.groupby('LOCACION')['SALDO'].apply(lambda x: abs(x.sum())).reset_index()
        fig_loc = px.pie(
            g_loc, values='SALDO', names='LOCACION', hole=0.4,
            color_discrete_sequence=['#E61C24', '#1E1E1E', '#7F1D1D', '#9CA3AF', '#D1D5DB']
        )
        fig_loc.update_traces(textposition='inside', textinfo='percent+label')
        fig_loc.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_loc, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c_r2_2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⚠️ Cuentas con Mayor Desviación</div>', unsafe_allow_html=True)
        p_cta = presupuesto_df.groupby('DESC CTA CBLE')['SALDO'].sum().rename('Presupuesto')
        g_cta = gasto_df.groupby('DESC CTA CBLE')['SALDO'].apply(lambda x: abs(x.sum())).rename('Gasto Real')
        comp_cta = pd.concat([p_cta, g_cta], axis=1).fillna(0)
        comp_cta['Desviacion'] = comp_cta['Gasto Real'] - comp_cta['Presupuesto']
        top_desv = comp_cta.sort_values(by='Desviacion', ascending=False).head(5).reset_index()

        fig_desv = px.bar(
            top_desv, x='Desviacion', y='DESC CTA CBLE', orientation='h',
            color='Desviacion', color_continuous_scale=['#1E1E1E', '#E61C24']
        )
        fig_desv.update_layout(template='plotly_white', height=300, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="Desviación en $", yaxis_title="")
        st.plotly_chart(fig_desv, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 4. TABLA TRANSACCIONAL AUDITABLE CON FILTRO DE CUENTA Y INVERSIÓN DE SIGNO
    # ---------------------------------------------------------
    st.markdown("---")
    st.markdown('<div class="section-title">🔍 Consulta y Auditoría Transaccional de Gastos</div>', unsafe_allow_html=True)

    df_gasto_auditoria = gasto_df.copy()

    # FILTRO ESPECÍFICO POR CUENTA CONTABLE
    cuentas_unicas = sorted(df_gasto_auditoria['DESC CTA CBLE'].dropna().unique())
    col_f1, col_f2 = st.columns([2, 1])
    
    with col_f1:
        f_cuentas_tabla = st.multiselect("🔎 Filtrar por Cuenta Contable:", cuentas_unicas, default=[])
    with col_f2:
        search_kw = st.text_input("💬 Buscar por Proveedor / Interno:", "")

    # Aplicar filtro de cuenta si hay seleccionadas
    if f_cuentas_tabla:
        df_gasto_auditoria = df_gasto_auditoria[df_gasto_auditoria['DESC CTA CBLE'].isin(f_cuentas_tabla)]

    # Aplicar búsqueda por palabra clave
    if search_kw:
        sk = search_kw.lower()
        mask = (
            df_gasto_auditoria['DES1'].astype(str).str.lower().str.contains(sk) |
            df_gasto_auditoria['INTERNO'].astype(str).str.lower().str.contains(sk) |
            df_gasto_auditoria['TEXTO INTERNO'].astype(str).str.lower().str.contains(sk)
        )
        df_gasto_auditoria = df_gasto_auditoria[mask]

    # REGLA DE SIGNOS SOLICITADA:
    # Si SALDO < 0 (es un gasto ordinario) -> se invierte a Positivo (SALDO * -1)
    # Si SALDO > 0 (es un recupero/crédito) -> se muestra en Negativo
    df_gasto_auditoria['MONTO_AJUSTADO'] = df_gasto_auditoria['SALDO'] * -1

    # Formatear columnas
    df_gasto_auditoria['REGISTRO_ID'] = df_gasto_auditoria.index
    cols_tabla = [
        'FECHA', 'MES_NOMBRE', 'LOCACION', 'RESPONSABLE', 
        'GRUPO DE CUENTAS', 'DESC CTA CBLE', 'DES1', 'INTERNO', 'MONTO_AJUSTADO', 'TEXTO INTERNO'
    ]

    df_render = df_gasto_auditoria[cols_tabla].rename(columns={
        'MES_NOMBRE': 'MES',
        'DESC CTA CBLE': 'CUENTA CONTABLE',
        'DES1': 'PROVEEDOR / ENTIDAD',
        'INTERNO': 'N° INTERNO',
        'MONTO_AJUSTADO': 'MONTO ($)'
    })

    # Mostrar la Tabla
    st.dataframe(
        df_render.style.format({
            'MONTO ($)': '$ {:,.2f}'
        }),
        use_container_width=True,
        height=380
    )

    # ---------------------------------------------------------
    # INSPECTOR DINÁMICO DE TEXTO INTERNO (POP-UP / EXPANDABLE)
    # ---------------------------------------------------------
    st.markdown("##### 📌 Inspeccionar 'Texto Interno' de un Gasto Especifico")
    
    # Crear una lista amigable para seleccionar y ver el detalle
    if not df_gasto_auditoria.empty:
        opciones_inspeccion = df_gasto_auditoria.apply(
            lambda r: f"ID {r.name} | {r['FECHA']} | {r['DES1']} | ${r['MONTO_AJUSTADO']:,.0f} | {r['DESC CTA CBLE']}", axis=1
        ).tolist()
        
        selected_option = st.selectbox("Seleccione una transacción para desplegar su detalle completo:", opciones_inspeccion)
        
        if selected_option:
            selected_id = int(selected_option.split(" | ")[0].replace("ID ", ""))
            item_row = df_gasto_auditoria.loc[selected_id]
            
            st.markdown(f"""
                <div class="detail-popup">
                    <h5 style="color: #B45309; margin: 0 0 8px 0;">📝 Texto Interno / Detalle Completo de la Compra</h5>
                    <p style="font-size: 16px; font-weight: 600; color: #1F2937; margin: 0;">"{item_row['TEXTO INTERNO']}"</p>
                    <hr style="margin: 10px 0; border-color: #FDE68A;">
                    <small style="color: #4B5563;"><b>Proveedor:</b> {item_row['DES1']} | <b>Cuenta:</b> {item_row['DESC CTA CBLE']} | <b>N° Interno:</b> {item_row['INTERNO']} | <b>Comprobante:</b> {item_row['COMPROBANTE']}</small>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No hay registros disponibles para inspeccionar con los filtros actuales.")
