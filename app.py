import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILOS NATIVOS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Reginald Lee - Dashboard Presupuestario",
    page_icon="🥤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS limpios y libres de conflictos
st.markdown("""
    <style>
    /* Fondo General */
    .stApp {
        background-color: #F8F9FA !important;
    }
    
    /* Header Corporativo Coca-Cola */
    .main-header {
        background: linear-gradient(135deg, #111111 0%, #E61C24 100%);
        padding: 22px 30px;
        border-radius: 14px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(230, 28, 36, 0.2);
    }
    .main-header h2 {
        color: #FFFFFF !important;
        margin: 0;
        font-weight: 800;
        font-size: 26px;
    }
    .main-header p {
        margin-top: 5px;
        color: #F3F4F6 !important;
        font-size: 14px;
        margin-bottom: 0;
    }

    /* CARDS PERSONALIZADAS CON CONTROL TOTAL DE ALINEACIÓN Y CONTRASTE */
    .custom-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 18px 22px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.06);
        border-top: 5px solid #E61C24;
        margin-bottom: 20px;
        min-height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .card-title {
        font-size: 13px;
        font-weight: 700;
        color: #4B5563;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .card-value {
        font-size: 22px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 2px;
    }
    .card-sub {
        font-size: 12px;
        font-weight: 600;
    }
    .text-red { color: #E61C24; }
    .text-green { color: #10B981; }

    /* Tarjetas para Gráficos */
    .chart-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        border: 1px solid #E5E7EB;
    }
    .chart-title {
        font-size: 16px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Inspección de Texto Interno */
    .detail-popup {
        background-color: #FFFBEB;
        border-left: 5px solid #F59E0B;
        padding: 15px 20px;
        border-radius: 8px;
        margin: 15px 0;
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
    # Intercambiar coma por punto para miles y punto por coma para decimales
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
    # 1. CARDS DE KPI TOTALMENTE HIGIENIZADAS Y VISIBLES (HTML/CSS)
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
    # 2. SECCIÓN PRINCIPAL DE GRÁFICOS (ALINEACIÓN LIMPIA)
    # ---------------------------------------------------------
    col_g1, col_g2, col_g3 = st.columns([1.5, 1.2, 1])

    with col_g1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📅 Presupuesto vs Real por Mes</div>', unsafe_allow_html=True)
        p_mes = presupuesto_df.groupby('MES_NOMBRE')['SALDO'].sum().reset_index().rename(columns={'SALDO': 'Presupuesto'})
        g_mes = gasto_df.groupby('MES_NOMBRE')['SALDO'].apply(lambda x: abs(x.sum())).reset_index().rename(columns={'SALDO': 'Gasto Real'})
        comp_mes = pd.merge(p_mes, g_mes, on='MES_NOMBRE', how='outer').fillna(0)

        fig_mes = go.Figure()
        fig_mes.add_trace(go.Bar(x=comp_mes['MES_NOMBRE'], y=comp_mes['Presupuesto'], name='Presupuesto', marker_color='#1E1E1E'))
        fig_mes.add_trace(go.Bar(x=comp_mes['MES_NOMBRE'], y=comp_mes['Gasto Real'], name='Gasto Real', marker_color='#E61C24'))
        fig_mes.update_layout(barmode='group', template='plotly_white', height=280, margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", y=1.15))
        st.plotly_chart(fig_mes, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_g2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📊 Gasto por Grupo de Cuentas</div>', unsafe_allow_html=True)
        g_grupo = gasto_df.groupby('GRUPO DE CUENTAS')['SALDO'].apply(lambda x: abs(x.sum())).reset_index().sort_values(by='SALDO', ascending=True).tail(7)
        fig_grupo = px.bar(g_grupo, x='SALDO', y='GRUPO DE CUENTAS', orientation='h', color_discrete_sequence=['#E61C24'])
        fig_grupo.update_layout(template='plotly_white', height=280, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="", yaxis_title="")
        st.plotly_chart(fig_grupo, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_g3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🎯 Nivel de Ejecución</div>', unsafe_allow_html=True)
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
        fig_gauge.update_layout(height=280, margin=dict(l=15, r=15, t=15, b=15))
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 3. SEGUNDA FILA DE GRÁFICOS
    # ---------------------------------------------------------
    c_r2_1, c_r2_2 = st.columns([1, 1.5])

    with c_r2_1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🏢 Gastos por Locación</div>', unsafe_allow_html=True)
        g_loc = gasto_df.groupby('LOCACION')['SALDO'].apply(lambda x: abs(x.sum())).reset_index()
        fig_loc = px.pie(
            g_loc, values='SALDO', names='LOCACION', hole=0.4,
            color_discrete_sequence=['#E61C24', '#1E1E1E', '#7F1D1D', '#9CA3AF', '#D1D5DB']
        )
        fig_loc.update_traces(textposition='inside', textinfo='percent+label')
        fig_loc.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_loc, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c_r2_2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">⚠️ Cuentas con Mayor Desviación</div>', unsafe_allow_html=True)
        p_cta = presupuesto_df.groupby('DESC CTA CBLE')['SALDO'].sum().rename('Presupuesto')
        g_cta = gasto_df.groupby('DESC CTA CBLE')['SALDO'].apply(lambda x: abs(x.sum())).rename('Gasto Real')
        comp_cta = pd.concat([p_cta, g_cta], axis=1).fillna(0)
        comp_cta['Desviacion'] = comp_cta['Gasto Real'] - comp_cta['Presupuesto']
        top_desv = comp_cta.sort_values(by='Desviacion', ascending=False).head(5).reset_index()

        fig_desv = px.bar(
            top_desv, x='Desviacion', y='DESC CTA CBLE', orientation='h',
            color='Desviacion', color_continuous_scale=['#1E1E1E', '#E61C24']
        )
        fig_desv.update_layout(template='plotly_white', height=280, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="Desviación en $", yaxis_title="")
        st.plotly_chart(fig_desv, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 4. TABLA TRANSACCIONAL DE GASTOS (SIGNOS INVERTIDOS + FORMATO $ 10.000,85)
    # ---------------------------------------------------------
    st.markdown("---")
    st.markdown('<div class="chart-title">🔍 Consulta y Auditoría Transaccional de Gastos</div>', unsafe_allow_html=True)

    df_auditoria = gasto_df.copy()

    # MULTISELECT CUENTAS
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

    # INVERSIÓN ESTRICTA DE SIGNO PARA GASTOS:
    # SALDO (ej: -10000.85) -> * -1 -> 10000.85 (Positivo para gasto normal)
    df_auditoria['MONTO_MOSTRAR'] = df_auditoria['SALDO'] * -1

    # Formatear la columna de texto con el estándar $ 10.000,85
    df_auditoria['MONTO_FORMATO'] = df_auditoria['MONTO_MOSTRAR'].apply(lambda v: formato_moneda(v, con_decimales=True))

    cols_tabla = [
        'FECHA', 'MES_NOMBRE', 'LOCACION', 'RESPONSABLE', 
        'GRUPO DE CUENTAS', 'DESC CTA CBLE', 'DES1', 'INTERNO', 'MONTO_FORMATO', 'TEXTO INTERNO'
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
    st.markdown("##### 📌 Inspeccionar 'Texto Interno' de un Gasto Especifico")
    
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
                    <h5 style="color: #B45309; margin: 0 0 8px 0;">📝 Texto Interno / Detalle Completo de la Compra</h5>
                    <p style="font-size: 16px; font-weight: 600; color: #1F2937; margin: 0;">"{item_row['TEXTO INTERNO']}"</p>
                    <hr style="margin: 10px 0; border-color: #FDE68A;">
                    <small style="color: #4B5563;"><b>Proveedor:</b> {item_row['DES1']} | <b>Cuenta:</b> {item_row['DESC CTA CBLE']} | <b>N° Interno:</b> {item_row['INTERNO']} | <b>Comprobante:</b> {item_row['COMPROBANTE']}</small>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No hay registros disponibles para inspeccionar con los filtros actuales.")
